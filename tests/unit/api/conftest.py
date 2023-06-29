import json
from contextlib import contextmanager

import pytest
import requests
from geneweaver.client.api.utils import _raise_for_status_hook
from requests import Response


class MockSession:
    def __init__(
        self, status_code=200, resp_json=None, resp_content=None, raise_for_status=True
    ) -> None:
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

    def _prepare_mock_response(self, url: str, *args, **kwargs):
        resp = Response()
        resp.url = url
        resp._content = self._content
        resp.status_code = self.status_code
        self.hooks["response"](resp, *args, **kwargs)
        return resp

    def get(self, url, **kwargs):
        return self._prepare_mock_response(url, **kwargs)

    def options(self, url, **kwargs):
        return self._prepare_mock_response(url, **kwargs)

    def head(self, url, **kwargs):
        return self._prepare_mock_response(url, **kwargs)

    def post(self, url, data=None, json=None, **kwargs):
        return self._prepare_mock_response(url, data=data, json=json, **kwargs)

    def put(self, url, data=None, **kwargs):
        return self._prepare_mock_response(url, data=data, **kwargs)

    def patch(self, url, data=None, **kwargs):
        return self._prepare_mock_response(url, data=data, **kwargs)

    def delete(self, url, **kwargs):
        return self._prepare_mock_response(url, **kwargs)


@pytest.fixture()
def config_sessionmanager_patch(monkeypatch):
    def create_contextmanager(status_code=200, resp_json=None, resp_content=None):
        @contextmanager
        def mocked_contextmanager():
            mock = MockSession(
                status_code=status_code, resp_json=resp_json, resp_content=resp_content
            )
            yield mock

        monkeypatch.setattr(requests, "Session", mocked_contextmanager)
        return mocked_contextmanager

    return create_contextmanager
