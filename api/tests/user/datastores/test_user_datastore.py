"""Tests for user_datastore module."""
from datetime import datetime
from unittest.mock import Mock

from bson import ObjectId
from pytz import utc

from app.database.mongo.mongo_document_database import MongoDocument
from app.shared.models.v1.shared import RoleType
from app.user.datastores.role_datastore import RoleDatastore
from app.user.datastores.user_datastore import UserDatastore
from app.user.models.db.role import RoleDatabaseModel


def test_add_role_to_user_can_add_role(
    authenticated_user_default, company_id, file_manager, doc_database_collection_mocks, doc_id
):
    fake_role = RoleDatabaseModel(id=str(ObjectId()), name="company_admin", type=RoleType.company_role)
    fake_user = {
        "_id": ObjectId(doc_id),
        "email": "nisse@perssons.se",
        "firstname": "Nisse",
        "lastname": "Persson",
        "city": "Visby",
        "country_iso": "SE",
        "timezone": "Europe/Stockholm",
        "language_iso": "SV",
        "verified": True,
        "password_hash": "ThisIsHash_IPromizze",
        "created": datetime.now(utc),
        "last_logged_in": None,
        "roles": [],
    }
    db, collection = doc_database_collection_mocks
    role_datastore = Mock(RoleDatastore)
    role_datastore.get_role.return_value = fake_role
    collection.by_id.return_value = MongoDocument(fake_user, collection)
    db.collection.return_value = collection

    target = UserDatastore(db, role_datastore, file_manager)
    target.add_role_to_user(authenticated_user_default, doc_id, "company_admin", company_id)

    collection.update_document.assert_called_once()
