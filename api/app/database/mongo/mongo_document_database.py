from bson import ObjectId
from pymongo import ASCENDING, DESCENDING
from pymongo.collection import Collection as MongoCollection
from pymongo.cursor import Cursor
from pymongo.database import Database as MongoDatabase

from ..document_database import *
from ...utils.enum_utils import enums_to_string

TOutType = TypeVar('TOutType')


class MongoDocument(Document):
    _doc: dict
    _collection: MongoCollection

    def __init__(self, doc: dict, collection: MongoCollection):
        super().__init__()
        self._doc = doc
        self._collection = collection

    def __getitem__(self, item):
        return self._doc[item]

    def __setitem__(self, key, value):
        self._doc[key] = value

    @property
    def id(self) -> str:
        return str(self._doc['_id'])

    def to_dict(self) -> dict:
        return self._doc

    def replace(self, data: dict) -> Document:
        data = enums_to_string(data)
        self._collection.replace_one(
            {'_id': ObjectId(self.id)},
            data,
        )
        return MongoDocument(self._collection.find_one({'_id': ObjectId(self.id)}), self._collection)


class MongoDocumentCollection(DocumentCollection):
    _cursor: Cursor
    _collection: MongoCollection

    def __init__(self, cursor: Cursor, collection: MongoCollection):
        self._cursor = cursor
        self._collection = collection
    
    def skip(self, skip: int | None) -> 'DocumentCollection':
        if skip is not None:
            self._cursor = self._cursor.skip(skip)
        return self
    
    def take(self, take: int | None) -> 'DocumentCollection':
        if take is not None:
            self._cursor = self._cursor.limit(take)
        return self
    
    def sort(self, sort_by: str | None, sort_order: str | None) -> 'DocumentCollection':
        if sort_by is not None:
            order = ASCENDING
            if sort_order == 'desc':
                order = DESCENDING
            self._cursor = self._cursor.sort(sort_by, order)
        return self

    def select_for_each(self, factory: Callable[[Document], Type[T]]) -> List[T]:
        for doc in self._cursor:
            yield factory(MongoDocument(doc, self._collection))

    def to_list(self) -> list[Document]:
        for doc in self._cursor:
            yield MongoDocument(doc, self._collection)


class MongoDatabaseCollection(DatabaseCollection):
    _collection: MongoCollection

    def __init__(self, collection: MongoCollection):
        self._collection = collection

    def by_id(self, doc_id: str) -> Document | None:
        doc = self._collection.find_one({'_id': ObjectId(doc_id)})
        if doc is None:
            return None
        return MongoDocument(doc, self._collection)
    
    def by_key(self, key: str, value: Any) -> Document | None:
        doc = self._collection.find_one({key: value})
        if doc is None:
            return None
        return MongoDocument(
            self._collection.find_one({key: value}),
            self._collection
        )

    def add(self, data: Dict) -> Document:
        result = self._collection.insert_one(data)
        return self.by_id(result.inserted_id)

    def get_all(self) -> DocumentCollection:
        return MongoDocumentCollection(
            self._collection.find(),
            self._collection
        )
    
    def get(
        self,
        filters: Dict[str, Any] = None,
    ) -> DocumentCollection:
        if filters is None:
            filters = {}
        cursor = self._collection.find(filters)
        return MongoDocumentCollection(cursor, self._collection)
    
    def exists(self, filters: Dict[str, Any]) -> bool:
        return self._collection.count_documents(filters, limit=1) > 0


class MongoDocumentDatabase(DocumentDatabase):
    _db: MongoDatabase

    def __init__(self, db: MongoDatabase):
        self._db = db

    def collection(self, collection_name: str) -> DatabaseCollection:
        return MongoDatabaseCollection(
            self._db.get_collection(collection_name)
        )
