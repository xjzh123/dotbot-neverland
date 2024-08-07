from typing import Any, Literal, Mapping, Optional, Self

from attrs import define

from ..utils.validators import validate_trip
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
    def parse(cls, _data: Mapping[str, Any], **extra_kwds) -> Self:
        data: dict = _data.copy()  # type: ignore
        data["trip"] = validate_trip(data.get("trip"))
        if "raw" in data:
            data.pop("raw")
        return super().parse(data, raw=data, **extra_kwds)
