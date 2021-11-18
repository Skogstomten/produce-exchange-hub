from bson import ObjectId
from pymongo.database import Database as MongoDatabase
from pymongo.collection import Collection as MongoCollection
from pymongo.cursor import Cursor

from ..document_database import *


TOutType = TypeVar('TOutType')


class MongoDocument(Document):
    _doc: Dict

    def __init__(self, doc: Dict):
        super().__init__()
        self._doc = doc

    @property
    def id(self) -> str:
        return str(self._doc['_id'])

    def get(self, return_type: Type[TOutType], key: str, default: TOutType | NotSet = NotSet.not_set) -> TOutType:
        if default == NotSet.not_set:
            return self._doc.get(key)
        return self._doc.get(key, default)


class MongoDocumentCollection(DocumentCollection):
    _cursor: Cursor

    def __init__(self, cursor: Cursor):
        self._cursor = cursor

    def select_for_each(self, factory: Callable[[Document], Type[T]]) -> List[T]:
        for doc in self._cursor:
            yield factory(MongoDocument(doc))


class MongoDatabaseCollection(DatabaseCollection):
    _collection: MongoCollection

    def __init__(self, collection: MongoCollection):
        self._collection = collection

    def by_id(self, doc_id: str) -> Document:
        return MongoDocument(self._collection.find_one({'_id': ObjectId(doc_id)}))

    def add(self, data: Dict) -> Document:
        doc_id = self._collection.insert_one(data)
        return self.by_id(doc_id)

    def get_all(self) -> DocumentCollection:
        return MongoDocumentCollection(
            self._collection.find()
        )


class MongoDocumentDatabase(DocumentDatabase):
    _db: MongoDatabase

    def __init__(self, db: MongoDatabase):
        self._db = db

    def collection(self, collection_name: str) -> DatabaseCollection:
        return MongoDatabaseCollection(
            self._db.get_collection(collection_name)
        )
