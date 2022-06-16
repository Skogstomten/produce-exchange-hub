from unittest.mock import Mock, PropertyMock

from pytest import fixture, mark
from fastapi import Request
from fastapi.security import SecurityScopes

from app.dependencies.user import SecurityScopeRestrictions
from app.models.v1.token import TokenData


@fixture
def http_request():
    return Mock(Request)


@fixture
def security_scope():
    return Mock(SecurityScopes)


@fixture
def empty_http_request(http_request):
    type(http_request).path_params = PropertyMock(return_value={})
    return http_request


def test_works_with_no_scopes(security_scope, empty_http_request):
    type(security_scope).scopes = PropertyMock(return_value=[])
    type(empty_http_request).path_params = PropertyMock(return_value={})
    target = SecurityScopeRestrictions(security_scope, empty_http_request)
    assert len(target._roles) == 0


@mark.parametrize(
    ("scopes", "expected"),
    [
        ([], None),
        (["verified:True"], True),
        (["verified:False"], False),
    ],
)
def test_scope_restriction_verified(
    security_scope, empty_http_request, scopes, expected
):
    type(security_scope).scopes = PropertyMock(return_value=scopes)
    target = SecurityScopeRestrictions(security_scope, empty_http_request)
    assert target._verified == expected


@mark.parametrize(
    ("scopes", "path_params", "token_data_roles", "expected"),
    [
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
    ],
)
def test_scope_restrictions_user_has_required_roles(
    security_scope, http_request, scopes, path_params, token_data_roles, expected
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
    target = SecurityScopeRestrictions(security_scope, http_request)
    assert target.user_has_required_roles(token_data) == expected
