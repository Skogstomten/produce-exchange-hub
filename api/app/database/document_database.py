from typing import Any, Callable, TypeVar, NoReturn
from enum import Enum
from abc import ABCMeta, abstractmethod
from collections.abc import MutableMapping


class NotSet(Enum):
    not_set = "NotSet"


T = TypeVar("T")
TOutType = TypeVar("TOutType")


class Document(MutableMapping, metaclass=ABCMeta):
    @abstractmethod
    def __getitem__(self, item):
        ...

    @abstractmethod
    def __setitem__(self, key, value):
        ...

    @abstractmethod
    def __delitem__(self, key):
        ...

    @abstractmethod
    def __iter__(self):
        ...

    @abstractmethod
    def __len__(self):
        ...

    @property
    @abstractmethod
    def id(self) -> str:
        ...

    def to(self, convert: Callable[["Document"], T]) -> T:
        return convert(self)

    @abstractmethod
    def to_dict(self) -> dict:
        ...

    @abstractmethod
    def replace(self, data: MutableMapping) -> "Document":
        ...

    @abstractmethod
    def delete(self) -> NoReturn:
        ...


class DocumentCollection(metaclass=ABCMeta):
    @abstractmethod
    def to_list(self) -> list[Document]:
        ...

    @abstractmethod
    def skip(self, skip: int | None) -> "DocumentCollection":
        ...

    @abstractmethod
    def take(self, take: int | None) -> "DocumentCollection":
        ...

    @abstractmethod
    def sort(
        self, sort_by: str | None, sort_order: str | None
    ) -> "DocumentCollection":
        ...


class DatabaseCollection(metaclass=ABCMeta):
    @abstractmethod
    def get_all(self) -> DocumentCollection:
        ...

    @abstractmethod
    def get(
        self,
        filters: dict[str, Any] | None = None,
    ) -> DocumentCollection:
        ...

    @abstractmethod
    def by_id(self, doc_id: str) -> Document | None:
        ...

    @abstractmethod
    def by_key(self, key: str, value: Any) -> Document | None:
        ...

    @abstractmethod
    def exists(self, filters: dict[str, Any]) -> bool:
        ...

    @abstractmethod
    def add(self, data: dict) -> Document:
        ...


class DocumentDatabase(metaclass=ABCMeta):
    @abstractmethod
    def collection(self, collection_name: str) -> DatabaseCollection:
        ...
