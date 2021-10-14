from google.cloud.firestore_v1.client import Client


class BaseDatastore(object):
    db: Client

    def __init__(self, db: Client):
        self.db = db

    def get_localization(self, document_key: str) -> dict[str, str]:
        document_snapshot = self.db.collection('localization').document(document_key).get()
        if document_snapshot.exists:
            return document_snapshot.to_dict()
        return {}
