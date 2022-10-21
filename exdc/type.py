# eXDC - Discord client
# Copyright (C) 2022  eXhumer

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, version 3 of the
# License.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from __future__ import annotations
from datetime import datetime
from enum import IntEnum, IntFlag, StrEnum
from typing import IO, List, Literal, NotRequired, Tuple, TypedDict


class AllowedMention(TypedDict):
    parse: List[AllowedMentionType]
    roles: List[Snowflake | str | int]
    users: List[Snowflake | str | int]
    replied_user: bool


class AllowedMentionType(StrEnum):
    ROLES = "roles"
    USERS = "users"
    EVERYONE = "everyone"


class Attachment(TypedDict):
    id: str
    filename: NotRequired[str]
    description: NotRequired[str]
    content_type: NotRequired[str]
    size: NotRequired[int]
    url: NotRequired[str]
    proxy_url: NotRequired[str]
    height: NotRequired[int | None]
    width: NotRequired[int | None]
    ephemeral: NotRequired[bool]


class ComponentType(IntEnum):
    ACTION_ROW = 1
    BUTTON = 2
    SELECT_MENU = 3
    TEXT_INPUT = 4


class ComponentActionRow(TypedDict):
    type: Literal[ComponentType.ACTION_ROW]
    components: List[ComponentButton, ComponentSelectMenu, ComponentTextInput]


class ComponentButtonStyle(IntEnum):
    PRIMARY = 1
    SECONDARY = 2
    SUCCESS = 3
    DANGER = 4
    LINK = 5


class ComponentButton(TypedDict):
    type: Literal[ComponentType.BUTTON]
    style: ComponentButtonStyle
    label: NotRequired[str]
    emoji: NotRequired[Emoji]
    custom_id: NotRequired[str]
    url: NotRequired[str]
    disabled: NotRequired[bool]


class ComponentSelectMenu(TypedDict):
    type: Literal[ComponentType.SELECT_MENU]
    custom_id: str
    options: List[ComponentSelectMenuOption]
    placeholder: NotRequired[str]
    min_values: NotRequired[int]
    max_values: NotRequired[int]
    disabled: NotRequired[bool]


class ComponentSelectMenuOption(TypedDict):
    label: str
    value: str
    description: NotRequired[str]
    emoji: NotRequired[Emoji]
    default: NotRequired[bool]


class ComponentTextInput(TypedDict):
    type: Literal[ComponentType.SELECT_MENU]
    custom_id: str
    style: ComponentTextInputStyle
    label: str
    min_length: NotRequired[int]
    max_length: NotRequired[int]
    required: NotRequired[bool]
    value: NotRequired[str]
    placeholder: NotRequired[str]


class ComponentTextInputStyle(IntEnum):
    SHORT = 1
    PARAGRAPH = 2


class Embed(TypedDict):
    title: NotRequired[str]
    type: NotRequired[EmbedType]
    description: NotRequired[str]
    url: NotRequired[str]
    timestamp: NotRequired[str]
    color: NotRequired[int]
    footer: NotRequired[EmbedFooter]
    image: NotRequired[EmbedImage | Tuple[IO[bytes], str]]
    thumbnail: NotRequired[EmbedThumbnail | Tuple[IO[bytes], str]]
    video: NotRequired[EmbedVideo | Tuple[IO[bytes], str]]
    provider: NotRequired[EmbedProvider]
    author: NotRequired[EmbedAuthor]
    fields: NotRequired[List[EmbedField]]


class EmbedAuthor(TypedDict):
    name: str
    url: NotRequired[str]
    icon_url: NotRequired[str | Tuple[IO[bytes], str]]
    proxy_icon_url: NotRequired[str]


class EmbedField(TypedDict):
    name: str
    value: str
    inline: NotRequired[bool]


class EmbedFooter(TypedDict):
    text: str
    icon_url: NotRequired[str | Tuple[IO[bytes], str]]
    proxy_icon_url: NotRequired[str]


class EmbedImage(TypedDict):
    url: str
    proxy_url: NotRequired[str]
    height: NotRequired[int]
    width: NotRequired[int]


class EmbedProvider(TypedDict):
    name: NotRequired[str]
    url: NotRequired[str]


class EmbedThumbnail(TypedDict):
    url: str
    proxy_url: NotRequired[str]
    height: NotRequired[int]
    width: NotRequired[int]


class EmbedType(StrEnum):
    RICH = "rich"
    IMAGE = "image"
    VIDEO = "video"
    GIFV = "gifv"
    ARTICLE = "article"
    LINK = "link"


class EmbedVideo(TypedDict):
    url: str
    proxy_url: NotRequired[str]
    height: NotRequired[int]
    width: NotRequired[int]


class Emoji(TypedDict):
    id: Snowflake | str | int | None
    name: str | None
    roles: NotRequired[List[Snowflake | str | int]]
    user: NotRequired[User]
    require_colons: NotRequired[bool]
    managed: NotRequired[bool]
    animated: NotRequired[bool]
    available: NotRequired[bool]


class MessageFlag(IntFlag):
    CROSSPOSTED = 1 << 0
    IS_CROSSPOST = 1 << 1
    SUPPRESS_EMBEDS = 1 << 2
    SOURCE_MESSAGE_DELETED = 1 << 3
    URGENT = 1 << 4
    HAS_THREAD = 1 << 5
    EPHEMERAL = 1 << 6
    LOADING = 1 << 7
    FAILED_TO_MENTION_SOME_ROLES_IN_THREAD = 1 << 8


class MessagePayload(TypedDict):
    content: NotRequired[str]
    nonce: NotRequired[int | str]
    tts: NotRequired[bool]
    embeds: NotRequired[List[Embed]]
    allowed_mentions: NotRequired[AllowedMention]
    message_reference: NotRequired[MessageReference]
    components: NotRequired[List[ComponentActionRow]]
    sticker_ids: NotRequired[List[str]]
    payload_json: NotRequired[str]
    attachments: NotRequired[List[Attachment]]
    flags: NotRequired[MessageFlag]


class MessageReference(TypedDict):
    message_id: NotRequired[Snowflake | str | int]
    channel_id: NotRequired[Snowflake | str | int]
    guild_id: NotRequired[Snowflake | str | int]
    fail_if_not_exists: NotRequired[bool]


class Snowflake:
    def __init__(self, value: int | str):
        assert int(value) <= (1 << 64) - 1, "Value too big!"
        self.__value = int(value)

    def __repr__(self):
        __data = ", ".join((
            f"value={self.__value}",
            f"timestamp={self.timestamp}",
            f"internal_process_id={self.internal_process_id}",
            f"internal_worker_id={self.internal_worker_id}",
            f"increment={self.increment}",
        ))

        return f"{type(self).__name__}({__data})"

    def __str__(self):
        return str(self.__value)

    @property
    def __discord_epoch_timestamp_ms(self):
        return self.__value >> 22

    @property
    def __epoch_timestamp_ms(self):
        return self.__discord_epoch_timestamp_ms + 0x14AA2CAB000

    @property
    def increment(self):
        return self.__value & 0xFFF

    @property
    def internal_process_id(self):
        return (self.__value & 0x1F000) >> 12

    @property
    def internal_worker_id(self):
        return (self.__value & 0x3E0000) >> 17

    @property
    def timestamp(self):
        return datetime.fromtimestamp(self.__epoch_timestamp_ms / 1000)


class User(TypedDict):
    id: Snowflake | str | int
    username: str
    discriminator: str
    avatar: str | None
    bot: NotRequired[bool]
    system: NotRequired[bool]
    mfa_enabled: NotRequired[bool]
    banner: NotRequired[str | None]
    accent_color: NotRequired[int | None]
    locale: NotRequired[str]
    verified: NotRequired[bool]
    email: NotRequired[str | None]
    flags: NotRequired[UserFlag]
    premium_type: NotRequired[UserPremiumType]
    public_flags: NotRequired[UserFlag]


class UserFlag(IntFlag):
    STAFF = 1 << 0
    PARTNER = 1 << 1
    HYPESQUAD = 1 << 2
    BUG_HUNTER_LEVEL_1 = 1 << 3
    HYPESQUAD_ONLINE_HOUSE_1 = 1 << 6
    HYPESQUAD_ONLINE_HOUSE_2 = 1 << 7
    HYPESQUAD_ONLINE_HOUSE_3 = 1 << 8
    PREMIUM_EARLY_SUPPORTER = 1 << 9
    TEAM_PSEUDO_USER = 1 << 10
    BUG_HUNTER_LEVEL_2 = 1 << 14
    VERIFIED_BOT = 1 << 16
    VERIFIED_DEVELOPER = 1 << 17
    CERTIFIED_MODERATOR = 1 << 18
    BOT_HTTP_INTERACTIONS = 1 << 19


class UserPremiumType(IntEnum):
    NONE = 0
    NITRO_CLASSIC = 1
    NITRO = 2
