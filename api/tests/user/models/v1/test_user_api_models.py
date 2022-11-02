from fastapi import APIRouter

from app.shared.models.v1.shared import Language, CountryCode
from app.user.models.v1.user_api_models import UserOutModel
from tests.fixtures.user_fixtures import get_user


def test_user_out_model_from_database_model(http_request):
    result = UserOutModel.from_database_model(
        get_user(
            user_id="62dff56418a15da3e2708434",
            email="modscorpiogrl@gmail.com",
            firstname="Cecilia",
            lastname="Miller",
            city="Visby",
            country_iso=CountryCode.SE,
            timezone="Europe/Stockholm",
            language_iso=Language.SV,
            verified=True,
        ),
        http_request,
        APIRouter(),
        Language.SV,
    )
    assert result is not None
