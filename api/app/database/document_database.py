"""
Interface for document database.
"""
from abc import ABCMeta, abstractmethod
from collections.abc import MutableMapping
from enum import Enum
from typing import Any, Callable, TypeVar

from app.dependencies.log import AppLoggerInjector

logger_injector = AppLoggerInjector("document_database")
logger = logger_injector()


class NotSet(Enum):
    """
    Not set enum constant.
    """

    NOT_SET = "NotSet"


T = TypeVar("T")
OutT = TypeVar("OutT")


class DocumentDatabaseUpdateContext(metaclass=ABCMeta):
    @abstractmethod
    def set_values(self, value_dict: dict[str, Any]) -> None:
        """
        Dict of key value pairs with key being the database field to update
        and value being the new value for given field.
        """

    @abstractmethod
    def push_to_list(self, list_name: str, data: Any) -> None:
        """Append given data to document sub collection of list_name."""

    @abstractmethod
    def to_implementation_specific_update_syntax(self) -> Any:
        """To be called by database implementation to get the update context converted to the syntax it requires."""


class Document(MutableMapping, metaclass=ABCMeta):
    """
    Representation of a document.
    Can be accessed like a dict.
    """

    @abstractmethod
    def __getitem__(self, item):
        """
        Get item from doc.
        :param item: The item to get.
        :return: An item.
        """

    @abstractmethod
    def __setitem__(self, key, value):
        """
        Set item in the doc.
        :param key: Key of item to set.
        :param value: New value for item.
        :return: None.
        """

    @abstractmethod
    def __delitem__(self, key):
        """
        Deletes an item from the doc.
        :param key: Key of item to delete.
        :return: None.
        """

    @abstractmethod
    def __iter__(self):
        """
        Iterate items in the doc.
        :return: Iterator for the doc.
        """

    @abstractmethod
    def __len__(self):
        """
        Get the number of items for the doc.
        :return: Number of items as int.
        """

    @property
    @abstractmethod
    def id(self) -> str:
        """
        Easy accessor prop for doc id.
        :return: id as str.
        """

    def to(self, convert: Callable[["Document"], T]) -> T:
        """
        Convinience method to convert doc to another type with converter
        passed as argument.
        :param convert: Converter function.
        :return: Type converted to by the callable.
        """
        return convert(self)

    @abstractmethod
    def to_dict(self) -> dict:
        """
        Returns a dict with the same data as in the document.
        :return: Doc as dict.
        """

    @abstractmethod
    def replace(self, data: MutableMapping) -> "Document":
        """
        Replace data in document.
        :param data: Data to replace with.
        :return: The updated document.
        """

    @abstractmethod
    def delete(self) -> None:
        """
        Delete the document from database.
        :return: None.
        """


class DocumentCollection(metaclass=ABCMeta):
    """
    A cursor to a collection of documents.
    """

    @abstractmethod
    def to_list(self) -> list[Document]:
        """
        Converts the cursor to an in memory list of documents.
        :return: List of Document.
        """

    @abstractmethod
    def skip(self, skip: int | None) -> "DocumentCollection":
        """
        Skip a number of documents.
        :param skip: Number to skip.
        :return: Updated cursor.
        """

    @abstractmethod
    def take(self, take: int | None) -> "DocumentCollection":
        """
        Take only a certain number of documents.
        :param take: The number to take.
        :return: Updated cursor.
        """

    @abstractmethod
    def sort(self, sort_by: str | None, sort_order: str | None) -> "DocumentCollection":
        """
        Sort the documents in the cursor.
        :param sort_by: field to sort by.
        :param sort_order: asc or desc.
        :return: Updated cursor.
        """


class DatabaseCollection(metaclass=ABCMeta):
    """
    Referencing a collection in the database.
    """

    @abstractmethod
    def get_all(self, fields: list[str] | None = None) -> DocumentCollection:
        """
        Get a cursor for all documents in the collection.
        :param fields: The fields to select from the documents. If None, all fields are returned.
        :return: DocumentCollection cursor wrapper.
        """

    @abstractmethod
    def get(
        self,
        filters: dict[str, Any] | None = None,
        fields: list[str] | None = None,
    ) -> DocumentCollection:
        """
        Get a cursor for all documents fitting the filter from the collection.
        :param filters: Syntax depends on the implementation.
        :param fields: The fields to select from the documents. If None, all fields are returned.
        :return: DocumentCollection cursor wrapper.
        """

    @abstractmethod
    def by_id(self, doc_id: str, fields: list[str] | None = None) -> Document | None:
        """
        Get a document by its document id.
        :param doc_id: The id of the document.
        :param fields: The fields to select from the document. If None, all fields are returned.
        :return: The document or None if no document was found.
        """

    @abstractmethod
    def by_key(self, key: str, value: Any, fields: list[str] | None = None) -> Document | None:
        """
        Get document by key other than id.
        :param key: Name of the field to use as key.
        :param value: Value of the key field.
        :param fields: The fields to select from the document. If None, all fields are returned.
        :return: Document or None if no document was found.
        """

    @abstractmethod
    def exists(self, filters: dict[str, Any]) -> bool:
        """
        Check if document exists.
        :param filters: Filter parameters to specify conditions for search.
        :return: True or False.
        """

    @abstractmethod
    def add(self, data: dict) -> Document:
        """
        Add a document to the collection.
        :param data: The data to put in the document.
        :return: The created document.
        """

    @abstractmethod
    def patch_document(self, doc_id: str, updates: dict[str, Any]) -> None:
        """
        Updates the specified fields for document with given id.
        :param doc_id:

        :param updates:
        fields_to_update = {
            "field_name": var_with_value,
            "sub_doc.sub_doc_field_name": whatever_thing_that_has,
        }

        :return: None

        :raise app.errors.NotFoundError:
        If there's no document with the given key
        """

    @abstractmethod
    def push_to_list(self, doc_id: str, sub_collection_path: str, new_sub_collection_value: Any) -> None:
        """
        Adds sub document to sub collection of document.

        :param doc_id: ID of document containing sub collection.
        :param sub_collection_path: Path to sub collection. IE: name_of_subcollection
        :param new_sub_collection_value: Value to add to sub collection.
        :return: None.

        :raise NotFoundError: If no document with doc_id exists.
        """

    @abstractmethod
    def update_document(self, doc_id: str, updates: DocumentDatabaseUpdateContext) -> None:
        """Updates individual document."""


class DocumentDatabase(metaclass=ABCMeta):
    """
    Database wrapper.
    """

    @abstractmethod
    def collection(self, collection_name: str) -> DatabaseCollection:
        """
        Gets a database collection by name.
        :param collection_name: Name of collection.
        :return: DatabaseCollection.
        """

    @abstractmethod
    def transaction(self, datastore, function, *args, **kwargs):
        """Creates a transaction of function. To be used as decorator."""

    @abstractmethod
    def update_context(self) -> DocumentDatabaseUpdateContext:
        """Returns an update context use to build update queries."""


def transaction(function):
    def wrapper(self: "BaseDatastore", *args, **kwargs):
        logger.debug(f"transaction decorator is called. self={self}, *args={args}, **kwargs={kwargs}")
        return self.db.transaction(self, function, *args, **kwargs)

    return wrapper


class BaseDatastore:
    def __init__(self, db: DocumentDatabase):
        self.db = db
