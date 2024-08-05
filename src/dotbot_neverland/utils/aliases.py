from typing import Literal, Mapping

from ..models.events import *

Alias = Literal[
    "info",
    "chat",
    "emote",
    "warn",
    "onlineSet",
    "captcha",
    "onlineAdd",
    "onlineRemove",
    "updateUser",
    "whisper",
    "invite",
    "changeNick",
]

aliases: Mapping[Alias, type[Event]] = {
    "info": InfoEvent,
    "chat": ChatEvent,
    "emote": EmoteEvent,
    "warn": WarnEvent,
    "onlineSet": BotJoinEvent,
    "captcha": CaptchaEvent,
    "onlineAdd": UserJoinEvent,
    "onlineRemove": UserLeaveEvent,
    "updateUser": UpdateUserEvent,
    "whisper": WhisperEvent,
    "invite": InviteEvent,
    "changeNick": ChangeNickEvent,
}
