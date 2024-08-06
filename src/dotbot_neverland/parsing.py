# pyright: reportTypedDictNotRequiredAccess = false

from typing import Union

from .models import *
from .utils.parcing_utils import parse_changenick, parse_emote, parse_whisper
from .utils.validators import validate_trip


def parse(
    _data: EventRawData,
) -> Union[
    None,
    Event,
    InfoEvent,
    ChatEvent,
    EmoteEvent,
    WarnEvent,
    BotJoinEvent,
    CaptchaEvent,
    UserJoinEvent,
    UserLeaveEvent,
    UpdateUserEvent,
    WhisperEvent,
    InviteEvent,
    ChangeNickEvent,
]:
    data = _data.copy()

    if "cmd" not in data:
        return None

    match data["cmd"]:
        case "chat":
            data["trip"] = validate_trip(data["trip"])  # type: ignore
            return ChatEvent.parse(data)

        case "warn":
            return WarnEvent.parse(data)

        case "onlineAdd":
            return UserJoinEvent.parse(data, user=User.parse(data))

        case "onlineRemove":
            return UserLeaveEvent.parse(data)

        case "updateUser":
            return UpdateUserEvent.parse(data)

        case "onlineSet":
            users = [User.parse(user) for user in data["users"]]
            data["users"] = users  # type: ignore
            return BotJoinEvent.parse(data)

        case "captcha":
            return CaptchaEvent.parse(data)

        case "info":
            text_raw = data["text"]

            if "type" not in data:
                return InfoEvent.parse(data, text_raw=text_raw)

            match data["type"]:
                case "whisper":
                    if isinstance(data["from"], int):
                        # Feedback event, not handled by DotBot-NL
                        return None
                    groups = parse_whisper(text_raw)
                    if groups:
                        data["nick"] = data["from"]
                        data["text"] = groups[1]
                        data["trip"] = validate_trip(data["trip"])  # type: ignore
                        return WhisperEvent.parse(data, text_raw=text_raw)
                    else:
                        raise ValueError(
                            f"Failed to parse whisper message: {text_raw!r}"
                        )

                case "emote":
                    groups = parse_emote(text_raw)
                    if groups:
                        (nick, text) = groups
                        data["nick"] = nick
                        data["text"] = text
                        data["trip"] = validate_trip(data["trip"])  # type: ignore
                        return EmoteEvent.parse(data, text_raw=text_raw)
                    else:
                        raise ValueError(f"Failed to parse emote message: {text_raw!r}")

                case "invite":
                    if not data["from"]:
                        # Feedback event, not handled by DotBot-NL
                        return None
                    return InviteEvent.parse(
                        data, nick=data["from"], channel=data["inviteChannel"]
                    )

                case _:
                    groups = parse_changenick(text_raw)
                    if groups:
                        return ChangeNickEvent.parse(
                            data,
                            old_nick=groups[0],
                            new_nick=groups[1],
                            text_raw=text_raw,
                        )

                    return InfoEvent.parse(data, text_raw=text_raw)

        case _:
            return None
