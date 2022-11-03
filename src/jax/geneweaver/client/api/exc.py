"""Exception classes relating to calling the Geneweaver API."""
from jax.geneweaver.core.exc import GeneweaverException


class GeneweaverAPIException(GeneweaverException):
    """Base class for exceptions in the Geneweaver API."""

    pass
