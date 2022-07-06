"""
MongoDb implementation of document database interface
"""
from collections.abc import MutableMapping, Iterable
from datetime import datetime
from typing import Any

from bson import ObjectId
from pymongo import ASCENDING, DESCENDING
from pymongo.client_session import ClientSession
from pymongo.collection import Collection as MongoCollection
from pymongo.cursor import Cursor
from pymongo.database import Database as MongoDatabase

from ..document_database import (
    Document,
    DocumentDatabase,
    DocumentCollection,
    DatabaseCollection,
)
from ...dependencies.log import AppLogger
from ...errors import InvalidOperationError, NotFoundError
from ...utils.enum_utils import enums_to_string


def _convert_str_id_to_object_id(data: dict) -> dict:
    """Converts data dict id field to mongodb _id field."""
    data = data.copy()
    if "id" in data:
        temp_id = data["id"]
        data["_id"] = ObjectId(temp_id)
        del data["id"]
    return data


def _convert_object_id_to_str_id(data: dict) -> dict:
    data = data.copy()
    if "_id" in data:
        temp_obj_id = data["_id"]
        data["id"] = str(temp_obj_id)
        del data["_id"]
    return data


def _ensure_updated(update_result, doc_id, collection_name):
    if update_result.modified_count < 1:
        raise NotFoundError(f"No document with key='{doc_id}' " f"was found in collection='{collection_name}'")


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
        return self._collection.by_id(self.id)

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

    def __init__(self, collection: MongoCollection):
        """
        Creates a mongo database collection wrapping a Collection from pymongo.
        :param collection: pymongo.database.collection
        """
        self.mongo_collection = collection

    def __str__(self):
        return str(self.mongo_collection)

    def __repr__(self):
        return f"MongoDatabaseCollection({repr(self.mongo_collection)})"

    def by_id(self, doc_id: str) -> Document | None:
        """
        Get a document by id.
        :param doc_id: id of document.
        :return: Document with id or None if no document is found.
        """
        doc = self.mongo_collection.find_one({"_id": ObjectId(doc_id)})
        if doc is None:
            return None
        return MongoDocument(doc, self)

    def by_key(self, key: str, value: Any) -> Document | None:
        """
        Get a document by key other than id.
        If more than one document is found, the first document in unspecified
        order will be returned.
        Should preferably be used with values that are supposed to be unique.

        :param key: Lookup key.
        :param value: Lookup value.
        :return: Document or None if no document is found.
        """
        doc = self.mongo_collection.find_one({key: value})
        if doc is None:
            return None
        return MongoDocument(self.mongo_collection.find_one({key: value}), self)

    def add(self, data: dict) -> Document:
        """
        Add a new document to the database.

        :param data: The data for the document.
        :return: The newly created document.
        """
        data = enums_to_string(data)
        result = self.mongo_collection.insert_one(data)
        return self.by_id(result.inserted_id)

    def get_all(self) -> DocumentCollection:
        """
        Get a document collection cursor currently containing all documents
        in the database collection.
        Note that no documents are fetched when calling this method.
        :return: DocumentCollection operating as a cursor.
        """
        return MongoDocumentCollection(self.mongo_collection.find(), self)

    def get(
        self,
        filters: dict[str, Any] = None,
    ) -> DocumentCollection:
        """
        Get a document collection cursor pointing towards all documents that
        fit the current filter.
        :param filters: Filters using mongodb pymongo syntax.
        :return: DocumentCollection cursor.
        """
        if filters is None:
            filters = {}
        filters = enums_to_string(filters)
        filters = _convert_str_id_to_object_id(filters)
        cursor = self.mongo_collection.find(filters)
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
        return self.mongo_collection.count_documents(filters, limit=1) > 0

    def patch_document(self, doc_id: str, updates: dict[str, Any]) -> None:
        """See base class."""
        update_result = self.mongo_collection.update_one({"_id": ObjectId(doc_id)}, {"$set": enums_to_string(updates)})
        _ensure_updated(update_result, doc_id, self.mongo_collection.name)

    def add_to_sub_collection(
        self, doc_id: str, sub_collection_path: str, new_sub_collection_value: dict | list | str | int | datetime
    ) -> None:
        """See base class."""
        update_result = self.mongo_collection.update_one(
            {"_id": ObjectId(doc_id)}, {"$push": {sub_collection_path: enums_to_string(new_sub_collection_value)}}
        )
        _ensure_updated(update_result, doc_id, self.mongo_collection.name)

    def replace(self, doc_id: str, data: dict) -> None:
        """Replaces data for document."""
        data = _convert_str_id_to_object_id(data)
        data = enums_to_string(data)
        self.mongo_collection.replace_one({"_id": ObjectId(doc_id)}, data)

    def delete(self, doc_id: str) -> None:
        """Deletes a document."""
        self.mongo_collection.delete_one({"_id": ObjectId(doc_id)})


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
        return MongoDatabaseCollection(self._db.get_collection(collection_name))

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
