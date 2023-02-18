from __future__ import annotations
from enum import IntEnum
from typing import NotRequired, TypedDict


class ApplicationRoleConnectionMetadata(TypedDict):
    type: ApplicationRoleConnectionMetadataType
    key: str
    name: str
    name_localizations: NotRequired[dict[str, str]]
    description: str
    name_localizations: NotRequired[dict[str, str]]


class ApplicationRoleConnectionMetadataType(IntEnum):
    INTEGER_LESS_THAN_OR_EQUAL = 1
    INTEGER_GREATER_THAN_OR_EQUAL = 2
    INTEGER_EQUAL = 3
    INTEGER_NOT_EQUAL = 4
    DATETIME_LESS_THAN_OR_EQUAL = 5
    DATETIME_GREATER_THAN_OR_EQUAL = 6
    BOOLEAN_EQUAL = 7
    BOOLEAN_NOT_EQUAL = 8
