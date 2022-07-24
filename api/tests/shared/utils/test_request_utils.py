from unittest.mock import Mock, PropertyMock

import pytest
from fastapi.datastructures import QueryParams, URL

from app.shared.utils.request_utils import get_query_string, get_url


@pytest.mark.parametrize(
    ("query_params", "expected"),
    [
        ({}, ""),
        ("param1", "?param1"),
        ({"param1": "val1"}, "?param1=val1"),
        ({"param1": "val1", "param2": "val2"}, "?param1=val1&param2=val2"),
    ],
)
def test_get_query_string(http_request, query_params, expected):
    type(http_request).query_params = PropertyMock(return_value=QueryParams(query_params))
    assert get_query_string(http_request) == expected


@pytest.mark.parametrize(
    ("port", "expected"),
    [(80, "https://localhost/api"), (8000, "https://localhost:8000/api")],
)
def test_get_url(http_request, port, expected):
    url = Mock(URL)
    type(url).scheme = PropertyMock(return_value="https")
    type(url).hostname = PropertyMock(return_value="localhost")
    type(url).port = PropertyMock(return_value=port)
    type(url).path = PropertyMock(return_value="/api")
    type(http_request).url = PropertyMock(return_value=url)
    assert get_url(http_request) == expected
