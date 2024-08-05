from typing import Any, Mapping, TypedDict


EventRawData = TypedDict(
    "EventRawData",
    {
        "cmd": str,
        "channel": str,
        "text": str,
        "type": str,
        "nick": str,
        "trip": str,
        "from": str | int,
        "to": str | int,
        "nicks": list[str],
        "users": list[Mapping[str, Any]],
        "time": str,
        "color": str,
        "admin": bool,
        "mod": bool,
        "inviteChannel": str,
    },
    total=False,
)
