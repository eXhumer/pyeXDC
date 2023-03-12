from __future__ import annotations
from enum import IntEnum, IntFlag, StrEnum
from typing import Any, Literal, NotRequired, TypedDict, TYPE_CHECKING

from .channel import Message

if TYPE_CHECKING:
    from .application import Application
    from .guild import GuildMember, UnavailableGuild
    from .user import User


class Operation(IntEnum):
    DISPATCH = 0
    HEARTBEAT = 1
    IDENTIFY = 2
    PRESENCE_UPDATE = 3
    VOICE_STATE_UPDATE = 4
    RESUME = 6
    RECONNECT = 7
    REQUEST_QUILD_MEMBERS = 8
    INVALID_SESSION = 9
    HELLO = 10
    HEARTBEAT_ACK = 11


class ReceiveEventPayload(TypedDict):
    op: Operation
    d: int | HelloData | None
    s: int | None
    t: ReceiveEvent | None


class DispatchPayload(ReceiveEventPayload):
    op: Literal[Operation.DISPATCH]
    d: Any | None
    s: None
    t: ReceiveEvent


class HeartbeatPayload(ReceiveEventPayload):
    op: Literal[Operation.HEARTBEAT]
    d: int
    s: None
    t: None


class HelloData(TypedDict):
    heartbeat_interval: int


class HelloPayload(ReceiveEventPayload):
    op: Literal[Operation.HELLO]
    d: HelloData


class GetGatewayResponse(TypedDict):
    url: str


class IdentifyData(TypedDict):
    token: str
    properties: IdentifyProperties
    compress: NotRequired[bool]
    large_threshold: NotRequired[int]
    shard: NotRequired[list[int]]
    presence: NotRequired[PresenceUpdateData]
    intents: Intent


class IdentifyPayload(ReceiveEventPayload):
    op: Literal[Operation.IDENTIFY]
    d: IdentifyData
    s: None
    t: None


class IdentifyProperties(TypedDict):
    os: str
    browser: str
    device: str


class Intent(IntFlag):
    GUILDS = 1 << 0
    GUILD_MEMBERS = 1 << 1
    GUILD_MODERATION = 1 << 2
    GUILD_EMOJIS_AND_STICKERS = 1 << 3
    GUILD_INTEGRATIONS = 1 << 4
    GUILD_WEBHOOKS = 1 << 5
    GUILD_INVITES = 1 << 6
    GUILD_VOICE_STATES = 1 << 7
    GUILD_PRESENCES = 1 << 8
    GUILD_MESSAGES = 1 << 9
    GUILD_MESSAGE_REACTIONS = 1 << 10
    GUILD_MESSAGE_TYPING = 1 << 11
    DIRECT_MESSAGES = 1 << 12
    DIRECT_MESSAGE_REACTIONS = 1 << 13
    DIRECT_MESSAGE_TYPING = 1 << 14
    MESSAGE_CONTENT = 1 << 15
    GUILD_SCHEDULED_EVENTS = 1 << 16
    AUTO_MODERATION_CONFIGURATION = 1 << 20
    AUTO_MODERATION_EXECUTION = 1 << 21


class MessageCreate(Message):
    guild_id: NotRequired[str]
    member: NotRequired[GuildMember]
    mentions: list[User]


class MessageDelete(TypedDict):
    id: str
    channel_id: str
    guild_id: NotRequired[str]


class PresenceActivity(TypedDict):
    name: str
    type: PresenceActivityType
    url: NotRequired[str | None]
    created_at: int
    timestamps: NotRequired[PresenceActivityTimestamps]
    application_id: NotRequired[str]
    details: NotRequired[str | None]
    state: NotRequired[str | None]
    emoji: NotRequired[PresenceActivityEmoji | None]
    party: NotRequired[PresenceActivityParty]
    assets: NotRequired[PresenceActivityAssets]
    secrets: NotRequired[PresenceActivitySecrets]
    instance: NotRequired[bool]
    flags: NotRequired[PresenceActivityFlag]


class PresenceActivityAssets(TypedDict):
    large_image: NotRequired[str]
    large_text: NotRequired[str]
    small_image: NotRequired[str]
    small_text: NotRequired[str]


class PresenceActivityEmoji(TypedDict):
    name: str
    id: NotRequired[str]
    animated: NotRequired[bool]


class PresenceActivityFlag(IntFlag):
    INSTANCE = 1 << 0
    JOIN = 1 << 1
    SPECTATE = 1 << 2
    JOIN_REQUEST = 1 << 3
    SYNC = 1 << 4
    PLAY = 1 << 5
    PARTY_PRIVACY_FRIENDS = 1 << 6
    PARTY_PRIVACY_VOICE_CHANNEL = 1 << 7
    EMBEDDED = 1 << 8


class PresenceActivityParty(TypedDict):
    id: NotRequired[str]
    size: NotRequired[list[int]]


class PresenceActivitySecrets(TypedDict):
    join: NotRequired[str]
    spectate: NotRequired[str]
    match: NotRequired[str]


class PresenceActivityTimestamps(TypedDict):
    start: NotRequired[int]
    end: NotRequired[int]


class PresenceActivityType(IntEnum):
    GAME = 0
    STREAMING = 1
    LISTENING = 2
    WATCHING = 3
    CUSTOM = 4
    COMPETING = 5


class PresenceStatus(StrEnum):
    ONLINE = "online"
    DND = "dnd"
    IDLE = "idle"
    INVISIBLE = "invisible"
    OFFLINE = "offline"


class PresenceUpdateData(TypedDict):
    since: int | None
    activities: list[PresenceActivity]
    status: PresenceStatus
    afk: bool


class PresenceUpdatePayload(ReceiveEventPayload):
    op: Literal[Operation.PRESENCE_UPDATE]
    d: PresenceUpdateData
    s: None
    t: None


class ReadyEventData(TypedDict):
    v: int
    user: User
    guilds: list[UnavailableGuild]
    session_id: str
    resume_gateway_url: str
    shard: NotRequired[list[int]]
    application: Application


class ReceiveEvent(StrEnum):
    HELLO = "HELLO"
    READY = "READY"
    RESUMED = "RESUMED"
    RECONNECT = "RECONNECT"
    INVALID_SESSION = "INVALID_SESSION"
    APPLICATION_COMMAND_PERMISSIONS_UPDATE = "APPLICATION_COMMAND_PERMISSIONS_UPDATE"
    AUTO_MODERATION_RULE_CREATE = "AUTO_MODERATION_RULE_CREATE"
    AUTO_MODERATION_RULE_UPDATE = "AUTO_MODERATION_RULE_UPDATE"
    AUTO_MODERATION_RULE_DELETE = "AUTO_MODERATION_RULE_DELETE"
    AUTO_MODERATION_ACTION_EXECUTION = "AUTO_MODERATION_ACTION_EXECUTION"
    CHANNEL_CREATE = "CHANNEL_CREATE"
    CHANNEL_UPDATE = "CHANNEL_UPDATE"
    CHANNEL_DELETE = "CHANNEL_DELETE"
    CHANNEL_PINS_UPDATE = "CHANNEL_PINS_UPDATE"
    THREAD_CREATE = "THREAD_CREATE"
    THREAD_UPDATE = "THREAD_UPDATE"
    THREAD_DELETE = "THREAD_DELETE"
    THREAD_LIST_SYNC = "THREAD_LIST_SYNC"
    THREAD_MEMBER_UPDATE = "THREAD_MEMBER_UPDATE"
    THREAD_MEMBERS_UPDATE = "THREAD_MEMBERS_UPDATE"
    GUILD_CREATE = "GUILD_CREATE"
    GUILD_UPDATE = "GUILD_UPDATE"
    GUILD_DELETE = "GUILD_DELETE"
    GUILD_AUDIT_LOG_ENTRY_CREATE = "GUILD_AUDIT_LOG_ENTRY_CREATE"
    GUILD_BAN_ADD = "GUILD_BAN_ADD"
    GUILD_BAN_REMOVE = "GUILD_BAN_REMOVE"
    GUILD_EMOJIS_UPDATE = "GUILD_EMOJIS_UPDATE"
    GUILD_STICKERS_UPDATE = "GUILD_STICKERS_UPDATE"
    GUILD_INTEGRATIONS_UPDATE = "GUILD_INTEGRATIONS_UPDATE"
    GUILD_MEMBER_ADD = "GUILD_MEMBER_ADD"
    GUILD_MEMBER_REMOVE = "GUILD_MEMBER_REMOVE"
    GUILD_MEMBER_UPDATE = "GUILD_MEMBER_UPDATE"
    GUILD_MEMBERS_CHUNK = "GUILD_MEMBERS_CHUNK"
    GUILD_ROLE_CREATE = "GUILD_ROLE_CREATE"
    GUILD_ROLE_UPDATE = "GUILD_ROLE_UPDATE"
    GUILD_ROLE_DELETE = "GUILD_ROLE_DELETE"
    GUILD_SCHEDULED_EVENT_CREATE = "GUILD_SCHEDULED_EVENT_CREATE"
    GUILD_SCHEDULED_EVENT_UPDATE = "GUILD_SCHEDULED_EVENT_UPDATE"
    GUILD_SCHEDULED_EVENT_DELETE = "GUILD_SCHEDULED_EVENT_DELETE"
    GUILD_SCHEDULED_EVENT_USER_ADD = "GUILD_SCHEDULED_EVENT_USER_ADD"
    GUILD_SCHEDULED_EVENT_USER_REMOVE = "GUILD_SCHEDULED_EVENT_USER_REMOVE"
    INTEGRATION_CREATE = "INTEGRATION_CREATE"
    INTEGRATION_UPDATE = "INTEGRATION_UPDATE"
    INTEGRATION_DELETE = "INTEGRATION_DELETE"
    INTERACTION_CREATE = "INTERACTION_CREATE"
    INVITE_CREATE = "INVITE_CREATE"
    INVITE_DELETE = "INVITE_DELETE"
    MESSAGE_CREATE = "MESSAGE_CREATE"
    MESSAGE_UPDATE = "MESSAGE_UPDATE"
    MESSAGE_DELETE = "MESSAGE_DELETE"
    MESSAGE_DELETE_BULK = "MESSAGE_DELETE_BULK"
    MESSAGE_REACTION_ADD = "MESSAGE_REACTION_ADD"
    MESSAGE_REACTION_REMOVE = "MESSAGE_REACTION_REMOVE"
    MESSAGE_REACTION_REMOVE_ALL = "MESSAGE_REACTION_REMOVE_ALL"
    MESSAGE_REACTION_REMOVE_EMOJI = "MESSAGE_REACTION_REMOVE_EMOJI"
    PRESENCE_UPDATE = "PRESENCE_UPDATE"
    STAGE_INSTANCE_CREATE = "STAGE_INSTANCE_CREATE"
    STAGE_INSTANCE_UPDATE = "STAGE_INSTANCE_UPDATE"
    STAGE_INSTANCE_DELETE = "STAGE_INSTANCE_DELETE"
    TYPING_START = "TYPING_START"
    USER_UPDATE = "USER_UPDATE"
    VOICE_STATE_UPDATE = "VOICE_STATE_UPDATE"
    VOICE_SERVER_UPDATE = "VOICE_SERVER_UPDATE"
    WEBHOOKS_UPDATE = "WEBHOOKS_UPDATE"


class ResumeData(TypedDict):
    token: str
    session_id: str
    seq: int


class ResumePayload(ReceiveEventPayload):
    op: Literal[Operation.RESUME]
    d: ResumeData
    s: None
    t: None


class SendEvent(StrEnum):
    IDENTIFY = "IDENTIFY"
    RESUME = "RESUME"
    HEARTBEAT = "HEARTBEAT"
    REQUEST_GUILD_MEMBERS = "REQUEST_GUILD_MEMBERS"
    UPDATE_VOICE_STATE = "UPDATE_VOICE_STATE"
    UPDATE_PRESENCE = "UPDATE_PRESENCE"
