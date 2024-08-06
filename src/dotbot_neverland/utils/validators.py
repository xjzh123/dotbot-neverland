import re

validate_nick_regex = re.compile(r"^[a-zA-Z0-9_]{1,24}$")


def is_valid_nick(nick: str) -> bool:
    return bool(validate_nick_regex.fullmatch(nick))


def strip_nick(nick: str) -> str:
    return nick.strip().removeprefix("@")


def validate_trip(trip: str) -> str | None:
    if trip == "" or trip == "null":
        return None
    return trip
