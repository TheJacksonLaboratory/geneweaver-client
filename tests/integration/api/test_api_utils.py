import pytest
from jax.geneweaver.client.api.utils import sessionmanager
from jax.geneweaver.client.api.exc import GeneweaverAPIException

from ...unit.api.test_api_utils import SUCCESS, CLIENT_ERROR, SERVER_ERROR


# NOTE: httpstat.us is a service that returns a response with a given status code.
#  It does not currently support 504 statuses, instead returning a 200.
#  We manually remove it from our SERVER_ERROR list when parametrizing this test.
@pytest.mark.parametrize("status_code", CLIENT_ERROR + SERVER_ERROR[:4]+SERVER_ERROR[5:])
def test_calling_raise_for_status_from_sessionmanager(status_code):
    with pytest.raises(GeneweaverAPIException):
        with sessionmanager() as session:
            session.get(f"https://httpstat.us/{status_code}")


# NOTE: httpstat.us is a service that returns a response with a given status code.
#  It does not appear to currently support INFO or REDIRECTION responses, so they are left our of this parametrization.
@pytest.mark.parametrize("status_code", SUCCESS)
def test_calling_raise_for_status_from_sessionmanager_does_not_raise(status_code):
    with sessionmanager() as session:
        resp = session.get(f"https://httpstat.us/{status_code}")
        assert resp is not None
        assert resp.ok is True
        assert resp.status_code == status_code
