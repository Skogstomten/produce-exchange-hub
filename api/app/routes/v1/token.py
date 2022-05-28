from datetime import timedelta, datetime

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestFormStrict
from jose import jwt

from ...models.v1.token import Token
from ...datastores.user_datastore import UserDatastore, get_user_datastore
from ...dependencies.auth import ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY, ALGORITHM
from ...oauth2.scopes import Scopes

router = APIRouter(prefix='/v1/token')


@router.post('/', response_model=Token)
async def token(
        form_data: OAuth2PasswordRequestFormStrict = Depends(),
        users: UserDatastore = Depends(get_user_datastore),
):
    user = users.authenticate_user(form_data.username, form_data.password)
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    scopes = Scopes(form_data.scopes)
    claims = users.get_claims(user, scopes)
    access_token = create_access_token(
        data={
            'sub': user.email,
            'scopes': form_data.scopes,
        },
        expires_delta=access_token_expires
    )
    return Token(
        access_token=access_token,
        token_type='bearer'
    )


def create_access_token(
        data: dict,
        expires_delta: timedelta | None = None
) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
