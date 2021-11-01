from fastapi import Depends

from firebase_admin.auth import Client
from firebase_admin import App

from .firestore import get_firebase_app


def get_auth_client(
        app: App = Depends(get_firebase_app)
) -> Client:
    return Client(app)
