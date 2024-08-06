from __future__ import annotations

import asyncio
import json
import ssl
from collections import OrderedDict
from typing import Any, Awaitable, Callable, Collection, Coroutine, Literal

import websockets
from attr import define
from attrs import asdict

from .models import (
    BotJoinEvent,
    ChangeNickEvent,
    ChatEvent,
    Event,
    UpdateUserEvent,
    User,
    UserJoinEvent,
    UserLeaveEvent,
    WhisperEvent,
)
from .parsing import parse
from .utils.aliases import Alias, aliases

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

    async def whisper(self, nick: str, text: str):
        await self.send_json({"cmd": "whisper", "nick": nick, "text": text})

    async def emote(self, text: str):
        await self.send_json({"cmd": "emote", "text": text})

    async def change_nick(self, nick: str):
        self.nick = nick
        await self.send_json({"cmd": "changenick", "nick": nick})

    def _add_listener(self, event_type: ListenerKey, listener: Listener):
        if event_type not in self.listeners.keys():
            self.listeners[event_type] = []

        self.listeners[event_type].append(listener)

    def add_listener(self, matcher: ListenerKey | Alias, listener: Listener):
        if isinstance(matcher, str) and matcher != "*":
            matcher = aliases[matcher]
        self._add_listener(matcher, listener)

    def listen(self, matchers: Collection[ListenerKey | Alias], listener: Listener):
        for matcher in matchers:
            self.add_listener(matcher, listener)

    def on(self, *matchers: ListenerKey | Alias):
        def deco(listener: Listener):
            self.listen(matchers, listener)
            return listener

        return deco

    async def _internal_handler(self, ctx: Context[Event]):
        e = ctx.event
        match e:
            case UserJoinEvent():
                self.users_dict[e.user.nick] = e.user
            case UserLeaveEvent():
                self.users_dict.pop(e.nick)
            case BotJoinEvent():
                self.users_dict = OrderedDict([(user.nick, user) for user in e.users])
            case UpdateUserEvent():
                user = self.users_dict[e.nick]
                self.users_dict[e.nick] = User.parse({**asdict(user), **e.raw})

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

    async def reply(self, text: str):
        if isinstance(self.event, ChatEvent):
            await self.bot.chat(text)
        elif isinstance(self.event, WhisperEvent):
            await self.bot.whisper(self.event.nick, text)
        else:
            raise ValueError(
                f"Context[{type(self.event).__name__}] doesn't support reply"
            )
