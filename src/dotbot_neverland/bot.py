from __future__ import annotations

import asyncio
import json
import ssl
import warnings
from collections import OrderedDict
from typing import Any, Awaitable, Callable, Collection, Coroutine, Literal

import websockets
from attrs import asdict, define

from .models import (
    ChangeNickEvent,
    ChatEvent,
    Event,
    SelfJoinEvent,
    UpdateUserEvent,
    User,
    UserJoinEvent,
    UserLeaveEvent,
    WarnEvent,
    WhisperEvent,
)
from .parsing import parse
from .utils.aliases import Alias, aliases
from .utils.custom_id import generate_customid

type Listener[T: Event] = Callable[[Context[T]], None | Awaitable[None]]
type ListenerKey = type[Event] | Literal["*"]


HC_WS_URL = "wss://hack.chat/chat-ws"


class Bot:
    def __init__(self) -> None:
        self.is_connected = False
        self.listeners: dict[ListenerKey, list[Listener]] = {
            "*": [self._internal_handler]
        }
        self.ws: websockets.WebSocketClientProtocol | None = None
        self.users_dict: OrderedDict[str, User] = OrderedDict()

        self.channel = self.nick = self.password = ""

    async def _connect(self, ws_url: str, ws_opts={}, bypass_dns=False):
        if bypass_dns:
            if ws_url != HC_WS_URL:
                raise ValueError("Bypass DNS is only supported for hack.chat")

            insecure_ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
            insecure_ssl_context.check_hostname = False
            insecure_ssl_context.verify_mode = ssl.CERT_NONE
            self.ws = await websockets.connect(
                HC_WS_URL,
                host="104.131.138.176",
                ssl=insecure_ssl_context,
                **ws_opts,
            )
        else:
            self.ws = await websockets.connect(ws_url, **ws_opts)

    async def _join(self, channel: str, nick: str, password: str | None = None):
        payload: dict = {"cmd": "join", "channel": channel, "nick": nick}
        if password:
            payload["password"] = password
        await self.send_json(payload)

    async def connect(
        self,
        channel: str,
        nick: str,
        password: str | None = None,
        ws_url: str = HC_WS_URL,
        ws_opts={},
        bypass_dns=False,
    ):
        self.channel = channel
        self.nick = nick
        self.password = password
        await self._connect(ws_url, ws_opts=ws_opts, bypass_dns=bypass_dns)
        self.is_connected = True
        await self._join(channel, nick, password)
        try:
            while self.ws and self.ws.open:
                message = await self.ws.recv()
                obj = json.loads(message)
                event = parse(obj)

                if event is None:
                    continue

                ctx = Context(self, event)

                await self.dispatch("*", ctx)

                await self.dispatch(type(event), ctx)
        except asyncio.exceptions.CancelledError:
            pass
        finally:
            await self.close()

    async def dispatch[T: Event](
        self, event_type: type[T] | Literal["*"], ctx: Context[T]
    ):
        listeners = self.listeners.get(event_type, [])

        coros: list[Coroutine] = []

        for listener in listeners:
            result = listener(ctx)

            if asyncio.iscoroutine(result):
                coros.append(result)

        await asyncio.gather(*coros)

    async def close(self):
        if self.ws:
            self.is_connected = False
            await self.ws.close()
            self.ws = None

    async def send_raw(self, data: websockets.Data):
        if not self.ws:
            raise RuntimeError("Can't send data when not connected")
        await self.ws.send(data)

    async def send_json(self, obj: Any):
        await self.send_raw(json.dumps(obj))

    async def chat(self, text: str):
        await self.send_json({"cmd": "chat", "text": text})

    async def send(self, text: str):  # the same as `chat`
        await self.send_json({"cmd": "chat", "text": text})

    async def chat_updatable(self, text: str):
        customId = generate_customid()
        await self.send_json({"cmd": "chat", "text": text, "customId": customId})
        return UpdatableMessage(text, customId, self)

    async def whisper(self, nick: str, text: str):
        await self.send_json({"cmd": "whisper", "nick": nick, "text": text})

    async def emote(self, text: str):
        await self.send_json({"cmd": "emote", "text": text})

    async def change_nick(self, nick: str):
        await self.send_json({"cmd": "changenick", "nick": nick})

    async def change_color(self, color: str | None):
        await self.send_json({"cmd": "changecolor", "color": color or "reset"})

    def _add_listener(self, event_type: ListenerKey, listener: Listener):
        if event_type not in self.listeners.keys():
            self.listeners[event_type] = []

        self.listeners[event_type].append(listener)

    def add_listener(
        self,
        matcher: ListenerKey | Alias,
        listener: Listener,
        *,
        ignore_self: bool = True,
    ):
        if isinstance(matcher, str) and matcher != "*":
            matcher = aliases[matcher]
        if ignore_self:

            def _listener(c: Context, /):
                if hasattr(c.event, "nick"):
                    if c.event.nick == self.nick:  # type: ignore
                        return
                return listener(c)
        else:
            _listener = listener
        self._add_listener(matcher, _listener)

    def listen(
        self,
        matchers: Collection[ListenerKey | Alias],
        listener: Listener,
        *,
        ignore_self: bool = True,
    ):
        for matcher in matchers:
            self.add_listener(matcher, listener, ignore_self=ignore_self)

    def on(self, *matchers: ListenerKey | Alias, ignore_self: bool = True):
        def deco(listener: Listener):
            self.listen(matchers, listener, ignore_self=ignore_self)
            return listener

        return deco

    async def _internal_handler(self, ctx: Context[Event]):
        e = ctx.event
        match e:
            case UserJoinEvent():
                self.users_dict[e.user.nick] = e.user
            case UserLeaveEvent():
                self.users_dict.pop(e.nick)
            case SelfJoinEvent():
                self.users_dict = OrderedDict([(user.nick, user) for user in e.users])
            case UpdateUserEvent():
                user = self.users_dict[e.nick]
                # `User.parse` automatically adds `raw` attribute, and `asdict(user)` also provides a `raw`
                # So the previous `raw` must be discarded
                self.users_dict[e.nick] = User.parse({**asdict(user), **e.raw})
            case ChangeNickEvent():
                if e.old_nick == self.nick:
                    self.nick = e.new_nick
            case WarnEvent():
                warnings.warn(f"Warning from server: {e.text}")
        if "channel" in e.raw:
            if (channel := e.raw["channel"]) != self.channel:
                warnings.warn(
                    f"Unexpected channel: {channel} (expecting {self.channel})"
                )

    @property
    def nicks(self):
        return self.users_dict.keys()

    @property
    def users(self):
        return self.users_dict.values()


@define
class Context[T: Event]:
    bot: Bot
    event: T

    @property
    def pair(self):
        return (self.bot, self.event)

    def get_user(self):
        if isinstance(self.event, UserJoinEvent):
            return self.event.user

        elif isinstance(self.event, ChangeNickEvent):
            return self.bot.users_dict[self.event.old_nick]

        return self.bot.users_dict[self.event.nick]  # type: ignore

    def get_channel(self):
        return self.event.raw.get("channel")

    async def reply(self, text: str, whisper_newline: str | bool = False):
        if isinstance(self.event, ChatEvent):
            await self.bot.chat(text)
        elif isinstance(self.event, WhisperEvent):
            if whisper_newline:
                if isinstance(whisper_newline, bool):
                    whisper_newline = ">"
                text = f"{whisper_newline}\n{text}"
            await self.bot.whisper(self.event.nick, text)
        else:
            raise ValueError(
                f"Context[{type(self.event).__name__}] doesn't support reply"
            )


type UpdateMessageMode = Literal["overwrite", "prepend", "append"]


@define
class UpdatableMessage:
    text: str
    customId: str

    bot: Bot

    def _update(self, mode: UpdateMessageMode, text: str):
        return {
            "cmd": "updateMessage",
            "mode": mode,
            "text": text,
            "customId": self.customId,
        }

    def _overwrite(self, text: str):
        return self._update("overwrite", text)

    def _prepend(self, text: str):
        return self._update("prepend", text)

    def _append(self, text: str):
        return self._update("append", text)

    def _complete(self):
        return {
            "cmd": "updateMessage",
            "mode": "complete",
            "customId": self.customId,
        }

    async def update(self, mode: UpdateMessageMode, text: str):
        await self.bot.send_json(self._update(mode, text))

    async def overwrite(self, text: str):
        await self.bot.send_json(self._overwrite(text))

    async def prepend(self, text: str):
        await self.bot.send_json(self._prepend(text))

    async def append(self, text: str):
        await self.bot.send_json(self._append(text))

    async def complete(self):
        await self.bot.send_json(self._complete())
