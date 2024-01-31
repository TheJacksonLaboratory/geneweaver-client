"""Tests for API utilities."""
# ruff: noqa: B905, ANN001, ANN201
from itertools import chain
from unittest.mock import Mock, patch

import pytest
import requests
from geneweaver.client.api.exc import GeneweaverAPIError
from geneweaver.client.api.utils import (
    _raise_for_status_hook,
    format_endpoint,
    sessionmanager,
)

INFO = list(range(100, 104))
SUCCESS = list(chain(range(200, 209), (226,)))
REDIRECTION = list(range(300, 309))
CLIENT_ERROR = list(chain(range(400, 419), range(421, 427), (428, 429, 431, 451)))
SERVER_ERROR = list(chain(range(500, 509), (510, 511)))


@pytest.mark.parametrize("status_code", CLIENT_ERROR + SERVER_ERROR)
def test_raise_for_status_hook(status_code):
    """Test that raise_for_status hook raises an exception for non-2xx status codes."""
    response = requests.Response()
    response.status_code = status_code
    with pytest.raises(requests.exceptions.RequestException):
        _raise_for_status_hook(response)


def test_sessionmanager_sets_raise_for_status():
    """Test that sessionmanager sets the raise_for_status hook."""
    with sessionmanager() as session:
        assert session.hooks["response"] == _raise_for_status_hook


def test_sessionmanager_sets_auth_header():
    """Test that the sessionmanager sets the Authorization header."""
    with sessionmanager(token="test") as session:
        assert "Authorization" in session.headers
        assert session.headers["Authorization"] == "Bearer test"


def test_sessionmanager_catches_requests_exceptions():
    """Test that the sessionmanager catches requests exceptions."""
    mock_response = Mock()
    mock_response.text = "test"
    with pytest.raises(GeneweaverAPIError):  # noqa: PT012
        with sessionmanager() as session:
            with patch.object(
                session,
                "get",
                side_effect=requests.exceptions.RequestException(
                    response=mock_response
                ),
            ):
                session.get("http://example.com")


@pytest.mark.parametrize(
    ("parts", "expected"),
    [
        (("foo", "bar"), "foo/bar"),
        (("foo", "bar", "baz"), "foo/bar/baz"),
        (["foo", "bar", "foo", "bar"], "foo/bar/foo/bar"),
        (["foo", "foo", "bar", "bar", "baz", "baz"], "foo/foo/bar/bar/baz/baz"),
    ],
)
def test_format_endpoint(parts, expected):
    """Test that format_endpoint formats the endpoint correctly."""
    assert type(format_endpoint(*parts)) == str
    assert format_endpoint(*parts).endswith(expected)
