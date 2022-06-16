from enum import Enum, unique
from typing import TypeVar

from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


@unique
class SortOrder(Enum):
    asc = "asc"
    desc = "desc"


@unique
class CompanyStatus(Enum):
    created = "created"
    active = "active"
    deactivated = "deactivated"


@unique
class Language(Enum):
    sv = "sv"
    en = "en"


@unique
class ContactType(Enum):
    phone_number = "phone_number"
    email = "email"


@unique
class RoleType(Enum):
    global_role = "global_role"
    company_role = "company_role"
