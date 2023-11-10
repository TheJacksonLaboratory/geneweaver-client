"""API Utilities integration tests."""
# ruff: noqa: ANN001, ANN201
import pytest
from geneweaver.client.api.exc import GeneweaverAPIError
from geneweaver.client.api.utils import sessionmanager

from tests.unit.api.test_api_utils import CLIENT_ERROR, SERVER_ERROR, SUCCESS


# NOTE: httpstat.us is a service that returns a response with a given status code.
#  It does not currently support 504 statuses, instead returning a 200.
#  We manually remove it from our SERVER_ERROR list when parametrizing this test.
@pytest.mark.parametrize(
    "status_code", CLIENT_ERROR + SERVER_ERROR[:4] + SERVER_ERROR[5:]
)
def test_calling_raise_for_status_from_sessionmanager(status_code):
    """Test that sessionmanager raises an exception for non-2xx status codes."""
    with pytest.raises(GeneweaverAPIError):  # noqa: PT012
        with sessionmanager() as session:
            session.get(f"https://httpstat.us/{status_code}")


# NOTE: httpstat.us is a service that returns a response with a given status code.
#  It does not appear to currently support INFO or REDIRECTION responses, so they are
#  left our of this parametrization.
@pytest.mark.parametrize("status_code", SUCCESS)
def test_calling_raise_for_status_from_sessionmanager_does_not_raise(status_code):
    """Test that sessionmanager does not raise an exception for 2xx status codes."""
    with sessionmanager() as session:
        resp = session.get(f"https://httpstat.us/{status_code}")
        assert resp is not None
        assert resp.ok is True
        assert resp.status_code == status_code
