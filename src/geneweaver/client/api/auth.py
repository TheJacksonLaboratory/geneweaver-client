"""Utilities for authenticating with the GeneWeaver API via Oauth."""

from geneweaver.client import auth


class ApiClient:
    """A client to the GeneWeaver API."""

    def __init__(self) -> None:
        """Initialize the ApiClient."""
        self.auth = auth
