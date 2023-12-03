from enum import unique, Enum


@unique
class CompanyStatus(Enum):
    """Available statuses for companies."""

    created = "created"
    active = "active"
    deactivated = "deactivated"


@unique
class CompanyTypes(Enum):
    """Enum with the available company types."""

    producer = "producer"
    buyer = "buyer"


@unique
class Language(Enum):
    """Available languages."""

    SV = "SV"
    EN = "EN"

    def __str__(self):
        return self.value


@unique
class ContactType(Enum):
    """Available contact types."""

    phone_number = "phone_number"
    email = "email"


@unique
class ChangeType(Enum):
    """Enum containing change types for change model."""

    add = "add"
    update = "update"
    delete = "delete"


@unique
class CompanyRole(Enum):
    """Enum containing available role types for company users."""

    company_admin = "company_admin"
