"""API related utilities, helpers, and other internal functions."""
from contextlib import contextmanager

import requests
from geneweaver.client.api.exc import GeneweaverAPIException


def _raise_for_status_hook(response, *args, **kwargs):
    """Have request responses raise an exception for non-200 status codes."""
    response.raise_for_status()


@contextmanager
def sessionmanager() -> requests.Session:
    """Context manager for a requests.Session object.

    This context manager will do everything that a requests.Session context manager
    does, but will also raise an exception if the response status code is not 200.
    It will also wrap all exceptions inheriting from
    `requests.exceptions.RequestException` in a GeneweaverAPIException.
    """
    with requests.Session() as session:
        session.hooks = {"response": _raise_for_status_hook}
        try:
            yield session
        except requests.exceptions.RequestException as err:
            # TODO: We SHOULD try extracting the error message from the response,
            #  could even check the JSON.
            err_str = (
                f"There was a problem calling the Geneweaver API: {err.response.text}"
            )
            raise GeneweaverAPIException(err_str) from err
