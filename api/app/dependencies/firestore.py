import functools

from fastapi import Depends
from firebase_admin.credentials import Certificate
from firebase_admin import App as FirebaseApp, initialize_app as init_firebase
from firebase_admin.firestore import client
from google.cloud.firestore_v1 import Client


@functools.lru_cache(None)
def get_firebase_app() -> FirebaseApp:
    credentials = Certificate('./produce-exchange-hub-firebase-adminsdk-ufzci-78e6592558.json')
    options = {"databaseURL": "https://produce-exchange-hub.firebaseio.com"}
    firebase_app = init_firebase(credentials, options, __name__)
    return firebase_app


async def get_db_client(firebase_app: FirebaseApp = Depends(get_firebase_app)) -> Client:
    return client(firebase_app)
