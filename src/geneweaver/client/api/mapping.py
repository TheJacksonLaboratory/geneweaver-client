"""Cross-API Geneset Symbol Mapping."""

from typing import List, Optional

from geneweaver.client.api import aon, genes, genesets
from geneweaver.client.utils.aon import map_symbols
from geneweaver.core.enum import GeneIdentifier, Species


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

    if species == Species.HOMO_SAPIENS:
        gene_id_type = GeneIdentifier.HGNC

    response = genesets.get_values(access_token, geneset_id, gene_id_type, in_threshold)

    if species == Species.MUS_MUSCULUS:
        result = response["data"]

    else:
        if algorithm:
            algorithm_id = aon.algorithm_id_from_name(algorithm.value)
        else:
            algorithm_id = None

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

        result = [{"symbol": k, "value": v} for k, v in ensembl_result.items()]

    return result
