"""Functions that wrap the GeneWeaver API on /genesets endpoints."""
from typing import Optional

import requests
from geneweaver.client.api.utils import sessionmanager
from geneweaver.client.core.config import settings
from geneweaver.core.schema import geneset as geneset_schema

ENDPOINT = "/genesets"


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


def get(token: str, geneset_id: int) -> dict:
    """Get a Geneset by ID."""
    with sessionmanager() as session:
        resp = session.get(
            settings.API_URL + ENDPOINT + "/" + str(geneset_id),
            headers={"Authorization": f"Bearer {token}"},
        )
    return resp.json()


def get_genesets(access_token: str) -> list:
    """Get all visible genesets."""
    return requests.get(
        settings.api_v3_path() + "/genesets",
        headers={"Authorization": f"Bearer {access_token}"},
    ).json()
