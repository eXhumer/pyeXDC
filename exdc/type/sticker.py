from __future__ import annotations
from enum import IntEnum
from typing import NotRequired, TypedDict, TYPE_CHECKING

if TYPE_CHECKING:
    from .user import User


class Sticker(TypedDict):
    id: str
    pack_id: NotRequired[str]
    name: str
    description: str | None
    tags: str
    asset: NotRequired[str]
    type: StickerType
    format_type: StickerFormatType
    available: NotRequired[bool]
    guild_id: NotRequired[str]
    user: NotRequired[User]
    sort_value: NotRequired[int]


class StickerItem(TypedDict):
    id: str
    name: str
    format_type: StickerFormatType


class StickerFormatType(IntEnum):
    PNG = 1
    APNG = 2
    LOTTIE = 3
    GIF = 4


class StickerPack(TypedDict):
    id: str
    stickers: list[Sticker]
    name: str
    sku_id: str
    cover_sticker_id: NotRequired[str]
    description: str
    banner_asset_id: NotRequired[str]


class StickerType(IntEnum):
    STANDARD = 1
    GUILD = 2
