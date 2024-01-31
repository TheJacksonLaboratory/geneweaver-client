"""Functions that wrap the GeneWeaver API on /genesets endpoints."""
from typing import Optional

from geneweaver.client.api.utils import format_endpoint, sessionmanager
from geneweaver.core.enum import GeneIdentifier

ENDPOINT = "genesets"


def get(
    access_token: str, geneset_id: int, gene_id_type: Optional[GeneIdentifier] = None
) -> dict:
    """Get a Geneset by ID."""
    params = {} if gene_id_type is None else {"gene_id_type": int(gene_id_type)}
    with sessionmanager(token=access_token) as session:
        resp = session.get(
            format_endpoint(ENDPOINT, str(geneset_id)),
            params=params,
        )
    return resp.json()


def get_genesets(access_token: str) -> list:
    """Get all visible genesets."""
    with sessionmanager(token=access_token) as session:
        resp = session.get(format_endpoint(ENDPOINT))
    return resp.json()
