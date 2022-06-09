from fastapi import Depends, HTTPException, status, Request
from fastapi.security import SecurityScopes
from jose import jwt, JWTError

from app.datastores.user_datastore import UserDatastore, get_user_datastore
from app.errors.unauthorized_error import UnauthorizedError
from app.models.v1.database_models.user_database_model import UserDatabaseModel
from app.models.v1.token import TokenData
from .auth import oauth2_scheme_optional, SECRET_KEY, ALGORITHM


def get_current_user_if_any(
        request: Request,
        security_scopes: SecurityScopes,
        token: str | None = Depends(oauth2_scheme_optional),
        users: UserDatastore = Depends(get_user_datastore),
) -> UserDatabaseModel | None:
    if token is None:
        return None
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = 'Bearer'
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': authenticate_value},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        token_data = TokenData(**payload)
        print(payload)
        email: str = payload.get('sub')
        if email is None:
            raise credentials_exception
    except JWTError:
        # TODO: Log error
        raise credentials_exception
    user = users.get_user(email)
    if user is None:
        raise credentials_exception
    if not user_has_access(security_scopes, request, token_data):
        raise UnauthorizedError
    return user


def get_current_user(
        user: UserDatabaseModel | None = Depends(get_current_user_if_any),
) -> UserDatabaseModel:
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Could not validate credentials',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    return user


def user_has_access(
        security_scopes: SecurityScopes,
        request: Request,
        token: TokenData,
) -> bool:
    if not security_scopes.scopes:
        return True

    has_access = False
    for scope in security_scopes.scopes:
        parts = scope.split(':')
        if len(parts) not in (2, 3):
            raise HTTPException(
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                f"endpoint '{str(request.url)}' has invalid security claim setup: '{scope}'"
            )
        claim_type: str = parts[0]
        if claim_type == 'roles':
            if len(parts) == 2:
                role_name = parts[1]
                if role_name in token.roles:
                    has_access = True
            if len(parts) == 3:
                role_name = parts[1]
                reference_param_name = parts[2].translate(str.maketrans({'{': '', '}': ''}))
                if reference_param_name not in request.path_params:
                    raise HTTPException(
                        status.HTTP_500_INTERNAL_SERVER_ERROR,
                        f"Path param '{reference_param_name}' does not exist"
                    )
                reference = request.path_params.get(reference_param_name)
                if f"{role_name}:{reference}" in token.roles:
                    has_access = True
        elif claim_type == 'verified':
            verified: bool = parts[1].lower() == 'true'
            if verified:
                if not token.verified:
                    return False

    print('User has access: ' + str(has_access))
    return has_access
