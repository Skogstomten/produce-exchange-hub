from fastapi import Depends, HTTPException, status, Request
from fastapi.security import SecurityScopes
from jose import jwt, JWTError

from app.datastores.user_datastore import UserDatastore, get_user_datastore
from app.models.v1.database_models.user_database_model import UserDatabaseModel
from app.models.v1.token import TokenData
from app.utils.request_utils import get_current_request_url_with_additions
from .auth import oauth2_scheme_optional, SECRET_KEY, ALGORITHM


class SecurityScopeRestrictions(object):
    """
    Parses and strictures the scope restrictions set on endpoint for easy verification
    """
    def __init__(self, security_scopes: SecurityScopes, request: Request):
        """
        Parses and stores the security scopes
        :param security_scopes: SecurityScopes object received from fastapi
        :param request: HTTP request object, needed to acquire resource keys to check for access to specific resources
        """
        self._roles: list[str] = []

        for scope in security_scopes.scopes:
            parts: list[str] = scope.split(':')
            _ensure_correct_scopes_format(scope, parts, request)
            claim_type: str = parts[0]
            if claim_type == 'roles':
                role_name: str = parts[1]
                reference: str | None = None
                if len(parts) == 3:
                    reference_name: str = parts[3].translate({'{': '', '}': ''})
                    if reference_name in request.path_params:
                        reference = request.path_params.get(reference_name)
                role: str = f"roles:{role_name}"
                if reference is not None:
                    role += f":{reference}"
                self._roles.append(role)
            if claim_type == 'verified':
                self._verified: bool | None = parts[1].lower() == 'true'

    def user_has_required_roles(self, token: TokenData) -> bool:
        """
        Will check if user has any of the required roles set as a requirement on the endpoint

        if no required roles are set on the endpoint being called, this will always return True

        :param token: Deserialized access token data
        :return: True if user has any of the required roles or if no roles are required
        """
        if len(self._roles) == 0:
            return True

        for role in self._roles:
            if role in token.roles:
                return True
        return False

    def check_verified(self, token: TokenData) -> bool:
        """
        Checks if verified is required and if user is verified
        :param token: Deserialized access token datum
        :return: True if verified is not required or if verified is required and user is verified
        """
        if self._verified is None:
            return True
        if self._verified == token.verified:
            return True
        return False


def get_current_user_if_any(
        request: Request,
        security_scopes: SecurityScopes,
        token: str | None = Depends(oauth2_scheme_optional),
        users: UserDatastore = Depends(get_user_datastore),
) -> UserDatabaseModel | None:
    """
    Gets current user from access token, if there is an access token
    :param request: HTTP request object
    :param security_scopes: security scope restrictions for current endpoint
    :param token: encoded jwt token
    :param users: datastore for user database access
    :return: User model from database
    """
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
    except JWTError as err:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Unable to decode jwt token: ' + str(err),
            headers={'WWW-Authenticate': authenticate_value},
        )
    user = users.get_user(email)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='No user was found for the provided username',
            headers={'WWW-Authenticate': authenticate_value},
        )
    if not user_has_access(security_scopes, request, token_data):
        request_url: str = get_current_request_url_with_additions(request, include_query=False)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"User is not authorized to access endpoint '{request_url}'",
            headers={'WWW-Authenticate': authenticate_value},
        )
    return user


def get_current_user(
        user: UserDatabaseModel | None = Depends(get_current_user_if_any),
) -> UserDatabaseModel:
    """
    Get current user

    :raises HTTPException: if user is not authenticated
    :param user: The user, if any
    :return: The user, if any
    """
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
    """
    Checks if user has access according to specifications in security scopes

    :param security_scopes: Scopes defined on endpoint of type fastapi.SecurityScopes
    :param request: HTTP Request object of type fastapi.Request
    :param token: Deserialized access token of type app.models.v1.token.TokenData
    :return: Bool True if user is authorized to access specific endpoint, otherwise False
    """
    print('Checking if user has access')
    security_scope_restrictions = SecurityScopeRestrictions(security_scopes, request)
    if security_scope_restrictions.user_has_required_roles(token):
        if security_scope_restrictions.check_verified(token):
            return True
    return False


def _ensure_correct_scopes_format(scope: str, parts: list[str], request: Request) -> None:
    """
    Verifies that the scope restriction is formatted correctly

    :raises HTTPException: 500 Internal Server Error if scope restriction has invalid format
    :param scope: raw scope string
    :param parts: scope string in parts split by colon
    :param request: HTTP request object
    :return: None
    """
    if len(parts) not in (2, 3):
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            f"endpoint '{str(request.url)}' has invalid security claim setup: '{scope}'"
        )
