"""Tests for API utilities."""
# ruff: noqa: B905, ANN001, ANN201
from itertools import chain

import pytest
import requests
from geneweaver.client.api.utils import _raise_for_status_hook, sessionmanager

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
