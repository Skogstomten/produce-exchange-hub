from fastapi import Depends, HTTPException, status
from jose import jwt, JWTError

from .auth import oauth2_scheme_optional, SECRET_KEY, ALGORITHM
from ..models.user import UserInternal
from ..datastores.user_datastore import UserDatastore, get_user_datastore


def get_current_user_if_any(
        token: str | None = Depends(oauth2_scheme_optional),
        users: UserDatastore = Depends(get_user_datastore),
) -> UserInternal | None:
    if token is None:
        return None
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get('sub')
        if email is None:
            raise credentials_exception
    except JWTError:
        # TODO: Log error
        raise credentials_exception
    user = users.get_user(email)
    if user is None:
        raise credentials_exception
    return user
