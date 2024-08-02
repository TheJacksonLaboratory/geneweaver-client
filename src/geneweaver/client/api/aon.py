"""Functions that wrap the GeneWeaver API on /genesets endpoints."""

from typing import List

from geneweaver.client.api.utils import sessionmanager
from geneweaver.client.core.config import settings
from geneweaver.core.enum import Species


def ortholog_mapping(
    identifiers: List[str], to_species: Species, algorithm_id: int = 7
) -> dict:
    """Get ortholog mapping for a list of genes.

    :param identifiers: List of gene values (must be AON ID type for Species).
    :param to_species: Species to map to.
    :param algorithm_id: Algorithm ID for mapping.

    :return: Ortholog mapping dict.
    """
    with sessionmanager() as session:
        resp = session.post(
            settings.AON_API_URL + "/genes/ortholog/mapping",
            params={
                "to_species": int(to_species),
                "algorithm_id": algorithm_id,
                "limit": 30000,
            },
            json=identifiers,
        )
    return resp.json()
