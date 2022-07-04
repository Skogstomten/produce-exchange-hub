"""Contains user related test fixtures."""
from datetime import datetime

import pytest
from pytz import utc

from app.models.v1.database_models.user_database_model import UserDatabaseModel


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
