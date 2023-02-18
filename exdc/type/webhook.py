from __future__ import annotations
from enum import IntEnum
from typing import NotRequired, TypedDict, TYPE_CHECKING

if TYPE_CHECKING:
    from .channel import Channel
    from .guild import Guild
    from .user import User


class Webhook(TypedDict):
    id: str
    type: WebhookType
    guild_id: NotRequired[str | None]
    channel_id: str | None
    user: NotRequired["User"]
    name: str | None
    avatar: str | None
    token: NotRequired[str]
    application_id: str | None
    source_guild: NotRequired["Guild"]
    source_channel: NotRequired["Channel"]
    url: NotRequired[str]


class WebhookType(IntEnum):
    INCOMING = 1
    CHANNEL_FOLLOWER = 2
    APPLICATION = 3
