from datetime import timedelta, datetime

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestFormStrict
from jose import jwt

from app.models.v1.token import Token
from app.models.v1.database_models.user_database_model import UserDatabaseModel
from app.datastores.user_datastore import UserDatastore, get_user_datastore
from app.dependencies.auth import ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY, ALGORITHM
from app.oauth2.scopes import Scopes
from app.oauth2.claim import Claim
from app.utils.string_values import StringValues

router = APIRouter(prefix="/v1/token", tags=["Token"])


@router.post("/", response_model=Token)
async def token(
    form_data: OAuth2PasswordRequestFormStrict = Depends(),
    users: UserDatastore = Depends(get_user_datastore),
):
    user = users.authenticate_user(form_data.username, form_data.password)
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    scopes = Scopes(form_data.scopes)
    claims = get_user_claims(user, scopes)
    access_token = create_access_token(
        data={
            "sub": user.email,
            "scopes": form_data.scopes,
            **{claim.type: claim.get_value() for claim in claims},
        },
        expires_delta=access_token_expires,
    )
    return Token(access_token=access_token, token_type="bearer")


def get_user_claims(user: UserDatabaseModel, scopes: Scopes) -> list[Claim]:
    claims = [Claim("verified", user.verified)]
    if scopes.has_scope("profile"):
        claims.extend(
            [
                Claim("email", user.email),
                Claim("given_name", user.firstname),
                Claim("family_name", user.lastname),
            ]
        )
    if scopes.has_scope("roles"):
        roles = []
        for role in user.roles:
            value = role.role_name
            if role.reference is not None:
                value += f":{role.reference}"
            roles.append(value)
        claims.append(Claim("roles", StringValues(*roles)))
    return claims


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    # print('data put in token: ' + str(data))
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
