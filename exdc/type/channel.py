from __future__ import annotations
from enum import IntEnum, IntFlag, StrEnum
from typing import NotRequired, TypedDict, TYPE_CHECKING

if TYPE_CHECKING:
    from .application import Application
    from .emoji import Emoji
    from .guild import GuildMember
    from .interactions import MessageInteraction
    from .interactions.message_component import ActionRowComponent
    from .sticker import Sticker, StickerItem
    from .user import User


class AllowedMentions(TypedDict):
    parse: list[AlloweMentionType]
    roles: list[str]
    users: list[str]
    replied_user: bool


class AlloweMentionType(StrEnum):
    ROLES = "roles"
    USERS = "users"
    EVERYONE = "everyone"


class Attachment(TypedDict):
    id: str
    filename: str
    description: NotRequired[str]
    content_type: NotRequired[str]
    size: int
    url: str
    proxy_url: str
    height: NotRequired[int | None]
    width: NotRequired[int | None]
    ephemeral: NotRequired[bool]


class Channel(TypedDict):
    id: str
    type: ChannelType
    guild_id: NotRequired[str]
    position: NotRequired[int]
    permission_overwrites: NotRequired[list[Overwrite]]
    name: NotRequired[str | None]
    topic: NotRequired[str | None]
    nsfw: NotRequired[bool]
    last_message_id: NotRequired[str | None]
    bitrate: NotRequired[int]
    user_limit: NotRequired[int]
    rate_limit_per_user: NotRequired[int]
    recipients: NotRequired[list["User"]]
    icon: NotRequired[str | None]
    owner_id: NotRequired[str]
    application_id: NotRequired[str]
    managed: NotRequired[bool]
    parent_id: NotRequired[str | None]
    last_pin_timestamp: NotRequired[str | None]
    rtc_region: NotRequired[str | None]
    video_quality_mode: NotRequired[VideoQualityMode]
    message_count: NotRequired[int]
    member_count: NotRequired[int]
    thread_metadata: NotRequired[ThreadMetadata]
    member: NotRequired[ThreadMember]
    default_auto_archive_duration: NotRequired[int]
    permissions: NotRequired[str]
    flags: NotRequired[ChannelFlag]
    total_message_sent: NotRequired[int]
    available_tags: NotRequired[list[ForumTag]]
    applied_tags: NotRequired[list[str]]
    default_reaction_emoji: NotRequired[DefaultReaction | None]
    default_thread_rate_limit_per_user: NotRequired[int]
    default_sort_order: NotRequired[SortOrder | None]
    default_forum_layout: NotRequired[ForumLayout]


class ChannelFlag(IntFlag):
    PINNED = 1 << 1
    REQUIRE_TAG = 1 << 4


class ChannelMention(TypedDict):
    id: str
    guild_id: str
    type: ChannelType
    name: str


class ChannelType(IntEnum):
    GUILD_TEXT = 0
    DM = 1
    GUILD_VOICE = 2
    GROUP_DM = 3
    GUILD_CATEGORY = 4
    GUILD_ANNOUNCEMENT = 5
    ANNOUNCEMENT_THREAD = 10
    PUBLIC_THREAD = 11
    PRIVATE_THREAD = 12
    GUILD_STAGE_VOICE = 13
    GUILD_DIRECTORY = 14
    GUILD_FORUM = 15


class DefaultReaction(TypedDict):
    emoji_id: str | None
    emoji_name: str | None


class Embed(TypedDict):
    title: NotRequired[str]
    type: NotRequired[EmbedType]
    description: NotRequired[str]
    url: NotRequired[str]
    timestamp: NotRequired[str]
    color: NotRequired[int]
    footer: NotRequired[EmbedFooter]
    image: NotRequired[EmbedImage]
    thumbnail: NotRequired[EmbedThumbnail]
    video: NotRequired[EmbedVideo]
    provider: NotRequired[EmbedProvider]
    author: NotRequired[EmbedAuthor]
    fields: NotRequired[list[EmbedField]]


class EmbedAuthor(TypedDict):
    name: str
    url: NotRequired[str]
    icon_url: NotRequired[str]
    proxy_icon_url: NotRequired[str]


class EmbedField(TypedDict):
    name: str
    value: str
    inline: NotRequired[bool]


class EmbedFooter(TypedDict):
    text: str
    icon_url: NotRequired[str]
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


class FollowedChannel(TypedDict):
    channel_id: str
    webhook_id: str


class ForumLayout(IntEnum):
    NOT_SET = 0
    LIST_VIEW = 1
    GALLERY_VIEW = 2


class ForumTag(TypedDict):
    id: str
    name: str
    moderated: bool
    emoji_id: str | None
    emoji_name: str | None


class Message(TypedDict):
    id: str
    channel_id: str
    author: User
    content: str
    timestamp: str
    edited_timestamp: str | None
    tts: bool
    mention_everyone: bool
    mentions: list[User]
    mention_roles: list[str]
    mention_channels: NotRequired[list[ChannelMention]]
    attachments: list[Attachment]
    embeds: list[Embed]
    reactions: NotRequired[list[Reaction]]
    nonce: NotRequired[int | str]
    pinned: bool
    webhook_id: NotRequired[str]
    type: MessageType
    activity: NotRequired[MessageActivity]
    application: NotRequired["Application"]
    application_id: NotRequired[str]
    message_reference: NotRequired[MessageReference]
    flags: NotRequired[MessageFlag]
    referenced_message: NotRequired[Message | None]
    interaction: NotRequired["MessageInteraction"]
    thread: NotRequired[Channel]
    components: NotRequired[list["ActionRowComponent"]]
    sticker_items: NotRequired[list["StickerItem"]]
    stickers: NotRequired[list["Sticker"]]
    position: NotRequired[int]
    role_subscription_data: NotRequired[RoleSubscriptionData]


class MessageActivity(TypedDict):
    type: MessageActivityType
    party_id: NotRequired[str]


class MessageActivityType(IntEnum):
    JOIN = 1
    SPECTATE = 2
    LISTEN = 3
    JOIN_REQUEST = 4


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
    SUPPRESS_NOTIFICATIONS = 1 << 12


class MessageReference(TypedDict):
    message_id: NotRequired[str]
    channel_id: NotRequired[str]
    guild_id: NotRequired[str]
    fail_if_not_exists: NotRequired[bool]


class MessageType(IntEnum):
    DEFAULT = 0
    RECIPIENT_ADD = 1
    RECIPIENT_REMOVE = 2
    CALL = 3
    CHANNEL_NAME_CHANGE = 4
    CHANNEL_ICON_CHANGE = 5
    CHANNEL_PINNED_MESSAGE = 6
    USER_JOIN = 7
    GUILD_BOOST = 8
    GUILD_BOOST_TIER_1 = 9
    GUILD_BOOST_TIER_2 = 10
    GUILD_BOOST_TIER_3 = 11
    CHANNEL_FOLLOW_ADD = 12
    GUILD_DISCOVERY_DISQUALIFIED = 14
    GUILD_DISCOVERY_REQUALIFIED = 15
    GUILD_DISCOVERY_GRACE_PERIOD_INITIAL_WARNING = 16
    GUILD_DISCOVERY_GRACE_PERIOD_FINAL_WARNING = 17
    THREAD_CREATED = 18
    REPLY = 19
    CHAT_INPUT_COMMAND = 20
    THREAD_STARTER_MESSAGE = 21
    GUILD_INVITE_REMINDER = 22
    CONTEXT_MENU_COMMAND = 23
    AUTO_MODERATION_ACTION = 24
    ROLE_SUBSCRIPTION_PURCHASE = 25
    INTERACTION_PREMIUM_UPSELL = 26
    STAGE_START = 27
    STAGE_END = 28
    STAGE_SPEAKER = 29
    STAGE_TOPIC = 31
    GUILD_APPLICATION_PREMIUM_SUBSCRIPTION = 32


class Overwrite(TypedDict):
    id: str
    type: OverwriteType
    allow: str
    deny: str


class OverwriteType(IntEnum):
    ROLE = 0
    MEMBER = 1


class Reaction(TypedDict):
    count: int
    me: bool
    emoji: "Emoji"


class RoleSubscriptionData(TypedDict):
    role_subscription_listing_id: str
    tier_name: str
    total_months_subscribed: int
    is_renewal: bool


class SortOrder(IntEnum):
    LATEST_ACTIVITY = 0
    CREATION_DATE = 1


class ThreadMember(TypedDict):
    id: NotRequired[str]
    user_id: NotRequired[str]
    join_timestamp: str
    flags: int
    member: NotRequired["GuildMember"]


class ThreadMetadata(TypedDict):
    archived: bool
    auto_archive_duration: int
    archive_timestamp: str
    locked: bool
    invitable: NotRequired[bool]
    create_timestamp: NotRequired[str | None]


class VideoQualityMode(IntEnum):
    AUTO = 1
    FULL = 2
