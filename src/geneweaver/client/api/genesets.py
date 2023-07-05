"""Functions that wrap the GeneWeaver API on /genesets endpoints."""
from typing import Optional

from geneweaver.client.api.utils import sessionmanager
from geneweaver.client.config import settings
from geneweaver.core.schema import geneset as geneset_schema

ENDPOINT = "/genesets/"


def post(
    token: str, geneset: geneset_schema.GenesetUpload
) -> Optional[geneset_schema.Geneset]:
    """Create a new Geneset, with the genes specified in the request body."""
    with sessionmanager() as session:
        resp = session.post(
            settings.API_URL + ENDPOINT,
            json=geneset.dict(),
            headers={"Authorization": token},
        )
    return geneset_schema.Geneset(**resp.json())


def post_batch(
    token: str, geneset: geneset_schema.BatchUpload
) -> geneset_schema.Geneset:
    """Create a new Geneset using a batch upload file."""
    with sessionmanager() as session:
        resp = session.post(
            settings.API_URL + ENDPOINT + "batch",
            json=geneset.dict(),
            headers={"Authorization": token},
        )
    return geneset_schema.Geneset(**resp.json())


def get(token: str, geneset_id: int) -> geneset_schema.Geneset:
    """Get a Geneset by ID."""
    with sessionmanager() as session:
        resp = session.get(
            settings.API_URL + ENDPOINT + str(geneset_id),
            headers={"Authorization": token},
        )
    return geneset_schema.Geneset(**resp.json())
