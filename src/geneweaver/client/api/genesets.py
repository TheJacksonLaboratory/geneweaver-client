"""Functions that wrap the GeneWeaver API on /genesets endpoints."""
from geneweaver.client.api.utils import format_endpoint, sessionmanager
from geneweaver.core.enum import GeneIdentifier

ENDPOINT = "genesets"


def get(access_token: str, geneset_id: int, gene_id_type: GeneIdentifier) -> dict:
    """Get a Geneset by ID."""
    with sessionmanager(token=access_token) as session:
        resp = session.get(
            format_endpoint(ENDPOINT, str(geneset_id)),
            params={"gene_id_type": int(gene_id_type)},
        )
    return resp.json()


def get_genesets(access_token: str) -> list:
    """Get all visible genesets."""
    with sessionmanager(token=access_token) as session:
        resp = session.get(format_endpoint(ENDPOINT))
    return resp.json()
