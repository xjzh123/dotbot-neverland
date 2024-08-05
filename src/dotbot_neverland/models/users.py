from typing import Any, Literal, Mapping, Optional, Self

from attrs import define

from ._base import Base


@define
class User(Base):
    channel: str
    color: Optional[str]
    hash: str
    isBot: bool
    level: int
    nick: str
    trip: Optional[str]
    uType: Literal["user", "mod", "admin"]
    userid: int

    raw: Mapping[str, Any]

    @classmethod
    def parse(cls, data: Mapping[str, Any], **extra_kwds) -> Self:
        return super().parse(data, raw=data, **extra_kwds)
