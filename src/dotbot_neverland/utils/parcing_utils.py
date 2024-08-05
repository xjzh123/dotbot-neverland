import re

validate_nick_regex = re.compile(r"^[a-zA-Z0-9_]{1,24}$")


def validate_nick(nick: str):
    return bool(validate_nick_regex.fullmatch(nick))


parse_whisper_regex = re.compile(r"(?:You whispered to @.*?: |(.*?) whispered: )(.*)")


def parse_whisper(text: str) -> tuple[str | None, str] | None:
    match = parse_whisper_regex.fullmatch(text)
    if match:
        return match.groups()  # type: ignore

    return None


parse_emote_regex = re.compile(r"(@.*? )(.*)")


def parse_emote(text: str) -> tuple[str, str] | None:
    match = parse_emote_regex.fullmatch(text)
    if match:
        return match.groups()  # type: ignore

    return None


parse_changenick_regex = re.compile(r"(.*) is now (.*)")


def parse_changenick(text: str) -> tuple[str, str] | None:
    match = parse_changenick_regex.match(text)
    if match:
        return match.groups()  # type: ignore

    return None
