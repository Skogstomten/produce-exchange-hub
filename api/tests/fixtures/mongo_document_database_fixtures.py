"""Contains fixture for mongo document database."""
from unittest.mock import Mock

import pytest
from bson import ObjectId

from app.database.document_database import DocumentDatabase, DocumentCollection
from app.database.mongo.mongo_document_database import MongoDatabaseCollection


@pytest.fixture
def mongo_database_collection_mock():
    """Fixture for mock of document collection."""
    return Mock(MongoDatabaseCollection)


@pytest.fixture
def obj_id():
    """Fixture with a random doc id of type bson.ObjectId"""
    return ObjectId()


@pytest.fixture
def doc_id(obj_id):
    """Fixture with random doc id as str."""
    return str(obj_id)


@pytest.fixture
def doc_database_collection_mocks():
    """
    Fixture setting up mock of app.database.document_database.DocumentDatabase.
    Is also setup for using the transaction decorator.
    :return: Mock(DocumentDatabase)
        with collection.return_value = Mock(MongoDatabaseCollection)
        as tuple[Mock[DocumentDatabase], Mock[MongoDatabaseCollection]]
    """

    def fake_decorator_function(datastore, function, *args, **kwargs):
        return function(datastore, *args, **kwargs)

    collection_mock = Mock(MongoDatabaseCollection)
    db_mock = Mock(DocumentDatabase)

    db_mock.transaction = fake_decorator_function
    db_mock.collection.return_value = collection_mock
    return db_mock, collection_mock


@pytest.fixture
def document_collection_mock():
    mock = Mock(DocumentCollection)
    mock.skip.return_value = mock
    mock.take.return_value = mock
    mock.sort.return_value = mock
    return mock
