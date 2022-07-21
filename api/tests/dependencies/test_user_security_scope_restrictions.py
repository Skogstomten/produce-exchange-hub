from unittest.mock import Mock, PropertyMock

from bson import ObjectId
from fastapi.security import SecurityScopes
from pytest import fixture, mark

from app.dependencies.user import SecurityScopeRestrictions
from app.models.v1.token import TokenData


@fixture
def security_scope():
    return Mock(SecurityScopes)


@fixture
def empty_http_request(http_request):
    type(http_request).path_params = PropertyMock(return_value={})
    return http_request


def test_works_with_no_scopes(security_scope, empty_http_request, authenticated_user_default):
    type(security_scope).scopes = PropertyMock(return_value=[])
    type(empty_http_request).path_params = PropertyMock(return_value={})
    target = SecurityScopeRestrictions(security_scope, empty_http_request, authenticated_user_default)
    assert len(target._roles) == 0


@mark.parametrize(
    ("scopes", "expected"),
    [
        ([], None),
        (["verified:True"], True),
        (["verified:False"], False),
    ],
)
def test_scope_restriction_verified(security_scope, empty_http_request, authenticated_user_default, scopes, expected):
    type(security_scope).scopes = PropertyMock(return_value=scopes)
    target = SecurityScopeRestrictions(security_scope, empty_http_request, authenticated_user_default)
    assert target._verified == expected


@mark.parametrize(
    ("scopes", "path_params", "token_data_roles", "expected"),
    [
        (["roles:role_name:{resource_id}"], {"resource_id": "12345"}, ["superuser"], True),
        (
            ["roles:role_name"],
            {},
            [],
            False,
        ),
        (
            ["roles:role_name"],
            {},
            ["role_name"],
            True,
        ),
        (
            ["roles:role_name:{resource_id}"],
            {"resource_id": "1234"},
            ["role_name:1234"],
            True,
        ),
        (
            ["roles:role_name:{resource_id}"],
            {"resource_id": "1234"},
            ["role_name:1111"],
            False,
        ),
        (["roles:role_name:*"], {}, ["role_name:12345"], True),
    ],
)
def test_scope_restrictions_user_has_required_roles(
    scopes, path_params, token_data_roles, expected, security_scope, http_request, authenticated_user_default
):
    type(security_scope).scopes = PropertyMock(return_value=scopes)
    type(http_request).path_params = PropertyMock(return_value=path_params)
    token_data = TokenData(
        **{
            "sub": "nisse@perssons.se",
            "scopes": scopes,
            "verified": True,
            "roles": token_data_roles,
        }
    )
    target = SecurityScopeRestrictions(security_scope, http_request, authenticated_user_default)
    assert target.user_has_required_roles(token_data) == expected


@mark.parametrize(
    ["req_user_id", "user_id", "expected"],
    (
        ("62b0581674e22082fe2a721a", "62b0581674e22082fe2a721a", True),
        ("62b0581674e22082fe2a721a", str(ObjectId()), False),
    ),
)
def test_self_restriction_works(
    security_scope,
    http_request,
    authenticated_user_default,
    req_user_id,
    user_id,
    expected,
):
    type(security_scope).scopes = PropertyMock(return_value=("self:{user_id}",))
    type(http_request).path_params = PropertyMock(return_value={"user_id": req_user_id})
    token_data = TokenData(
        **{
            "sub": "nisse@perssons.se",
            "scopes": [],
            "verified": True,
            "roles": [],
        }
    )
    authenticated_user_default.id = user_id
    target = SecurityScopeRestrictions(security_scope, http_request, authenticated_user_default)
    assert target.user_has_required_roles(token_data) is expected
