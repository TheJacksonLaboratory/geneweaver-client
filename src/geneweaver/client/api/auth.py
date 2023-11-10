"""Utilities for authenticating with the GeneWeaver API via Oauth."""

from geneweaver.client import auth


class ApiClient:
    def __init__(self):
        self.auth = auth
