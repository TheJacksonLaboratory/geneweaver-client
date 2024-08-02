"""Functions that warp the Geneweaver /genes endpoint."""

from typing import List

from geneweaver.client.api.utils import format_endpoint, sessionmanager
from geneweaver.core.enum import GeneIdentifier, Species

ENDPOINT = "genes"


def mappings(
    access_token: str,
    source_ids: List[str],
    target_id_type: GeneIdentifier,
    species: Species,
) -> dict:
    """Get mappings for a list of genes.

    :param access_token: User access token
    :param source_ids: List of source gene IDs.
    :param target_id_type: Target gene ID type (one of GeneIdentifier).
    :param species: Species of the identifiers.
    """
    with sessionmanager(token=access_token) as session:
        resp = session.post(
            format_endpoint(ENDPOINT, "mappings"),
            json={
                "source_ids": source_ids,
                "target_gene_id_type": str(target_id_type),
                "species": str(species),
            },
        )

    return resp.json()
