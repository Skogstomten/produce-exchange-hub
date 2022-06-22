from datetime import datetime
from unittest.mock import Mock

import pytest
from bson import ObjectId
from httpx import AsyncClient
from pytz import utc

from app.datastores.company_datastore import (
    get_company_datastore,
    CompanyDatastore,
)
from app.main import app
from app.models.v1.database_models.company_database_model import (
    CompanyDatabaseModel,
)

FAKE_COMPANY = CompanyDatabaseModel(
    **{
        "id": "doc_id",
        "name": {},
        "status": "active",
        "created_date": datetime.now(utc),
        "company_types": [],
        "content_languages_iso": [],
        "description": {},
    }
)

company_datastore = Mock(CompanyDatastore)
company_datastore.activate_company.return_value(FAKE_COMPANY)


async def get_company_datastore_mock():
    return company_datastore


app.dependency_overrides[
    get_company_datastore
] = get_company_datastore_mock


@pytest.mark.anyio
async def test_activate_company():
    company_id = str(ObjectId())
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.put(f"/v1/sv/companies/{company_id}/activate")

    company_datastore.activate_company.assert_called_once_with(company_id)
    assert response.status_code == 200
