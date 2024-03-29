"""
MongoDb implementation of document database interface
"""
from collections.abc import MutableMapping, Iterable
from datetime import datetime
from typing import Any

from pymongo import ASCENDING, DESCENDING
from pymongo.client_session import ClientSession
from pymongo.collection import Collection as MongoCollection, ObjectId
from pymongo.cursor import Cursor
from pymongo.database import Database as MongoDatabase

from app.database.abstract.document_database import (
    Document,
    DocumentDatabase,
    DocumentCollection,
    DatabaseCollection,
    DocumentDatabaseUpdateContext,
)
from app.logging.log import AppLogger
from app.shared.errors.errors import InvalidOperationError, NotFoundError
from app.database.mongo.enum_utils import enums_to_string


def _convert_str_id_to_object_id(data: Any) -> dict:
    """
    Converts data dict id field to mongodb _id field.

    >>> _convert_str_id_to_object_id({"id": "62e00647e98e01ef28be554b"})
    {'_id': ObjectId('62e00647e98e01ef28be554b')}

    >>> _convert_str_id_to_object_id({"col": {"id": "62e00647e98e01ef28be554b"}})
    {'col': {'_id': ObjectId('62e00647e98e01ef28be554b')}}

    >>> _convert_str_id_to_object_id({"v": [{"id": "62e00647e98e01ef28be554b"}]})
    {'v': [{'_id': ObjectId('62e00647e98e01ef28be554b')}]}
    """
    if isinstance(data, dict):
        data_copy = data.copy()
        for key, value in data_copy.items():
            if key == "id":
                data["_id"] = ObjectId(value)
                del data["id"]
            else:
                data[key] = _convert_str_id_to_object_id(value)
    elif isinstance(data, list):
        for index, value in enumerate(data):
            data[index] = _convert_str_id_to_object_id(value)
    return data


def _convert_object_id_to_str_id(data: dict) -> dict:
    """
    >>> _convert_object_id_to_str_id({"_id": ObjectId("62e00647e98e01ef28be554b")})
    {'id': '62e00647e98e01ef28be554b'}

    >>> _convert_object_id_to_str_id({"field": {"_id": ObjectId("62e00647e98e01ef28be554b")}})
    {'field': {'id': '62e00647e98e01ef28be554b'}}

    :param data:
    :return:
    """
    data = data.copy()
    for key, value in data.copy().items():
        if key == "_id":
            data["id"] = str(value)
            del data["_id"]
        elif isinstance(value, dict):
            data[key] = _convert_object_id_to_str_id(value)
    return data


def _ensure_updated(update_result, doc_id, collection_name):
    if update_result.modified_count < 1:
        raise NotFoundError(f"No document with key='{doc_id}' " f"was found in collection='{collection_name}'")


class MongoDBUpdateContext(DocumentDatabaseUpdateContext):
    def __init__(self):
        self._set_updates = []
        self._list_push_updates = {}

    def set_values(self, value_dict: dict[str, Any]) -> None:
        self._set_updates.append(value_dict)

    def push_to_list(self, list_name: str, data: Any) -> None:
        if list_name in self._list_push_updates:
            self._list_push_updates[list_name].append(data)
        else:
            self._list_push_updates[list_name] = [data]

    def to_implementation_specific_update_syntax(self) -> Any:
        data = {}
        if any(self._set_updates):
            data["$set"] = {}
            for set_update in self._set_updates:
                data["$set"].update(set_update)

        if any(self._list_push_updates):
            data["$push"] = {}
            for key, value in self._list_push_updates.items():
                if len(value) > 1:
                    data["$push"][key] = {"$each": value}
                elif len(value) == 1:
                    item = value[0]
                    if item is not None:
                        data["$push"][key] = item
        return data


class MongoDocument(Document):
    """
    Mongo db document.
    """

    def __init__(self, doc: dict, collection: "MongoDatabaseCollection"):
        """
        Creates a new document.

        :param doc: dict with document data.
        :param collection: reference to collection for performing operations
        on the document.
        """
        super().__init__()
        self._doc = doc
        self._collection = collection

    def __getitem__(self, key: str):
        """
        Get item by key. Forwards to underlying dict.

        if key == "id": will return document id converted to str.
        :param key: dict key.
        :return: value in dict at for specific key.
        """
        if key == "id":
            return self.id
        return self._doc[key]

    def __setitem__(self, key: str, value: Any) -> None:
        """
        Set value for given key.

        :param key: Value key.
        :param value: Value to be set for key.
        :return: None.
        """
        if key == "id":
            raise InvalidOperationError("field 'id' can't be set")
        self._doc[key] = value

    def __delitem__(self, key: str) -> None:
        """
        Delete item from document.
        Note!! Will not update document in database!

        :raise InvalidOperationError: if id field is trying to be deleted.
        This is not allowed.
        :param key: Key of value to be deleted.
        :return: None.
        """
        if key == "id":
            raise InvalidOperationError("field 'id' can't be deleted")
        self._doc.__delitem__(key)

    def __iter__(self) -> Iterable:
        """
        Iterable implementation.
        Returns a copy of the dictionary containing the data, with the id
        inserted as "id" instead of mongoDB default "_id".
        :return: Iterable for dict.
        """
        clone = self._doc.copy()
        clone = _convert_object_id_to_str_id(clone)
        return clone.__iter__()

    def __len__(self) -> int:
        """
        Returns number of fields in document.
        :return: Number of fields as int.
        """
        return self._doc.__len__()

    def __str__(self):
        return str(self._doc)

    def __repr__(self):
        return f"MongoDocument({repr(self._doc)}, {repr(self._collection)})"

    @property
    def id(self) -> str:
        """
        Converts the mongodb ObjectId id to str.
        :return: document id.
        """
        return str(self._doc["_id"])

    def to_dict(self) -> dict:
        """
        Gets document as dict.
        :return: dict.
        """
        return _convert_object_id_to_str_id(self._doc)

    def replace(self, data: MutableMapping) -> Document:
        """
        Replaces document data with given data and gives back the updated
        document.
        :param data: Updated data as a mutable mapping.
        :return: Updated document.
        """
        if isinstance(data, Document):
            data = data.to_dict()
        self._collection.replace(
            self.id,
            data,
        )
        return self._collection.by_id(self.id, None)

    def delete(self) -> None:
        """
        delete document from database.
        :return:
        """
        self._collection.delete(self.id)


class MongoDocumentCollection(DocumentCollection):
    """
    A collection of documents.
    Technically wraps a mongodb cursor to be able to filter selection before
    fetching all data.
    """

    def __init__(self, cursor: Cursor, collection: "MongoDatabaseCollection") -> None:
        """
        Creates a mongo document collection.
        :param cursor: Reference to db cursor.
        :param collection: Reference to db collection
        """
        self._cursor = cursor
        self._collection = collection

    def __str__(self):
        return f"{str(self._cursor)}, {str(self._collection)}"

    def __repr__(self):
        return f"MongoDocumentCollection({repr(self._cursor)}, {repr(self._collection)})"

    def skip(self, skip: int | None) -> "DocumentCollection":
        """
        Tells cursor to skip a certain number of documents.
        :param skip: Int value to skip or None. None will be ignored.
        :return: A reference to itself for chaining calls.
        """
        if skip is not None:
            self._cursor = self._cursor.skip(skip)
        return self

    def take(self, take: int | None) -> "DocumentCollection":
        """
        The number of documents to take from the collection.
        Passing None will result in nothing happening.
        :param take: Int number to take or None.
        :return: A reference to itself for chaining calls.
        """
        if take is not None:
            self._cursor = self._cursor.limit(take)
        return self

    def sort(self, sort_by: str | None, sort_order: str | None) -> "DocumentCollection":
        """
        Sorts the document.
        :param sort_by: Name of db field to sort by.
        :param sort_order: asc or desc
        :return: A reference to self for chaining calls.
        """
        if sort_by is not None:
            order = ASCENDING
            if sort_order == "desc":
                order = DESCENDING
            self._cursor = self._cursor.sort(sort_by, order)
        return self

    def to_list(self) -> list[Document]:
        """
        Converts the whole cursor of documents to an in memory document
        collection.
        :return: list of Document.
        """
        for doc in self._cursor:
            yield MongoDocument(doc, self._collection)


class MongoDatabaseCollection(DatabaseCollection):
    """
    Represents a database collection
    """

    def __init__(self, collection: MongoCollection, logger: AppLogger):
        """
        Creates a mongo database collection wrapping a Collection from pymongo.
        :param collection: pymongo.database.collection
        """
        self._mongo_collection = collection
        self._logger = logger

    def __str__(self):
        return str(self._mongo_collection)

    def __repr__(self):
        return f"MongoDatabaseCollection({repr(self._mongo_collection)})"

    def by_id(self, doc_id: str, fields: list[str] | None = None) -> Document | None:
        """
        Get a document by id.
        """
        doc = self._mongo_collection.find_one(
            {"_id": ObjectId(doc_id)}, {field: 1 for field in fields} if fields else None
        )
        if doc is None:
            return None
        return MongoDocument(doc, self)

    def by_key(self, key: str, value: Any, fields: list[str] | None = None) -> Document | None:
        """
        Get a document by key other than id.
        If more than one document is found, the first document in unspecified
        order will be returned.
        Should preferably be used with values that are supposed to be unique.
        """
        doc = self._mongo_collection.find_one({key: value}, {field: 1 for field in fields} if fields else None)
        if doc is None:
            return None
        return MongoDocument(doc, self)

    def add(self, data: dict) -> Document:
        """
        Add a new document to the database.

        :param data: The data for the document.
        :return: The newly created document.
        """
        data = enums_to_string(data)
        result = self._mongo_collection.insert_one(data)
        return self.by_id(result.inserted_id)

    def get_all(self, fields: list[str] | None = None) -> DocumentCollection:
        """
        Get a document collection cursor currently containing all documents
        in the database collection.
        Note that no documents are fetched when calling this method.
        """
        return MongoDocumentCollection(
            self._mongo_collection.find(projection={field: 1 for field in fields} if fields else None), self
        )

    def get(self, filters: dict[str, Any] = None, fields: list[str] | None = None) -> DocumentCollection:
        """
        Get a document collection cursor pointing towards all documents that fit the current filter.
        """
        if filters is None:
            filters = {}
        filters = enums_to_string(filters)
        filters = _convert_str_id_to_object_id(filters)
        self._logger.debug(f"MongoDatabaseCollection.get(filters={filters})")
        cursor = self._mongo_collection.find(filters, {field: 1 for field in fields} if fields else None)
        return MongoDocumentCollection(cursor, self)

    def exists(self, filters: dict[str, Any]) -> bool:
        """
        Check if document matching filter exists.

        :param filters: Filter using mongodb pymongo syntax.
        If filter value contains "id", the parameter name will be converted to "_id" and wrapped in an ObjectId object.

        :return: True if document exists, else False.
        """
        filters = _convert_str_id_to_object_id(filters)
        filters = enums_to_string(filters)
        return self._mongo_collection.count_documents(filters, limit=1) > 0

    def patch_document(self, doc_id: str, updates: dict[str, Any]) -> None:
        """See base class."""
        update_result = self._mongo_collection.update_one({"_id": ObjectId(doc_id)}, {"$set": enums_to_string(updates)})
        _ensure_updated(update_result, doc_id, self._mongo_collection.name)

    def push_to_list(
        self, doc_id: str, sub_collection_path: str, new_sub_collection_value: dict | list | str | int | datetime
    ) -> None:
        """See base class."""
        update_result = self._mongo_collection.update_one(
            {"_id": ObjectId(doc_id)}, {"$push": {sub_collection_path: enums_to_string(new_sub_collection_value)}}
        )
        _ensure_updated(update_result, doc_id, self._mongo_collection.name)

    def update_document(self, doc_id: str, updates: DocumentDatabaseUpdateContext) -> None:
        data = updates.to_implementation_specific_update_syntax()
        data = enums_to_string(data)
        update_result = self._mongo_collection.update_one({"_id": ObjectId(doc_id)}, data)
        _ensure_updated(update_result, doc_id, self._mongo_collection.name)

    def replace(self, doc_id: str, data: dict) -> None:
        """Replaces data for document."""
        data = _convert_str_id_to_object_id(data)
        data = enums_to_string(data)
        self._mongo_collection.replace_one({"_id": ObjectId(doc_id)}, data)

    def delete(self, doc_id: str) -> None:
        """Deletes a document."""
        self._mongo_collection.delete_one({"_id": ObjectId(doc_id)})

    def like(self, field: str, value: str) -> DocumentCollection:
        cursor = self._mongo_collection.find({field: {"$regex": value}})
        return MongoDocumentCollection(cursor, self)


class MongoDocumentDatabase(DocumentDatabase):
    """
    Wrapper for MongoDB database.
    """

    def __init__(self, db: MongoDatabase, logger: AppLogger):
        self._db = db
        self._logger = logger

    def __str__(self):
        return str(self._db)

    def collection(self, collection_name: str) -> DatabaseCollection:
        """
        Gets database collection by name.
        :param collection_name: Name of collection.
        :return: Database collection to perform operations on the selected collection.
        """
        return MongoDatabaseCollection(self._db.get_collection(collection_name), self._logger)

    def transaction(self, datastore, function, *args, **kwargs):
        self._logger.debug(
            f"MongoDocumentDatabase.transaction(self={self}, datastore={datastore}, function={function}, "
            f"*args={args}, **kwargs={kwargs})"
        )

        def callback(session: ClientSession):
            self._logger.debug(f"MongoDocumentDatabase.transaction.callback(session={session})")
            temp_db = self._db
            self._db = session.client.get_database()
            result = function(datastore, *args, **kwargs)
            self._db = temp_db
            return result

        with self._db.client.start_session() as s:
            self._logger.debug("MongoDocumentDatabase.transaction: Starting session...")
            return s.with_transaction(callback)

    def update_context(self) -> DocumentDatabaseUpdateContext:
        return MongoDBUpdateContext()

    def new_id(self) -> str:
        return str(ObjectId())
