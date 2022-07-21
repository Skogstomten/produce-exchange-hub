from datetime import datetime
from unittest.mock import Mock

import pytest
from bson import ObjectId
from pytz import utc
from starlette.datastructures import URL
from starlette.requests import Request

from app.datastores.user_datastore import UserDatastore
from app.dependencies.log import AppLogger
from app.io.file_manager import FileManager
from app.models.v1.database_models.contact import ContactDatabaseModel
from app.models.v1.shared import ContactType, CompanyStatus


def _get_id() -> str:
    return str(ObjectId())


def _get_contact_model(
    contact_id: str = _get_id(),
    contact_type: ContactType = ContactType.email,
    value: str = "nisse@perssons.se",
    created_by: str = "user@email.com",
    created_at: datetime = datetime.now(utc),
) -> ContactDatabaseModel:
    return ContactDatabaseModel(
        id=contact_id,
        type=contact_type,
        value=value,
        created_by=created_by,
        created_at=created_at,
    )


def get_company_database_dict(
    company_id: ObjectId = ObjectId(),
    name: dict[str, str] = None,
    status: CompanyStatus = CompanyStatus.active,
    created_date: datetime = datetime.now(utc),
    company_types: list[str] | None = None,
    content_languages_iso: list[str] | None = None,
    activation_date: datetime | None = None,
    description: dict[str, str] | None = None,
    external_website_url: str | None = None,
    contacts: list[dict] | None = None,
    changes: list[dict] | None = None,
):
    if name is None:
        name = {}
    if company_types is None:
        company_types = []
    if content_languages_iso is None:
        content_languages_iso = []
    if description is None:
        description = []
    if contacts is None:
        contacts = []
    if changes is None:
        changes = []

    return {
        "_id": company_id,
        "name": name,
        "status": status,
        "created_date": created_date,
        "company_types": company_types,
        "content_languages_iso": content_languages_iso,
        "activation_date": activation_date,
        "description": description,
        "external_website_url": external_website_url,
        "contacts": contacts,
        "changes": changes,
    }


@pytest.fixture
def logger():
    """Creates logger mock."""
    mock = Mock(AppLogger)
    return mock


@pytest.fixture
def user_datastore():
    """Creates mock for user datastore."""
    mock = Mock(UserDatastore)
    return mock


@pytest.fixture
def fake_company_data(obj_id):
    """Fake document fixture."""

    fake_doc = {
        "_id": obj_id,
        "name": {},
        "status": "active",
        "created_date": datetime.now(utc),
        "company_types": [],
        "content_languages_iso": [],
        "description": {},
        "contacts": [],
        "changes": [],
    }
    return str(obj_id), fake_doc


@pytest.fixture
def company_id():
    """Creates company id."""
    return _get_id()


@pytest.fixture
def contact_id():
    """Creates contact id."""
    return _get_id()


@pytest.fixture
def contact_model(contact_id):
    """Initiates a contact model."""
    return _get_contact_model()


@pytest.fixture
def file_manager():
    return Mock(FileManager)


@pytest.fixture
def http_request():
    request_mock = Mock(Request)

    url_mock = Mock(URL)
    url_mock.scheme = "http"
    url_mock.hostname = "localhost"
    url_mock.port = 8000
    url_mock.path = "/v1"

    type(request_mock).url = url_mock
    return request_mock
