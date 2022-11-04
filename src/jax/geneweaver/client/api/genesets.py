"""
Functions that wrap the GeneWeaver API on /genesets endpoints.
"""
from typing import Optional
from jax.geneweaver.core.schema.geneset import Geneset, GenesetUpload, BatchUpload
from jax.geneweaver.client.config import settings
from jax.geneweaver.client.api.utils import sessionmanager

ENDPOINT = "/genesets/"


def post(token: str, geneset: GenesetUpload) -> Optional[Geneset]:
    """Create a new Geneset, with the genes specified in the request body."""
    with sessionmanager() as session:
        resp = session.post(settings.API_URL + ENDPOINT,
                            json=geneset.dict(),
                            headers={"Authorization": token})
    return Geneset(**resp.json())


def post_batch(token: str, geneset: BatchUpload) -> Geneset:
    """Create a new Geneset using a batch upload file."""

    with sessionmanager() as session:
        resp = session.post(settings.API_URL + ENDPOINT + 'batch',
                            json=geneset.dict(),
                            headers={"Authorization": token})
    return Geneset(**resp.json())
