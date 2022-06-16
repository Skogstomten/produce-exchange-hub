from unittest.mock import Mock, MagicMock

from bson import ObjectId
from pymongo.collection import Collection
from pytest import fixture

from app.database.mongo.mongo_document_database import MongoDocument


@fixture
def collection():
    return Mock(Collection)


def test_len_returns_correct_value(collection):
    target = MongoDocument({"_id": ObjectId, "name": "Nisse"}, collection)
    assert len(target) == 2


def test_converting_doc_to_dict_gives_you_correct_data(collection):
    obj_id = ObjectId()
    target = MongoDocument({"_id": obj_id, "name": "Nisse"}, collection)
    data = target.to_dict()
    assert len(data) == 2
    assert "id" in data
    assert data["id"] == str(obj_id)
    assert "name" in data
    assert data["name"] == "Nisse"


def test_replacing_document_with_dict_does_not_insert_id_into_database(collection):
    obj_id = ObjectId()
    collection.find_one.return_value = {"_id": obj_id, "name": "Egon"}
    collection.replace_one = MagicMock()
    target = MongoDocument({"_id": obj_id, "name": "Nisse"}, collection)
    data = target.to_dict()
    data["name"] = "Egon"
    target.replace(data)
    collection.replace_one.replace_one.assert_called_with(
        {"_id": obj_id},
        {
            "_id": obj_id,
            "name": "Egon",
        }
    )


def test_replacing_doc_works_by_passing_doc(collection):
    obj_id = ObjectId()
    collection.find_one.return_value = {"_id": obj_id, "name": "Egon"}
    collection.replace_one = MagicMock()
    target = MongoDocument({"_id": obj_id, "name": "Nisse"}, collection)
    target["name"] = "Egon"
    target.replace(target)
    collection.replace_one.replace_one.assert_called_with({
        "_id": obj_id,
        "name": "Egon",
    })
