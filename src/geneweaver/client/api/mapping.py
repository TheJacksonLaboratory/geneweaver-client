"""Cross-API Geneset Symbol Mapping."""

import re
from typing import List, Optional

from geneweaver.client.api import aon, genes, genesets
from geneweaver.client.utils.aon import map_symbols
from geneweaver.core.enum import GeneIdentifier, Species
from geneweaver.core.mapping import AON_ID_TYPE_FOR_SPECIES


def ensembl_mouse_mapping(
    access_token: str,
    geneset_id: int,
    in_threshold: bool,
    algorithm: Optional[aon.OrthologAlgorithms] = None,
) -> List[dict]:
    """Get a Geneset's values as Ensembl Mouse Gene IDs.

    :param access_token: User access token.
    :param geneset_id: Geneset ID.
    :param in_threshold: Whether to filter genes by threshold.
    :param algorithm: Ortholog mapping algorithm.

    :return: List of geneset values. `[{"symbol": k, "value": v}, ...]
    """
    response = genesets.get(access_token, geneset_id)
    species = Species(response["geneset"]["species_id"])

    gene_id_type = GeneIdentifier.ENSEMBLE_GENE

    if species != Species.MUS_MUSCULUS:
        try:
            gene_id_type = AON_ID_TYPE_FOR_SPECIES[species]
        except KeyError as e:
            raise ValueError(
                f"Species {species} is not supported for ortholog mapping"
            ) from e

    response = genesets.get_values(access_token, geneset_id, gene_id_type, in_threshold)
    if species == Species.MUS_MUSCULUS:
        result = [
            {"gene_id": item["symbol"], "score": item["value"]}
            for item in response["data"]
        ]

    else:
        if algorithm:
            algorithm_id = aon.algorithm_id_from_name(algorithm.value)
        else:
            algorithm_id = None

        response = clean_identifiers_for_aon(response, species)
        aon_response = aon.ortholog_mapping(
            [g["symbol"] for g in response["data"]],
            Species.MUS_MUSCULUS,
            algorithm_id=algorithm_id,
        )

        mgi_result = map_symbols(
            {item["symbol"]: item["value"] for item in response["data"]},
            [(r["from_gene"], r["to_gene"]) for r in aon_response],
        )

        gw_map_response = genes.mappings(
            access_token,
            list(set(mgi_result.keys())),
            GeneIdentifier.ENSEMBLE_GENE,
            Species.MUS_MUSCULUS,
        )

        ensembl_result = map_symbols(
            mgi_result,
            [
                (r["original_ref_id"], r["mapped_ref_id"])
                for r in gw_map_response["gene_ids_map"]
            ],
        )

        result = [{"gene_id": k, "score": v} for k, v in ensembl_result.items()]

    return result


IDENTIFIER_PREFIX_MAP = {
    Species.DANIO_RERIO: "ZFIN",
    Species.DROSOPHILA_MELANOGASTER: "FB",
    Species.CAENORHABDITIS_ELEGANS: "WB",
    Species.SACCHAROMYCES_CEREVISIAE: "SGD",
}


def clean_identifiers_for_aon(data: dict, species: Species) -> dict:
    """Clean up identifiers for AON mapping."""
    if species in [
        Species.DANIO_RERIO,
        Species.DROSOPHILA_MELANOGASTER,
        Species.CAENORHABDITIS_ELEGANS,
        Species.SACCHAROMYCES_CEREVISIAE,
    ]:
        data = {
            "data": [
                {
                    "symbol": f"{IDENTIFIER_PREFIX_MAP[species]}:{item['symbol']}",
                    "value": item["value"],
                }
                for item in data["data"]
            ]
        }
    elif species == Species.RATTUS_NORVEGICUS:
        data = {
            "data": [
                {
                    "symbol": insert_colon_delimiter(item["symbol"]),
                    "value": item["value"],
                }
                for item in data["data"]
            ]
        }

    return data


def insert_colon_delimiter(identifier: str) -> str:
    """Separates a prefix from ID and adds a colon delimiter between them."""
    if ":" in identifier:
        return identifier

    match = re.match(r"([A-Za-z]+)(\d+)", identifier)

    if match:
        prefix, suffix = match.groups()
        return f"{prefix}:{suffix}"
    else:
        # If the identifier does not match the expected pattern
        raise ValueError("Identifier format is invalid")
