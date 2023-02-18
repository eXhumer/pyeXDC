from __future__ import annotations
from enum import IntEnum
from typing import TypedDict, TYPE_CHECKING

if TYPE_CHECKING:
    from .user import User


class MembershipState(IntEnum):
    INVITED = 1
    ACCEPTED = 2


class Team(TypedDict):
    icon: str | None
    id: str
    members: list[TeamMember]
    name: str
    owner_user_id: str


class TeamMember(TypedDict):
    membership_state: int
    permissions: list[str]
    team_id: str
    user: "User"
