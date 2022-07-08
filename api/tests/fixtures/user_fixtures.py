"""Contains user related test fixtures."""
from datetime import datetime

import pytest
from bson import ObjectId
from pytz import utc

from app.models.v1.database_models.user_database_model import UserDatabaseModel, UserRoleDatabaseModel
from app.models.v1.shared import RoleType


def get_user(
    user_id: str = str(ObjectId()),
    email: str = "nisse@perssons.se",
    firstname: str = "Nisse",
    lastname: str = "Persson",
    city: str = "Visby",
    country_iso: str = "SE",
    timezone: str = "Europe/Stockholm",
    language_iso: str = "sv",
    verified: bool = True,
    password_hash: str = "uZEDYB40NDvgMqNF83W-gfxpEmpUWSfVEzhLZErIVsi4pTAJVLArCuvOZ__VLLZNxAl_SApFFjfQ2byTpy9Khkg2NFhYc"
    "UV6eFJ0c1htUHJ0TU9pczRPOGEzZFk3U09nU2tiVENHa2luRTN1cy1BOHQ4SmJxNVNvMGxxbXNmNmpab19LWDVhVUFCU0"
    "RHN0hOU3haenBYejZuc3JNWDdJZWNGaHlGOTNlMUowSVJMMGQ3cEZyd0dMbGdtdkcybGdIMU9CdlJKd0l1dUtsSXk4Q25"
    "GWWhHbXpuMVJtZU45ZnZTVnpIQXJkeFJmcWpUZTdsVXRMNTFCUmFpZUc2Z1o5M201UnhOUDJaSmNtSVR3QXJJWHNrT2lx"
    "ZFFyOWdzbWZrbmlNTHVJLWV4Mm9ONlJQTzVVN2twQTh1aE5wNDNwUnQ2MFlUb0tDTkFjdFFMMmhBcGxiZTFpTEVSeFpxa"
    "FhXRWw1eFZaVHd5WFVpWlB2X0RlWUlmSVVhZFRVX2tLV2l5N05HU1UwYm9uRGJDVXVfVXlBV0ZZdz09",
    created: datetime = datetime.now(utc),
    last_logged_in: datetime | None = None,
    roles: list[dict] | None = None,
) -> UserDatabaseModel:
    if roles is None:
        roles = []
    return UserDatabaseModel(
        id=user_id,
        email=email,
        firstname=firstname,
        lastname=lastname,
        city=city,
        country_iso=country_iso,
        timezone=timezone,
        language_iso=language_iso,
        verified=verified,
        password_hash=password_hash,
        created=created,
        last_logged_in=last_logged_in,
        roles=roles,
    )


def get_role(
    user_role_id: str = str(ObjectId()),
    role_id: str = str(ObjectId()),
    role_name: str = "company_admin",
    role_type: RoleType = RoleType.company_role,
    reference: str | None = None,
) -> UserRoleDatabaseModel:
    return UserRoleDatabaseModel(
        id=user_role_id,
        role_id=role_id,
        role_name=role_name,
        role_type=role_type,
        reference=reference,
    )


@pytest.fixture
def superuser_user_role():
    return get_role(role_name="superuser", role_type=RoleType.global_role)


@pytest.fixture
def company_admin_role():
    return get_role()


@pytest.fixture
def authenticated_user_default(doc_id):
    """Creates a default authenticated user object of UserDatabaseModel."""
    return UserDatabaseModel(
        id=doc_id,
        email="nisse@perssons.se",
        firstname="Nisse",
        lastname="Persson",
        city="Visby",
        country_iso="SE",
        timezone="Europe/Stockholm",
        language_iso="SV",
        verified=True,
        password_hash="uZEDYB40NDvgMqNF83W-gfxpEmpUWSfVEzhLZErIVsi4pTAJVLArCuvOZ__VLLZNxAl_SApFFjfQ2byTpy9Khkg2NFhYc"
        "UV6eFJ0c1htUHJ0TU9pczRPOGEzZFk3U09nU2tiVENHa2luRTN1cy1BOHQ4SmJxNVNvMGxxbXNmNmpab19LWDVhVUFCU0"
        "RHN0hOU3haenBYejZuc3JNWDdJZWNGaHlGOTNlMUowSVJMMGQ3cEZyd0dMbGdtdkcybGdIMU9CdlJKd0l1dUtsSXk4Q25"
        "GWWhHbXpuMVJtZU45ZnZTVnpIQXJkeFJmcWpUZTdsVXRMNTFCUmFpZUc2Z1o5M201UnhOUDJaSmNtSVR3QXJJWHNrT2lx"
        "ZFFyOWdzbWZrbmlNTHVJLWV4Mm9ONlJQTzVVN2twQTh1aE5wNDNwUnQ2MFlUb0tDTkFjdFFMMmhBcGxiZTFpTEVSeFpxa"
        "FhXRWw1eFZaVHd5WFVpWlB2X0RlWUlmSVVhZFRVX2tLV2l5N05HU1UwYm9uRGJDVXVfVXlBV0ZZdz09",
        created=datetime.now(utc),
        last_logged_in=datetime.now(utc),
        roles=[],
    )
