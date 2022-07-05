from datetime import datetime
from unittest.mock import Mock

import pytest
from bson import ObjectId
from pytz import utc

from app.datastores.user_datastore import UserDatastore
from app.dependencies.log import AppLogger
from app.models.v1.database_models.contact_database_model import ContactDatabaseModel
from app.models.v1.shared import ContactType


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
