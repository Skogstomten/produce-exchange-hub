"""Tests for MongoDocument class in mongo_document_database module."""
import pytest
from bson import ObjectId

from app.database.mongo.mongo_document_database import MongoDocument


@pytest.fixture
def basic_target(mongo_database_collection_mock, obj_id):
    """Sets up a basic test target."""
    return MongoDocument({"_id": obj_id, "name": "Nisse"}, mongo_database_collection_mock)


def test_len_returns_correct_value(basic_target):
    assert len(basic_target) == 2


def test_doc_converted_to_dict_is_correct_length(basic_target):
    assert len(basic_target.to_dict()) == 2


def test_id_in_doc_dict(basic_target):
    assert "id" in basic_target.to_dict()


def test_correct_id_in_doc_dict(mongo_database_collection_mock, obj_id):
    data = MongoDocument({"_id": obj_id}, mongo_database_collection_mock).to_dict()
    assert data["id"] == str(obj_id)


def test_other_data_is_correct(mongo_database_collection_mock, obj_id):
    data = MongoDocument({"_id": obj_id, "name": "Nisse"}, mongo_database_collection_mock).to_dict()
    assert data["name"] == "Nisse"


def test_doc_replace_calls_collection_replace(mongo_database_collection_mock, obj_id):
    target = MongoDocument({"_id": obj_id}, mongo_database_collection_mock)
    target.replace(target.to_dict())

    mongo_database_collection_mock.replace.assert_called_once_with(str(obj_id), {"id": str(obj_id)})


def test_replace_calls_replace_with_correct_doc_id(mongo_database_collection_mock, obj_id):
    def _verify(d_id, _):
        assert d_id == str(obj_id)

    mongo_database_collection_mock.replace = _verify

    target = MongoDocument({"_id": obj_id}, mongo_database_collection_mock)
    data = target.to_dict()
    target.replace(data)


def test_replacing_document_with_dict_does_not_insert_id_into_database(mongo_database_collection_mock, obj_id):
    def _verify_call(_, data_obj):
        assert len(data_obj) == 2, "len of data_obj is wrong"
        assert "name" in data_obj, "name is not found in data_obj"
        assert "id" in data_obj, "_id is not found in data_obj"
        assert data_obj["id"] == str(obj_id), "_id in data_obj is not same as obj_id"

    mongo_database_collection_mock.replace = _verify_call

    target = MongoDocument({"_id": obj_id, "name": "Nisse"}, mongo_database_collection_mock)
    data = target.to_dict()
    data["name"] = "Egon"
    target.replace(data)


def test_replacing_doc_works_by_passing_doc(mongo_database_collection_mock, obj_id):
    def _verify_call(doc_id, data_obj):
        assert doc_id == str(obj_id)
        assert len(data_obj) == 2
        assert "name" in data_obj
        assert "id" in data_obj
        assert data_obj["id"] == str(obj_id)

    # mongo_database_collection_mock.find_one.return_value = {"_id": obj_id, "name": "Egon"}
    mongo_database_collection_mock.replace = _verify_call

    target = MongoDocument({"_id": obj_id, "name": "Nisse"}, mongo_database_collection_mock)
    target["name"] = "Egon"
    target.replace(target)
