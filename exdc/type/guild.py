from __future__ import annotations
from enum import IntEnum, IntFlag, StrEnum
from typing import NotRequired, TypedDict, TYPE_CHECKING

if TYPE_CHECKING:
    from .application import Application
    from .emoji import Emoji
    from .oauth2 import OAuth2Scope
    from .permissions import Role
    from .sticker import Sticker
    from .user import User


class Ban(TypedDict):
    reason: str | None
    user: "User"


class DefaultMessageNotificationLevel(IntEnum):
    ALL_MESSAGES = 0
    ONLY_MENTIONS = 1


class ExplicitContentFilterLevel(IntEnum):
    DISABLED = 0
    MEMBERS_WITHOUT_ROLES = 1
    ALL_MEMBERS = 2


class Guild(TypedDict):
    id: str
    name: str
    icon: str | None
    icon_hash: NotRequired[str | None]
    splash: str | None
    discovery_splash: str | None
    owner: NotRequired[bool]
    owner_id: str
    permissions: NotRequired[str]
    region: NotRequired[str]
    afk_channel_id: str | None
    afk_timeout: int
    widget_enabled: NotRequired[bool]
    widget_channel_id: NotRequired[str | None]
    verification_level: VerificationLevel
    default_message_notifications: DefaultMessageNotificationLevel
    explicit_content_filter: ExplicitContentFilterLevel
    roles: list["Role"]
    emojis: list["Emoji"]
    features: list[GuildFeature | GuildMutableFeatue]
    mfa_level: MFALevel
    application_id: str | None
    system_channel_id: str | None
    system_channel_flags: SystemChannelFlag
    rules_channel_id: str | None
    max_presences: NotRequired[int | None]
    max_members: NotRequired[int]
    vanity_url_code: str | None
    description: str | None
    banner: str | None
    premium_tier: PremiumTier
    premium_subscription_count: NotRequired[int]
    preferred_locale: str
    public_updates_channel_id: str | None
    max_video_channel_users: NotRequired[int]
    approximate_member_count: NotRequired[int]
    approximate_presence_count: NotRequired[int]
    welcome_screen: NotRequired[WelcomeScreen]
    nsfw_level: GuildNSFWLevel
    stickers: NotRequired[list["Sticker"]]
    premium_progress_bar_enabled: bool


class GuildFeature(StrEnum):
    ANIMATED_BANNER = "ANIMATED_BANNER"
    ANIMATED_ICON = "ANIMATED_ICON"
    APPLICATION_COMMAND_PERMISSIONS_V2 = "APPLICATION_COMMAND_PERMISSIONS_V2"
    AUTO_MODERATION = "AUTO_MODERATION"
    BANNER = "BANNER"
    COMMUNITY = "COMMUNITY"
    CREATOR_MONETIZABLE_PROVISIONAL = "CREATOR_MONETIZABLE_PROVISIONAL"
    CREATOR_STORE_PAGE = "CREATOR_STORE_PAGE"
    DEVELOPER_SUPPORT_SERVER = "DEVELOPER_SUPPORT_SERVER"
    DISCOVERABLE = "DISCOVERABLE"
    FEATURABLE = "FEATURABLE"
    INVITES_DISABLED = "INVITES_DISABLED"
    INVITE_SPLASH = "INVITE_SPLASH"
    MEMBER_VERIFICATION_GATE_ENABLED = "MEMBER_VERIFICATION_GATE_ENABLED"
    MORE_STICKERS = "MORE_STICKERS"
    NEWS = "NEWS"
    PARTNERED = "PARTNERED"
    PREVIEW_ENABLED = "PREVIEW_ENABLED"
    ROLE_ICONS = "ROLE_ICONS"
    ROLE_SUBSCRIPTIONS_AVAILABLE_FOR_PURCHASE = "ROLE_SUBSCRIPTIONS_AVAILABLE_FOR_PURCHASE"
    ROLE_SUBSCRIPTIONS_ENABLED = "ROLE_SUBSCRIPTIONS_ENABLED"
    TICKETED_EVENTS_ENABLED = "TICKETED_EVENTS_ENABLED"
    VANITY_URL = "VANITY_URL"
    VERIFIED = "VERIFIED"
    VIP_REGIONS = "VIP_REGIONS"
    WELCOME_SCREEN_ENABLED = "WELCOME_SCREEN_ENABLED"


class GuildMemberFlag(IntFlag):
    DID_REJOIN = 1 << 0
    COMPLETED_ONBOARDING = 1 << 1
    BYPASSES_VERIFICATION = 1 << 2
    STARTED_ONBOARDING = 1 << 3


class GuildMember(TypedDict):
    user: NotRequired["User"]
    nick: NotRequired[str | None]
    avatar: NotRequired[str | None]
    roles: list[str]
    joined_at: str
    premium_since: NotRequired[str | None]
    deaf: bool
    mute: bool
    flags: GuildMemberFlag
    pending: NotRequired[bool]
    permissions: NotRequired[str]
    communication_disabled_until: NotRequired[str | None]


class GuildMutableFeatue(StrEnum):
    COMMUNITY = "COMMUNITY"
    INVITES_DISABLED = "INVITES_DISABLED"
    DISCOVERABLE = "DISCOVERABLE"


class GuildNSFWLevel(IntEnum):
    DEFAULT = 0
    EXPLICIT = 1
    SAFE = 2
    AGE_RESTRICTED = 3


class GuildPreview(TypedDict):
    id: str
    name: str
    icon: str | None
    splash: str | None
    discovery_splash: str | None
    emojis: list["Emoji"]
    features: list[GuildFeature | GuildMutableFeatue]
    approximate_member_count: int
    approximate_presence_count: int
    description: str | None
    stickers: list["Sticker"]


class GuildWidget(TypedDict):
    id: str
    name: str
    instant_invite: str | None
    instant_invite: str | None
    members: list["User"]
    presence_count: int


class GuildWidgetSettings(TypedDict):
    enabled: bool
    channel_id: str | None


class Integration(TypedDict):
    id: str
    name: str
    type: IntegrationType
    enabled: bool
    syncing: NotRequired[bool]
    role_id: NotRequired[str]
    enable_emoticons: NotRequired[bool]
    expire_behavior: NotRequired[IntegrationExpireBehavior]
    expire_grace_period: NotRequired[int]
    user: NotRequired["User"]
    account: IntegrationAccount
    synced_at: NotRequired[str]
    subscriber_count: NotRequired[int]
    revoked: NotRequired[bool]
    application: NotRequired["Application"]
    scopes: NotRequired["OAuth2Scope"]


class IntegrationAccount(TypedDict):
    id: str
    name: str


class IntegrationExpireBehavior(IntEnum):
    REMOVE_ROLE = 0
    KICK = 1


class IntegrationType(StrEnum):
    TWITCH = "twitch"
    YOUTUBE = "youtube"
    DISCORD = "discord"
    GUILD_SUBSCRIPTION = "guild_subscription"


class MFALevel(IntEnum):
    NONE = 0
    ELEVATED = 1


class PremiumTier(IntEnum):
    NONE = 0
    TIER_1 = 1
    TIER_2 = 2
    TIER_3 = 3


class SystemChannelFlag(IntFlag):
    SUPRESS_JOIN_NOTIFICATIONS = 1 << 0
    SUPPRESS_PREMIUM_SUBSCRIPTIONS = 1 << 1
    SUPPRESS_GUILD_REMINDER_NOTIFICATIONS = 1 << 2
    SUPPRESS_JOIN_NOTIFICATION_REPLIES = 1 << 3
    SUPPRESS_ROLE_SUBSCRIPTION_PURCHASE_NOTIFICATIONS = 1 << 4
    SUPPRESS_ROLE_SUBSCRIPTION_PURCHASE_NOTIFICATION_REPLIES = 1 << 5


class UnavailableGuild(TypedDict):
    id: str
    unavailable: bool


class VerificationLevel(IntEnum):
    NONE = 0
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    VERY_HIGH = 4


class WelcomeScreen(TypedDict):
    description: str | None
    welcome_channels: list[WelcomScreenChannel]


class WelcomScreenChannel(TypedDict):
    channel_id: str
    description: str
    emoji_id: str | None
    emoji_name: str | None
