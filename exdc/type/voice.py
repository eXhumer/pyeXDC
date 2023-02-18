from __future__ import annotations
from typing import NotRequired, TypedDict, TYPE_CHECKING

if TYPE_CHECKING:
    from .guild import GuildMember


class VoiceRegion(TypedDict):
    id: str
    name: str
    optimal: bool
    deprecated: bool
    custom: bool


class VoiceState(TypedDict):
    guild_id: NotRequired[str]
    channel_id: str | None
    user_id: str
    member: NotRequired["GuildMember"]
    session_id: str
    deaf: bool
    mute: bool
    self_deaf: bool
    self_mute: bool
    self_stream: NotRequired[bool]
    self_video: bool
    suppress: bool
    request_to_speak_timestamp: str | None
