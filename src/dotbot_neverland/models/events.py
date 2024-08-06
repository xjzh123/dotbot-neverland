from typing import Self

from attrs import define

from ._base import Base
from .raw import EventRawData
from .users import User

__all__ = [
    "Event",
    "InfoEvent",
    "ChatEvent",
    "EmoteEvent",
    "WarnEvent",
    "BotJoinEvent",
    "CaptchaEvent",
    "UserJoinEvent",
    "UserLeaveEvent",
    "UpdateUserEvent",
    "WhisperEvent",
    "InviteEvent",
    "ChangeNickEvent",
]


@define
class Event(Base):
    cmd: str
    raw: EventRawData

    @classmethod
    def parse(cls, data: EventRawData, **extra_kwds) -> Self:
        return super().parse(data, raw=data, **extra_kwds)


@define
class InfoEvent(Event):
    type: str | None
    text_raw: str


@define
class ChatEvent(Event):
    nick: str
    trip: str | None
    text: str


@define
class EmoteEvent(InfoEvent):
    nick: str
    trip: str | None
    text: str


@define
class WarnEvent(Event):
    text: str


@define
class BotJoinEvent(Event):
    users: list[User]


@define
class CaptchaEvent(Event):
    text: str


@define
class UserJoinEvent(Event):
    user: User


@define
class UserLeaveEvent(Event):
    nick: str


@define
class UpdateUserEvent(Event):
    nick: str
    # Some of the other fields are hard to model,
    # because they may or may not be present,
    # and requires complex fallback to something like attrs.NOTHING.
    # Since this event is hardly used, it is acceptable to only use the nick
    # and the raw data.


@define
class WhisperEvent(InfoEvent):
    nick: str
    trip: str | None
    text: str


@define
class InviteEvent(Event):
    nick: str
    channel: str


@define
class ChangeNickEvent(Event):
    old_nick: str
    new_nick: str
