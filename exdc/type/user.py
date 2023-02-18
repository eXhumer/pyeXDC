from __future__ import annotations
from enum import IntFlag, StrEnum
from typing import NotRequired, TypedDict, TYPE_CHECKING

if TYPE_CHECKING:
    from .application_role_connection_metadata import ApplicationRoleConnectionMetadata


class ApplicationRoleConnection(TypedDict):
    platform_name: str | None
    platform_username: str | None
    metadata: "ApplicationRoleConnectionMetadata"


class Connection(TypedDict):
    id: str
    name: str
    type: ServiceType
    revoked: NotRequired[bool]
    integrations: NotRequired[list]
    verified: bool
    friend_sync: bool
    show_activity: bool
    two_way_link: bool
    visibility: int


class PremiumType(IntFlag):
    NONE = 0
    NITRO_CLASSIC = 1
    NITRO = 2
    NITRO_BASIC = 3


class ServiceType(StrEnum):
    BATTLE_NET = "battlenet"
    EBAY = "ebay"
    EPIC_GAMES = "epicgames"
    FACEBOOK = "facebook"
    GITHUB = "github"
    INSTAGRAM = "instagram"
    LEAGUE_OF_LEGENDS = "leagueoflegends"
    PAYPAL = "paypal"
    PLAYSTATION = "playstation"
    REDDIT = "reddit"
    RIOT_GAMES = "riotgames"
    SPOTIFY = "spotify"
    SKYPE = "skype"
    STEAM = "steam"
    TIKTOK = "tiktok"
    TWITCH = "twitch"
    TWITTER = "twitter"
    XBOX = "xbox"
    YOUTUBE = "youtube"


class User(TypedDict):
    id: str
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
    premium_type: NotRequired[PremiumType]
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
    ACTIVE_DEVELOPER = 1 << 22
