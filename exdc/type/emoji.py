from __future__ import annotations
from typing import NotRequired, TypedDict, TYPE_CHECKING

if TYPE_CHECKING:
    from .permissions import Role
    from .user import User


class Emoji(TypedDict):
    id: str | None
    name: str | None
    roles: NotRequired[list["Role"]]
    user: NotRequired["User"]
    require_colons: NotRequired[bool]
    managed: NotRequired[bool]
    animated: NotRequired[bool]
    available: NotRequired[bool]
