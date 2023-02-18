from __future__ import annotations
from enum import IntFlag
from typing import NotRequired, TypedDict, TYPE_CHECKING

if TYPE_CHECKING:
    from .oauth2 import OAuth2Scope
    from .teams import Team
    from .user import User


class Application(TypedDict):
    id: str
    name: str
    icon: str | None
    description: str
    rpc_origins: NotRequired[list[str]]
    bot_public: bool
    bot_require_code_grant: bool
    terms_of_service_url: NotRequired[str]
    privacy_policy_url: NotRequired[str]
    owner: NotRequired[User]
    verify_key: str
    team: Team | None
    guild_id: NotRequired[str]
    primary_sku_id: NotRequired[str]
    slug: NotRequired[str]
    cover_image: NotRequired[str]
    flags: NotRequired[ApplicationFlag]
    tags: NotRequired[list[str]]
    install_params: NotRequired[InstallParams]
    custom_install_url: NotRequired[str]
    role_connections_verification_url: NotRequired[str]


class ApplicationFlag(IntFlag):
    GATEWAY_PRESENCE = 1 << 12
    GATEWAY_PRESENCE_LIMITED = 1 << 13
    GATEWAY_GUILD_MEMBERS = 1 << 14
    GATEWAY_GUILD_MEMBERS_LIMITED = 1 << 15
    VERIFICATION_PENDING_GUILD_LIMIT = 1 << 16
    EMBEDDED = 1 << 17
    GATEWAY_MESSAGE_CONTENT = 1 << 18
    GATEWAY_MESSAGE_CONTENT_LIMITED = 1 << 19
    APPLICATION_COMMAND_BADGE = 1 << 23


class InstallParams(TypedDict):
    scopes: list[OAuth2Scope]
    permissions: str
