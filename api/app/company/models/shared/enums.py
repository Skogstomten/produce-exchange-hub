from enum import Enum, unique


@unique
class CompanyStatus(Enum):
    """Available statuses for companies."""

    created = "created"
    active = "active"
    deactivated = "deactivated"


@unique
class ContactType(Enum):
    """Available contact types."""

    phone_number = "phone_number"
    email = "email"


@unique
class Currency(Enum):
    SEK = "SEK"
    EUR = "EUR"


@unique
class IntervalType(Enum):
    day = "day"
    week = "week"
    month = "month"


@unique
class SortOrder(Enum):
    """Sort order."""

    asc = "asc"
    desc = "desc"


@unique
class CompanyTypes(Enum):
    """Enum with the available company types."""

    producer = "producer"
    buyer = "buyer"
