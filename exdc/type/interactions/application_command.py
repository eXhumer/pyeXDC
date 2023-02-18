from __future__ import annotations
from enum import IntEnum
from typing import NotRequired, TypedDict, TYPE_CHECKING

if TYPE_CHECKING:
    from ..channel import ChannelType


class ApplicationCommand(TypedDict):
    id: str
    type: NotRequired[ApplicationCommandType]
    application_id: str
    guild_id: NotRequired[str]
    name: str
    name_localizations: NotRequired[dict[str, str] | None]
    description: str
    description_localizations: NotRequired[dict[str, str] | None]
    options: NotRequired[list[ApplicationCommandOption]]
    default_member_permissions: str | None
    dm_permission: NotRequired[bool]
    default_permission: NotRequired[bool | None]
    nsfw: NotRequired[bool]
    version: str


class ApplicationCommandOption(TypedDict):
    type: ApplicationCommandOptionType
    name: str
    name_localizations: NotRequired[dict[str, str] | None]
    description: str
    description_localizations: NotRequired[dict[str, str] | None]
    required: NotRequired[bool]
    choices: NotRequired[list[ApplicationCommandOptionChoice]]
    options: NotRequired[list[ApplicationCommandOption]]
    channel_types: NotRequired[list["ChannelType"]]
    min_value: NotRequired[int | float]
    max_value: NotRequired[int | float]
    min_length: NotRequired[int]
    max_length: NotRequired[int]
    autocomplete: NotRequired[bool]


class ApplicationCommandOptionChoice(TypedDict):
    name: str
    name_localizations: NotRequired[dict[str, str] | None]
    value: str | int | float


class ApplicationCommandOptionType(IntEnum):
    SUB_COMMAND = 1
    SUB_COMMAND_GROUP = 2
    STRING = 3
    INTEGER = 4
    BOOLEAN = 5
    USER = 6
    CHANNEL = 7
    ROLE = 8
    MENTIONABLE = 9
    NUMBER = 10
    ATTACHMENT = 11


class ApplicationCommandPermissions(TypedDict):
    id: str
    type: ApplicationCommandPermissionType
    permission: bool


class ApplicationCommandPermissionType(IntEnum):
    ROLE = 1
    USER = 2
    CHANNEL = 3


class ApplicationCommandType(IntEnum):
    CHAT_INPUT = 1
    USER = 2
    MESSAGE = 3


class ApplicationGuildCommandOptionPermissions(TypedDict):
    id: str
    application_id: str
    guild_id: str
    permissions: list[ApplicationCommandPermissions]
