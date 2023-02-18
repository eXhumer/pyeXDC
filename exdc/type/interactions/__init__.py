from __future__ import annotations
from enum import IntEnum
from typing import NotRequired, TypedDict, TYPE_CHECKING

if TYPE_CHECKING:
    from .application_command import ApplicationCommandOptionChoice, \
        ApplicationCommandOptionType, ApplicationCommandType
    from .message_component import ActionRowComponent
    from ..channel import AllowedMentions, Attachment, Channel, Embed, Message, MessageFlag
    from ..guild import GuildMember
    from ..permissions import Role
    from ..user import User


class ApplicationCommandData(TypedDict):
    id: str
    name: str
    type: "ApplicationCommandType"
    resolved: NotRequired[ResolvedData]
    options: NotRequired[list[ApplicationCommandInteractionDataOption]]
    guild_id: NotRequired[str]
    target_id: NotRequired[str]


class ApplicationCommandInteractionDataOption(TypedDict):
    name: str
    type: "ApplicationCommandOptionType"
    value: NotRequired[str | int | float | bool]
    options: NotRequired[list[ApplicationCommandInteractionDataOption]]
    focused: NotRequired[bool]


class Interaction(TypedDict):
    id: str
    application_id: str
    type: InteractionType
    data: NotRequired[ApplicationCommandData]
    guild_id: NotRequired[str]
    channel_id: NotRequired[str]
    member: NotRequired["GuildMember"]
    user: NotRequired["User"]
    token: str
    version: int
    message: NotRequired["Message"]
    app_permissions: NotRequired[str]
    locale: NotRequired[str]
    guild_locale: NotRequired[str]


class InteractionResponseAutocomplete(TypedDict):
    choices: list["ApplicationCommandOptionChoice"]


class InteractionResponseMessage(TypedDict):
    tts: NotRequired[bool]
    content: NotRequired[str]
    embeds: NotRequired[list["Embed"]]
    allowed_mentions: NotRequired["AllowedMentions"]
    flags: NotRequired["MessageFlag"]
    components: NotRequired[list["ActionRowComponent"]]
    attachments: NotRequired[list["Attachment"]]


class InteractionResponseModal(TypedDict):
    custom_id: str
    title: str
    components: list["ActionRowComponent"]


class InteractionResponse(TypedDict):
    type: InteractionResponseType
    data: NotRequired[InteractionResponseMessage | InteractionResponseAutocomplete |
                      InteractionResponseModal]


class InteractionResponseType(IntEnum):
    PONG = 1
    CHANNEL_MESSAGE_WITH_SOURCE = 4
    DEFERRED_CHANNEL_MESSAGE_WITH_SOURCE = 5
    DEFERRED_UPDATE_MESSAGE = 6
    UPDATE_MESSAGE = 7
    APPLICATION_COMMAND_AUTOCOMPLETE_RESULT = 8
    MODAL = 9


class InteractionType(IntEnum):
    PING = 1
    APPLICATION_COMMAND = 2
    MESSAGE_COMPONENT = 3
    APPLICATION_COMMAND_AUTOCOMPLETE = 4
    MODAL_SUBMIT = 5


class MessageInteraction(TypedDict):
    id: str
    type: InteractionType
    name: str
    user: "User"
    member: NotRequired["GuildMember"]


class ResolvedData(TypedDict):
    users: NotRequired[dict[str, "User"]]
    members: NotRequired[dict[str, "GuildMember"]]
    roles: NotRequired[dict[str, "Role"]]
    channels: NotRequired[dict[str, "Channel"]]
    messages: NotRequired[dict[str, "Message"]]
    attachments: NotRequired[dict[str, "Attachment"]]
