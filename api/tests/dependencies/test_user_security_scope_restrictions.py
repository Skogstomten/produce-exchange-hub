from unittest.mock import Mock, PropertyMock

from pytest import fixture
from fastapi import Request
from fastapi.security import SecurityScopes

from app.dependencies.user import SecurityScopeRestrictions


@fixture
def http_request():
    return Mock(Request)


@fixture
def security_scope():
    return Mock(SecurityScopes)


def test_works_with_no_scopes(security_scope, http_request):
    type(security_scope).scopes = PropertyMock(return_value=[])
    type(http_request).path_params = PropertyMock(return_value={})
    target = SecurityScopeRestrictions(security_scope, http_request)
    assert len(target._roles) == 0
    assert target._verified is None
