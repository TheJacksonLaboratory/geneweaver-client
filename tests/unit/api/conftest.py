"""Pytest fixtures for the API client unit tests."""
# ruff: noqa: ANN001, ANN401
import json
from contextlib import contextmanager
from typing import Any, Callable

import pytest
import requests
from geneweaver.client.api.utils import _raise_for_status_hook
from requests import Response


class MockSession:
    """A mock session for testing."""

    def __init__(
        self: "MockSession",
        status_code=200,
        resp_json=None,
        resp_content=None,
        raise_for_status=True,
    ) -> None:
        """Initialize a mock session."""
        self._default_resp_content = b'{"status": "ok"}'
        self.status_code = status_code
        self.raise_for_status = raise_for_status
        if resp_json:
            self._content = json.dumps(resp_json).encode()
        elif resp_content:
            self._content = resp_content
        else:
            self._content = self._default_resp_content

        self.hooks = {"response": _raise_for_status_hook}

    def _prepare_mock_response(
        self: "MockSession", url: str, *args: Any, **kwargs: Any
    ) -> Response:
        """Prepare a mock response."""
        resp = Response()
        resp.url = url
        resp._content = self._content
        resp.status_code = self.status_code
        self.hooks["response"](resp, *args, **kwargs)
        return resp

    def get(self: "MockSession", url, **kwargs: Any) -> Response:
        """Call the mock get method."""
        return self._prepare_mock_response(url, **kwargs)

    def options(self: "MockSession", url, **kwargs: Any) -> Response:
        """Call the mock options method."""
        return self._prepare_mock_response(url, **kwargs)

    def head(self: "MockSession", url, **kwargs: Any) -> Response:
        """Call the mock head method."""
        return self._prepare_mock_response(url, **kwargs)

    def post(self: "MockSession", url, data=None, json=None, **kwargs: Any) -> Response:
        """Call the mock post method."""
        return self._prepare_mock_response(url, data=data, json=json, **kwargs)

    def put(self: "MockSession", url, data=None, **kwargs: Any) -> Response:
        """Call the mock put method."""
        return self._prepare_mock_response(url, data=data, **kwargs)

    def patch(self: "MockSession", url, data=None, **kwargs: Any) -> Response:
        """Call the mock patch method."""
        return self._prepare_mock_response(url, data=data, **kwargs)

    def delete(self: "MockSession", url, **kwargs: Any) -> Response:
        """Call the mock delete method."""
        return self._prepare_mock_response(url, **kwargs)


@pytest.fixture()
def config_sessionmanager_patch(monkeypatch) -> Callable:
    """Patch the sessionmanager."""

    def create_contextmanager(
        status_code=200, resp_json=None, resp_content=None
    ) -> Callable:
        @contextmanager
        def mocked_contextmanager() -> MockSession:
            mock = MockSession(
                status_code=status_code, resp_json=resp_json, resp_content=resp_content
            )
            yield mock

        monkeypatch.setattr(requests, "Session", mocked_contextmanager)
        return mocked_contextmanager

    return create_contextmanager
