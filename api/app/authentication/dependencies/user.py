"""
Module for user related dependencies
"""
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import SecurityScopes
from jose import jwt, JWTError

from app.authentication.datastores.authentication_datastore import AuthenticationDatastore, get_authentication_datastore
from app.authentication.models.db.user import User
from app.authentication.models.v1.token import TokenData, TokenRoleMap
from app.shared.utils.request_utils import get_current_request_url_with_additions, get_url
from .auth import OAUTH2_SCHEME_OPTIONAL, SECRET_KEY, ALGORITHM
from app.logging.log import AppLogger, AppLoggerInjector
from app.shared.errors.errors import InvalidOperationError
from app.authentication.utils.str_utils import remove_brackets
from ..errors.claim_type_not_supported_error import ClaimTypeNotSupportedError

CLAIM_TYPE_VERIFIED = "verified"
CLAIM_TYPE_ROLES = "roles"
CLAIM_TYPE_SELF = "self"

logger_injector = AppLoggerInjector("dependencies.user")


def _get_ref_part(parts: list[str], i: int) -> str | None:
    ref_part = None
    try:
        ref_part = parts[i]
    except IndexError:
        pass
    return ref_part


def _get_ref(parts: list[str], i: int, request: Request) -> str | None:
    ref_part = _get_ref_part(parts, i)
    if ref_part == "*":
        return ref_part
    if ref_part:
        ref_part = remove_brackets(ref_part)
        return request.path_params.get(ref_part, None)
    return None


class Scope:
    def __init__(self, scope_str: str, request: Request):
        self._scope_str = scope_str
        self._request = request
        self._parts = scope_str.split(":")
        _ensure_correct_scopes_format(scope_str, self._parts, request)
        self._claim_type = self._parts[0]

    @property
    def claim_type(self) -> str:
        return self._claim_type

    def get_verified_value(self) -> bool:
        return self._get_part(CLAIM_TYPE_VERIFIED, 1).lower() == "true"

    def get_self_ref(self) -> str:
        return self._get_ref(CLAIM_TYPE_SELF, 1, allow_wildcard=False)

    def get_role_name(self) -> str:
        return self._get_part(CLAIM_TYPE_ROLES, 1)

    def get_role_ref(self) -> str | None:
        return self._get_ref(CLAIM_TYPE_ROLES, 2, required=False)

    def _get_ref(self, claim_type: str, index: int, required: bool = True, allow_wildcard: bool = True) -> str | None:
        ref_name = self._get_part(claim_type, index)
        if ref_name is None:
            if required:
                raise InvalidOperationError(
                    f"Required ref not found for claim type '{claim_type}'. URL={get_url(self._request)}"
                )
            return None
        if ref_name == "*":
            if allow_wildcard:
                return ref_name
            else:
                raise InvalidOperationError(
                    f"Can't have a wildcard on claim type {claim_type}. URL={get_url(self._request)}"
                )
        ref = self._request.path_params.get(remove_brackets(ref_name), None)
        if required:
            if ref is None:
                raise InvalidOperationError(f"Can't find ref for '{ref_name}'. URL={get_url(self._request)}")
        return ref

    def _get_part(self, claim_type: str, index: int) -> str | None:
        self._ensure_valid_claim_type(claim_type)
        try:
            return self._parts[index]
        except IndexError:
            return None

    def _ensure_valid_claim_type(self, claim_type: str):
        if not self._claim_type == claim_type:
            raise InvalidOperationError(
                f"Can't call method for claim_type other than {claim_type}: scope_str={self._scope_str}"
            )


class Role:
    def __init__(self, role_name: str, ref: str | None):
        self._role_name = role_name
        self._ref = ref

    def matches(self, token_role_map: TokenRoleMap, authenticated_user: User) -> bool:
        if self._role_name == CLAIM_TYPE_SELF:
            return self._ref == authenticated_user.id

        token_roles = token_role_map[self._role_name]
        if token_roles:
            if self._ref == "*":
                return True
            if self._ref in token_roles:
                return True

        return False


class Roles:
    """Collection class holding a collection of roles."""

    def __init__(self):
        self._roles: list[Role] = []

    def __len__(self):
        return self._roles.__len__()

    def __iter__(self):
        return self._roles.__iter__()

    def append_role(self, scope: Scope) -> None:
        if scope.claim_type not in (CLAIM_TYPE_SELF, CLAIM_TYPE_ROLES):
            return
        if scope.claim_type == CLAIM_TYPE_SELF:
            self._append_self(scope)
        elif scope.claim_type == CLAIM_TYPE_ROLES:
            self._append_roles(scope)
        else:
            raise ValueError("Shit")

    def _append_self(self, scope: Scope):
        role = CLAIM_TYPE_SELF
        ref = scope.get_self_ref()
        self._roles.append(Role(role, ref))

    def _append_roles(self, scope: Scope):
        role = scope.get_role_name()
        ref = scope.get_role_ref()
        self._roles.append(Role(role, ref))

    def match_with_user(self, token_role_map: TokenRoleMap, authenticated_user: User) -> True:
        for role in self._roles:
            if role.matches(token_role_map, authenticated_user):
                return True
        return False


class SecurityScopeRestrictions:
    """
    Parses and strictures the scope restrictions set on endpoint for easy
    verification
    """

    def __init__(
        self,
        security_scopes: SecurityScopes,
        request: Request,
        authenticated_user: User,
    ):
        """
        Parses and stores the security scopes.

        Supported scopes=
            roles:role_name:reference[optional]
            verified:True|False
            self:{user_id}

        :param security_scopes: SecurityScopes object received from fastapi
        :param request: HTTP request object, needed to acquire resource keys
        to check for access to specific resources
        """
        self._security_scopes = security_scopes
        self._request = request
        self._authenticated_user = authenticated_user
        self._roles = Roles()
        self._verified: bool | None = None

        for scope in [Scope(s, request) for s in security_scopes.scopes]:
            if scope.claim_type == CLAIM_TYPE_ROLES or scope.claim_type == CLAIM_TYPE_SELF:
                self._roles.append_role(scope)
            elif scope.claim_type == CLAIM_TYPE_VERIFIED:
                self._verified = scope.get_verified_value()
            else:
                raise ClaimTypeNotSupportedError(scope.claim_type)

    def user_has_required_roles(self, token: TokenData) -> bool:
        """
        Will check if user has any of the required roles set as a requirement
        on the endpoint.

        if no required roles are set on the endpoint being called, this will
        always return True.

        :param token: Deserialized access token data.
        :return: True if user has any of the required roles or if no roles are
                 required.
        """
        if token.has_superuser_role():
            return True

        return self._roles.match_with_user(token.get_token_role_map(), self._authenticated_user)

    def check_verified(self, token: TokenData) -> bool:
        """
        Checks if verified is required and if user is verified
        :param token: Deserialized access token datum
        :return: True if verified is not required or if verified is required
        and user is verified
        """
        if self._verified is None:
            return True
        if self._verified == token.verified:
            return True
        return False


def get_current_user_if_any(
    request: Request,
    security_scopes: SecurityScopes,
    token: str | None = Depends(OAUTH2_SCHEME_OPTIONAL),
    authentication_datastore: AuthenticationDatastore = Depends(get_authentication_datastore),
    logger: AppLogger = Depends(logger_injector),
) -> User | None:
    """
    Gets current user from access token, if there is an access token.
    :raise HTTPException: If Authentication of token or authorization of
    user should in any way fail.
    :param request: HTTP request object.
    :param security_scopes: security scope restrictions for current endpoint.
    :param token: encoded jwt token.
    :param authentication_datastore: datastore for user database access.
    :param logger: AppLogger
    :return: User model from database.
    """
    logger.debug(
        f"get_current_user_if_any(request={request}, security_scopes={security_scopes}, token={token}, "
        f"users={authentication_datastore})"
    )
    if token is None:
        return None
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = "Bearer"
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        token_data = TokenData(**payload)
        print(payload)
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="No email found in token.",
                headers={"WWW-Authenticate": authenticate_value},
            )
    except JWTError as err:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unable to decode jwt token: " + str(err),
            headers={"WWW-Authenticate": authenticate_value},
        ) from err
    user = authentication_datastore.get_user(email)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No user was found for the provided username",
            headers={"WWW-Authenticate": authenticate_value},
        )
    if not user_has_access(security_scopes, request, token_data, user):
        request_url: str = get_current_request_url_with_additions(request, include_query=False)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User is not authorized to access endpoint " f"'{request_url}'",
            headers={"WWW-Authenticate": authenticate_value},
        )
    return user


def get_current_user(
    user: User | None = Depends(get_current_user_if_any),
) -> User:
    """
    Get current user.
    :raises HTTPException: if user is not authenticated.
    :param user: The user, if any.
    :return: The user, if any.
    """
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


def user_has_access(
    security_scopes: SecurityScopes,
    request: Request,
    token: TokenData,
    authenticated_user: User,
) -> bool:
    """
    Checks if user has access according to specifications in security scopes.
    :param security_scopes: Scopes defined on endpoint of type
    fastapi.SecurityScopes
    :param request: HTTP Request object of type fastapi.Request
    :param token: Deserialized access token of type
    app.models.v1.token.TokenData
    :param authenticated_user:
    :return: Bool True if user is authorized to access specific endpoint,
    otherwise False
    """
    print("Checking if user has access")
    security_scope_restrictions = SecurityScopeRestrictions(security_scopes, request, authenticated_user)
    if security_scope_restrictions.user_has_required_roles(token):
        if security_scope_restrictions.check_verified(token):
            return True
    return False


def _ensure_correct_scopes_format(scope: str, parts: list[str], request: Request) -> None:
    """
    Verifies that the scope restriction is formatted correctly.
    :raises HTTPException: 500 Internal Server Error if scope restriction has
    invalid format.
    :param scope: raw scope string.
    :param parts: scope string in parts split by colon.
    :param request: HTTP request object.
    :return: None.
    """
    if len(parts) not in (2, 3):
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            f"endpoint '{str(request.url)}' " f"has invalid security claim setup: '{scope}'",
        )
