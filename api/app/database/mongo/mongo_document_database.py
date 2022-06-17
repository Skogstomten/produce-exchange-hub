"""
MongoDb implementation of document database interface
"""
from collections.abc import MutableMapping, Iterable
from typing import Any

from bson import ObjectId
from pymongo import ASCENDING, DESCENDING
from pymongo.collection import Collection as MongoCollection
from pymongo.cursor import Cursor
from pymongo.database import Database as MongoDatabase

from app.errors.invalid_operation_error import InvalidOperationError
from ..document_database import (
    Document,
    DocumentDatabase,
    DocumentCollection,
    DatabaseCollection,
)
from ...utils.enum_utils import enums_to_string


class MongoDocument(Document):
    """
    Mongo db document.
    """

    _doc: dict
    _collection: MongoCollection

    def __init__(self, doc: dict, collection: MongoCollection):
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
        clone.update({"id": self.id})
        return clone.__iter__()

    def __len__(self) -> int:
        """
        Returns number of fields in document.
        :return: Number of fields as int.
        """
        return self._doc.__len__()

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
        data = self._doc.copy()
        data["id"] = self.id
        del data["_id"]
        return data

    def replace(self, data: MutableMapping) -> Document:
        """
        Replaces document data with given data and gives back the updated
        document.
        :param data: Updated data as a mutable mapping.
        :return: Updated document.
        """
        if isinstance(data, Document):
            data = data.to_dict()

        data = enums_to_string(data)
        if "id" in data:
            data["_id"] = self._doc["_id"]
            del data["id"]
        self._collection.replace_one(
            {"_id": ObjectId(self.id)},
            data,
        )
        return MongoDocument(
            self._collection.find_one({"_id": ObjectId(self.id)}),
            self._collection,
        )

    def delete(self) -> None:
        """
        delete document from database.
        :return:
        """
        self._collection.delete_one({"_id": self._doc.get("_id")})


class MongoDocumentCollection(DocumentCollection):
    """
    A collection of documents.
    Technically wraps a mongodb cursor to be able to filter selection before
    fetching all data.
    """

    _cursor: Cursor
    _collection: MongoCollection

    def __init__(self, cursor: Cursor, collection: MongoCollection) -> None:
        """
        Creates a mongo document collection.
        :param cursor: Reference to db cursor.
        :param collection: Reference to db collection
        """
        self._cursor = cursor
        self._collection = collection

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

    def sort(
        self, sort_by: str | None, sort_order: str | None
    ) -> "DocumentCollection":
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

    _collection: MongoCollection

    def __init__(self, collection: MongoCollection):
        """
        Creates a mongo database collection wrapping a Collection from pymongo.
        :param collection: pymongo.database.collection
        """
        self._collection = collection

    def by_id(self, doc_id: str) -> Document | None:
        """
        Get a document by id.
        :param doc_id: id of document.
        :return: Document with id or None if no document is found.
        """
        doc = self._collection.find_one({"_id": ObjectId(doc_id)})
        if doc is None:
            return None
        return MongoDocument(doc, self._collection)

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
        doc = self._collection.find_one({key: value})
        if doc is None:
            return None
        return MongoDocument(
            self._collection.find_one({key: value}), self._collection
        )

    def add(self, data: dict) -> Document:
        """
        Add a new document to the database.

        :param data: The data for the document.
        :return: The newly created document.
        """
        data = enums_to_string(data)
        result = self._collection.insert_one(data)
        return self.by_id(result.inserted_id)

    def get_all(self) -> DocumentCollection:
        """
        Get a document collection cursor currently containing all documents
        in the database collection.
        Note that no documents are fetched when calling this method.
        :return: DocumentCollection operating as a cursor.
        """
        return MongoDocumentCollection(
            self._collection.find(), self._collection
        )

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
        cursor = self._collection.find(filters)
        return MongoDocumentCollection(cursor, self._collection)

    def exists(self, filters: dict[str, Any]) -> bool:
        """
        Check if document matching filter exists.
        :param filters: Filter using mongodb pymongo syntax.
        :return: True if document exists, else False.
        """
        return self._collection.count_documents(filters, limit=1) > 0


class MongoDocumentDatabase(DocumentDatabase):
    """
    Wrapper for MongoDB database.
    """

    _db: MongoDatabase

    def __init__(self, db: MongoDatabase):
        """
        Creates a MongoDb wrapper.
        :param db:
        """
        self._db = db

    def collection(self, collection_name: str) -> DatabaseCollection:
        """
        Gets database collection by name.
        :param collection_name: Name of collection.
        :return: Database collection to perform operations on the selected
        collection.
        """
        return MongoDatabaseCollection(
            self._db.get_collection(collection_name)
        )
