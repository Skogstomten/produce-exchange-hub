"""
Interface for document database.
"""
from abc import ABCMeta, abstractmethod
from collections.abc import MutableMapping
from enum import Enum
from typing import Any, Callable, TypeVar


class NotSet(Enum):
    """
    Not set enum constant.
    """

    NOT_SET = "NotSet"


T = TypeVar("T")
OutT = TypeVar("OutT")


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
    def sort(
        self, sort_by: str | None, sort_order: str | None
    ) -> "DocumentCollection":
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
    def get_all(self) -> DocumentCollection:
        """
        Get a cursor for all documents in the collection.
        :return: DocumentCollection cursor wrapper.
        """

    @abstractmethod
    def get(
        self,
        filters: dict[str, Any] | None = None,
    ) -> DocumentCollection:
        """
        Get a cursor for all documents fitting the filter from the collection.
        :param filters: Syntax depends on the implementation.
        :return: DocumentCollection cursor wrapper.
        """

    @abstractmethod
    def by_id(self, doc_id: str) -> Document | None:
        """
        Get a document by its document id.
        :param doc_id: The id of the document.
        :return: The document or None if no document was found.
        """

    @abstractmethod
    def by_key(self, key: str, value: Any) -> Document | None:
        """
        Get document by key other than id.
        :param key: Name of the field to use as key.
        :param value: Value of the key field.
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
