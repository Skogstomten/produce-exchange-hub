from typing import Any, Callable, Type, TypeVar, List, Dict
from enum import Enum
from abc import ABCMeta, abstractmethod


class NotSet(Enum):
    not_set = 'NotSet'


T = TypeVar('T')
TOutType = TypeVar('TOutType')


class Document(metaclass=ABCMeta):
    @abstractmethod
    def __getitem__(self, item):
        ...

    @abstractmethod
    def __setitem__(self, key, value):
        ...

    @property
    @abstractmethod
    def id(self) -> str:
        ...

    def to(self, convert: Callable[['Document'], T]) -> T:
        return convert(self)

    @abstractmethod
    def dict(self):
        ...


class DocumentCollection(metaclass=ABCMeta):
    @abstractmethod
    def select_for_each(self, factory: Callable[[Document], Type[T]]) -> List[T]:
        ...
    
    @abstractmethod
    def skip(self, skip: int | None) -> 'DocumentCollection':
        ...
    
    @abstractmethod
    def take(self, take: int | None) -> 'DocumentCollection':
        ...
    
    @abstractmethod
    def sort(self, sort_by: str | None, sort_order: str | None) -> 'DocumentCollection':
        ...


class DatabaseCollection(metaclass=ABCMeta):
    @abstractmethod
    def get_all(self) -> DocumentCollection:
        ...
    
    @abstractmethod
    def get(
        self,
        filters: Dict[str, Any] = None,
    ) -> DocumentCollection:
        ...

    @abstractmethod
    def by_id(self, doc_id: str) -> Document:
        ...
    
    @abstractmethod
    def by_key(self, key: str, value: Any) -> Document | None:
        ...
    
    @abstractmethod
    def exists(self, filters: Dict[str, Any]) -> bool:
        ...

    @abstractmethod
    def add(self, data: Dict) -> Document:
        ...


class DocumentDatabase(metaclass=ABCMeta):
    @abstractmethod
    def collection(self, collection_name: str) -> DatabaseCollection:
        ...
