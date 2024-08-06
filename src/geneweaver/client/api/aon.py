"""Functions that wrap the GeneWeaver API on /genesets endpoints."""

from enum import Enum
from typing import List, Optional

from geneweaver.client.api.utils import sessionmanager
from geneweaver.client.core.config import settings
from geneweaver.core.enum import Species


class OrthologAlgorithms(Enum):
    """The available ortholog algorithms in Geneweaver AON."""

    HGNC = "HGNC"
    PANTHER = "PANTHER"
    HIERANOID = "Hieranoid"
    PHYLOMEDB = "PhylomeDB"
    ORTHOINSPECTOR = "OrthoInspector"
    INPARANOID = "InParanoid"
    ORTHOFINDER = "OrthoFinder"
    ZFIN = "ZFIN"
    ENSEMBLCOMPARA = "EnsemblCompara"
    SONICPARANOID = "SonicParanoid"
    OMA = "OMA"
    XENBASE = "Xenbase"


def ortholog_mapping(
    identifiers: List[str], to_species: Species, algorithm_id: Optional[int] = None
) -> dict:
    """Get ortholog mapping for a list of genes.

    :param identifiers: List of gene values (must be AON ID type for Species).
    :param to_species: Species to map to.
    :param algorithm_id: Algorithm ID for mapping.

    :return: Ortholog mapping dict.
    """
    params = {"to_species": int(to_species), "limit": 30000}

    if algorithm_id is not None:
        params["algorithm_id"] = algorithm_id

    with sessionmanager() as session:
        resp = session.post(
            settings.AON_API_URL + "/genes/ortholog/mapping",
            params=params,
            json=identifiers,
        )
    return resp.json()


def algorithm_id_from_name(algorithm_name: str) -> int:
    """Get algorithm ID from algorithm name.

    :param algorithm_name: The name of the algorithm.
    :return: The algorithm ID.
    """
    with sessionmanager() as session:
        resp = session.get(settings.AON_API_URL + "/algorithms")
        algorithms = resp.json()
        for algorithm in algorithms:
            if algorithm["alg_name"].lower().replace(
                " ", ""
            ) == algorithm_name.lower().replace(" ", ""):
                return algorithm["alg_id"]
