"""Functions that warp the Geneweaver /genes endpoint."""
from typing import List, Optional

from geneweaver.client.api.utils import format_endpoint, sessionmanager
from geneweaver.core.enum import GeneIdentifier, Species

ENDPOINT = "genes"


def map_homologs(
    access_token: str,
    source_ids: List[str],
    target_id_type: GeneIdentifier,
    source_id_type: Optional[GeneIdentifier] = None,
    target_species: Optional[Species] = None,
    source_species: Optional[Species] = None,
) -> dict:
    """Map homologs between species."""
    post_args = {
        "source_ids": source_ids,
        "target_gene_id_type": int(target_id_type),
    }
    if source_id_type is not None:
        post_args["source_gene_id_type"] = int(source_id_type)

    if target_species is not None:
        post_args["target_species"] = int(target_species)

    if source_species is not None:
        post_args["source_species"] = int(source_species)

    with sessionmanager(token=access_token) as session:
        resp = session.post(format_endpoint(ENDPOINT, "homologous-ids"), json=post_args)

    return resp.json()
