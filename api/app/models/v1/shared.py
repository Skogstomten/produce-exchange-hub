"""Shared models and enums."""
from enum import Enum, unique
from typing import TypeVar

from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


@unique
class SortOrder(Enum):
    """Sort order."""

    asc = "asc"
    desc = "desc"


@unique
class CompanyStatus(Enum):
    """Available statuses for companies."""

    created = "created"
    active = "active"
    deactivated = "deactivated"


@unique
class Language(Enum):
    """Available languages."""

    sv = "sv"
    en = "en"

    def __str__(self):
        return self.value


@unique
class ContactType(Enum):
    """Available contact types."""

    phone_number = "phone_number"
    email = "email"


@unique
class RoleType(Enum):
    """Available role types."""

    global_role = "global_role"
    company_role = "company_role"


@unique
class FileType(Enum):
    """Supported file types for images."""

    jpg = "jpg"

    def __str__(self):
        return self.value
