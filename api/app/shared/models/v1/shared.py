"""Shared models and enums."""
from enum import Enum, unique
from typing import TypeVar

from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


@unique
class RoleType(Enum):
    """Available role types."""

    global_role = "global_role"
    company_role = "company_role"


@unique
class CountryCode(Enum):
    SE = "SE"
