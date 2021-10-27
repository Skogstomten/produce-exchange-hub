from enum import Enum
from typing import List, Dict, TypeVar, Generic, Iterable, Tuple, Callable, NoReturn

from google.cloud.firestore_v1 import DocumentReference, DocumentSnapshot
from google.cloud.firestore_v1.client import Client

from app.errors.not_found_error import NotFoundError


class Localization(Enum):
    company_statuses = 'company_statuses'
    address_types = 'address_types'
    countries_iso_name = 'countries_iso_name'
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


class BaseDatastore(Generic[TOut]):
    db: Client
    _collection_name: str

    def __init__(self, db: Client, collection_name: str):
        self.db = db
        self._collection_name = collection_name

    def get_all(self, create: Callable[[DocumentSnapshot], TOut]) -> List[TOut]:
        snapshots = self.db.collection(self._collection_name).get()
        for snapshot in snapshots:
            yield create(snapshot)

    def get(self, document_key: str, create: Callable[[str, Dict], TOut]) -> TOut:
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
            field_paths: Iterable[str] | None = None
    ) -> Tuple[DocumentReference, DocumentSnapshot]:
        ref = self.db.collection(self._collection_name).document(document_key)
        snapshot = ref.get(field_paths)
        if not snapshot.exists:
            raise NotFoundError(f"Document with id '{document_key} is not found")
        return ref, snapshot
