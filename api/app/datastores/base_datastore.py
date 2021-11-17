from enum import Enum
from typing import List, Dict, TypeVar, Generic, Iterable, Tuple, Callable, NoReturn

from pymongo.database import Database
from pymongo.collection import Collection

from app.errors.not_found_error import NotFoundError


class Localization(Enum):
    company_statuses = 'company_statuses'
    company_types = 'company_types'
    address_types = 'address_types'
    countries_iso_name = 'countries_iso_name'
    languages_iso_name = 'languages_iso_name'
    contact_types = 'contact_types'
    produce_types = 'produce_types'
    unit_types = 'unit_types'
    period_types = 'period_types'
    delivery_options = 'delivery_options'


def localize(
        data: Dict[str, str | Dict[str, str]],
        language: str,
        company_languages: List[str],
        default: str | Dict = None
) -> str | Dict[str, str]:
    if data is None:
        return default

    if language in data:
        return data.get(language)

    for language in company_languages:
        if language in data:
            return data.get(language)

    return default


TOut = TypeVar('TOut')
CollectionDocKeyPair = Tuple[Tuple[str, str | None]]


class BaseDatastore(Generic[TOut]):
    db: Database
    _collection_name: str

    def __init__(self, db: Database, collection_name: str):
        self.db = db
        self._collection_name = collection_name

    def get_all(
            self,
            create: Callable[[DocumentSnapshot], TOut],
            parent_doc_id: str | None = None,
            sub_collections: CollectionDocKeyPair | None = None
    ) -> List[TOut]:
        collection: Collection = self.db.get_collection(self._collection_name)
        if parent_doc_id is not None and sub_collections is not None and len(sub_collections) > 0:
            doc_ref: DocumentReference = collection_ref.document(parent_doc_id)
            for sub_collection in sub_collections:
                collection_ref = doc_ref.collection(sub_collection[0])
                if sub_collection[1] is not None:
                    doc_ref = collection_ref.document(sub_collection[1])
        snapshots: List[DocumentSnapshot] = collection_ref.get()
        for snapshot in snapshots:
            yield create(snapshot)

    def get(
            self,
            document_key: str,
            create: Callable[[str, Dict], TOut]
    ) -> TOut:
        ref, snapshot = self._get_ref_and_snapshot(document_key)
        data = snapshot.to_dict()
        return create(ref.id, data)

    def add(self, data_factory: Callable[..., dict], create: Callable[[str, Dict], TOut]) -> TOut:
        ref = self.db.collection(self._collection_name).document()
        ref.create(data_factory())
        return self.get(ref.id, create)

    def update(self, document_key: str, data_factory: Callable[..., dict], create: Callable[[str, Dict], TOut]) -> TOut:
        ref, snapshot = self._get_ref_and_snapshot(document_key)
        ref.set(data_factory())
        return self.get(ref.id, lambda data: create)

    def delete(self, document_key) -> NoReturn:
        ref, snapshot = self._get_ref_and_snapshot(document_key)
        ref.delete()

    def localize_from_document(
            self,
            localization: Localization,
            key: str,
            language: str,
            company_languages: List[str]
    ) -> str | None:
        if key is None:
            return None

        snapshot = self.db.collection('localization').document(localization.value).get()
        if snapshot.exists:
            data = snapshot.to_dict()
            if key in data:
                localizations = data.get(key)
                if language in localizations:
                    return localizations.get(language)

                for language in company_languages:
                    if language in localizations:
                        return localizations.get(language)

        return key

    def get_user_ref(self, user_id: str):
        user_ref = self.db.collection('users').document(user_id)
        if not user_ref.get().exists:
            raise NotFoundError(f"User with id '{user_id}' is not found")

        return user_ref

    def _get_ref_and_snapshot(
            self,
            document_key: str,
            field_paths: Iterable[str] | None = None,
            parent_doc_ref: DocumentReference | None = None,
            sub_collection_name: str | None = None
    ) -> Tuple[DocumentReference, DocumentSnapshot]:
        ref: DocumentReference
        if parent_doc_ref is not None and sub_collection_name:
            ref = parent_doc_ref.collection(sub_collection_name).document(document_key)
        else:
            ref = self.db.collection(self._collection_name).document(document_key)
        snapshot = ref.get(field_paths)
        if not snapshot.exists:
            raise NotFoundError(f"Document with id '{document_key} is not found")
        return ref, snapshot
