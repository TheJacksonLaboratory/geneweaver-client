"""Exception classes relating to calling the Geneweaver API."""

from geneweaver.core.exc import GeneweaverError


class GeneweaverAPIError(GeneweaverError):
    """Base class for exceptions in the Geneweaver API."""

    pass
