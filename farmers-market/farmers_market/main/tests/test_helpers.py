from typing import Iterable

from django.contrib.auth.models import User
from django.test import Client, TestCase as DjangoTestCase

from main.models import Company, CompanyUser, CompanyRole, CompanyType, Language, CompanyStatus, ContactType

PASSWORD = "test123"


class TestCase(DjangoTestCase):
    def login_user(self, user: User):
        self.client.login(username=user.username, password=PASSWORD)


def create_user(email="nisse@persson.se") -> User:
    return User.objects.create_user(email, email, PASSWORD)


def create_authenticated_user(client: Client, email="nisse@persson.se") -> User:
    user = create_user(email=email)
    client.login(username=user.username, password=PASSWORD)
    return user


def create_company_with_admin(company_types: Iterable[str] = ()) -> tuple[Company, User]:
    """
    Creates a company with an admin user.

    Returns:
        Tuple[Company, User, username, password]
    """
    company = create_company(company_types=company_types)
    role = get_company_admin_role()
    user = create_user()
    CompanyUser.objects.create(company=company, role=role, user=user)
    return company, user


def create_company_with_logged_in_admin(client: Client, company_types: Iterable[str] = ()) -> tuple[Company, User]:
    company, user = create_company_with_admin(company_types=company_types)
    client.login(username=user.username, password=PASSWORD)
    return company, user


def get_company_admin_role() -> CompanyRole:
    return get_company_role("company_admin")


def get_company_role(role_name: str) -> CompanyRole:
    return CompanyRole.objects.get(role_name=role_name)


def get_company_type(type_name: str) -> CompanyType:
    return CompanyType.objects.get(type_name=type_name)


def get_language(iso_639_1: str) -> Language:
    return Language.objects.get(iso_639_1=iso_639_1)


def get_status(status_name: str) -> CompanyStatus:
    return CompanyStatus.objects.get(status_name=status_name)


def create_company(company_types: Iterable[str] = ()) -> Company:
    company = Company.objects.create(name="Nisses firma", status=get_status("active"))
    for company_type in company_types:
        company.company_types.add(get_company_type(company_type))
    return company


def get_contact_type(contact_type) -> ContactType:
    return ContactType.objects.get(contact_type=contact_type)
