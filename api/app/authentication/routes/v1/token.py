"""
Routing module for oauth2 token endpoint.
"""
from datetime import timedelta

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestFormStrict
from jose import jwt
from pytz import utc
from sqlalchemy import Engine, select
from sqlalchemy.orm import Session

from app.authentication.dependencies.auth import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    SECRET_KEY,
    ALGORITHM,
)
from app.authentication.errors.invalid_username_or_password_error import InvalidUsernameOrPasswordError
from app.authentication.models.db.users import User
from app.authentication.models.v1.token import Token
from app.authentication.oauth2.claim import Claim
from app.authentication.oauth2.scopes import Scopes
from app.database.dependencies.mysql import get_sqlalchemy_engine
from app.shared.cryptography import password_hasher as hasher

router = APIRouter(prefix="/v1/token", tags=["Token"])


@router.post("/", response_model=Token)
async def token(
    form_data: OAuth2PasswordRequestFormStrict = Depends(),
    db: Engine = Depends(get_sqlalchemy_engine)
) -> Token:
    """Gets oauth2 access token."""
    with Session(db) as session:
        user = session.scalar(select(User).where(User.username == form_data.username))
        if user is None:
            raise InvalidUsernameOrPasswordError()
        if user.password_hash == hasher.is_correct_password(form_data.password, user.password_hash):
            raise InvalidUsernameOrPasswordError()
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        scopes = Scopes(form_data.scopes)
        claims = get_user_claims(user, scopes)
        access_token = create_access_token(
            data={
                "sub": user.email,
                "scopes": form_data.scopes,
                "id": user.id,
                **{claim.type: claim.get_value() for claim in claims},
            },
            expires_delta=access_token_expires,
        )
        return Token(access_token=access_token, token_type="bearer")


def get_user_claims(user: User, scopes: Scopes) -> list[Claim]:
    """
    Get claims for user according to provided scopes.
    :param user: user to get claims for.
    :param scopes: scopes requested by caller.
    :return: list of claims.
    """
    claims = [Claim("verified", user.verified)]
    if scopes.has_scope("profile"):
        claims.extend(
            [
                Claim("email", user.email),
                Claim("given_name", user.firstname),
                Claim("family_name", user.lastname),
            ]
        )
    # if scopes.has_scope("roles"):
    #     claims.append(Claim("roles", StringValues(*user.roles)))
    return claims


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """
    Creates jwt encoded oauth2 access token.
    :param data: Data to put in token.
    :param expires_delta: expiration time of token.
    :return: jwt token as str.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = utc + expires_delta
    else:
        expire = utc + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
