from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from ..models.v1.user import User, fake_decode_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')


async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    user = fake_decode_token(token)
    return user
