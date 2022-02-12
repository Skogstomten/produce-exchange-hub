from typing import Dict

from fastapi import Header, Depends, HTTPException

from .firebase_auth import get_auth_client, Client


class AuthHeader(object):
    id_token: str
    token_data: Dict

    def __init__(self, id_token: str, token_data: Dict):
        self.id_token = id_token
        self.token_data = token_data


def get_auth_header(
        id_token: str = Header(...),
        auth: Client = Depends(get_auth_client)
) -> AuthHeader:
    try:
        token_data = auth.verify_id_token(id_token, True)
        return AuthHeader(id_token, token_data)
    except Exception as ex:
        raise HTTPException(500, str(ex))
