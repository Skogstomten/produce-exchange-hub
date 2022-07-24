"""Tests for user_datastore module."""
from datetime import datetime
from unittest.mock import Mock

from bson import ObjectId
from pytz import utc

from app.database.abstract.document_database import DocumentDatabase
from app.database.mongo.mongo_document_database import MongoDocument, MongoDatabaseCollection
from app.user.datastores.role_datastore import RoleDatastore
from app.user.datastores.user_datastore import UserDatastore
from app.user.models.db.role import RoleDatabaseModel
from app.shared.models.v1.shared import RoleType


def test_add_role_to_user_can_add_role(authenticated_user_default, company_id, file_manager):
    user_id = str(ObjectId())
    fake_role = RoleDatabaseModel(id=str(ObjectId()), name="company_admin", type=RoleType.company_role)
    fake_user = {
        "_id": ObjectId(user_id),
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
    db = Mock(DocumentDatabase)
    role_datastore = Mock(RoleDatastore)
    role_datastore.get_role.return_value = fake_role
    collection = Mock(MongoDatabaseCollection)
    collection.by_id.return_value = MongoDocument(fake_user, collection)
    db.collection.return_value = collection

    target = UserDatastore(db, role_datastore, file_manager)
    target.add_role_to_user(authenticated_user_default, user_id, "company_admin", company_id)

    collection.update_document.assert_called_once()
