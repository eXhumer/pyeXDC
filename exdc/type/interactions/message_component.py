from __future__ import annotations
from enum import IntEnum
from typing import Literal, NotRequired, TypedDict, TYPE_CHECKING

if TYPE_CHECKING:
    from ..channel import ChannelType
    from ..emoji import Emoji


class ComponentType(IntEnum):
    ACTION_ROW = 1
    BUTTON = 2
    STRING_SELECT = 3
    TEXT_INPUT = 4
    USER_SELECT = 5
    ROLE_SELECT = 6
    MENTIONABLE_SELECT = 7
    CHANNEL_SELECT = 8


class ActionRowComponent(TypedDict):
    type: Literal[ComponentType.ACTION_ROW]
    components: list[ButtonComponent | SelectMenuComponent | TextInputComponent]


class ButtonComponent(TypedDict):
    type: Literal[ComponentType.BUTTON]
    style: ButtonStyle
    label: NotRequired[str]
    emoji: NotRequired[Emoji]
    custom_id: NotRequired[str]
    url: NotRequired[str]
    disabled: NotRequired[bool]


class ButtonStyle(IntEnum):
    PRIMARY = 1
    SECONDARY = 2
    SUCCESS = 3
    DANGER = 4
    LINK = 5


class SelectMenuComponent(TypedDict):
    type: ComponentType
    custom_id: str
    options: NotRequired[list[SelectOption]]
    channel_types: NotRequired[list[ChannelType]]
    placeholder: NotRequired[str]
    min_values: NotRequired[int]
    max_values: NotRequired[int]
    disabled: NotRequired[bool]


class SelectOption(TypedDict):
    label: str
    value: str
    description: NotRequired[str]
    emoji: NotRequired[Emoji]
    default: NotRequired[bool]


class TextInputComponent(TypedDict):
    type: Literal[ComponentType.TEXT_INPUT]
    custom_id: str
    style: TextInputStyle
    label: str
    min_length: NotRequired[int]
    max_length: NotRequired[int]
    required: NotRequired[bool]
    value: NotRequired[str]
    placeholder: NotRequired[str]


class TextInputStyle(IntEnum):
    SHORT = 1
    PARAGRAPH = 2
