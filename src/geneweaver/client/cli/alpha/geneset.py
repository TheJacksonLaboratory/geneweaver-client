"""Geneset CLI commands."""

# ruff: noqa: B008
import json
from typing import List, Optional

import typer
from geneweaver.client.api import aon, genes, genesets
from geneweaver.client.auth import get_access_token
from geneweaver.client.utils.aon import map_symbols
from geneweaver.client.utils.cli.print.csv import format_csv
from geneweaver.core.enum import GeneIdentifier, Species

cli = typer.Typer()

HELP_MESSAGE = """
The geneset commands allow you to authenticate with the GeneWeaver API.
"""


@cli.command()
def get(
    ctx: typer.Context,
    geneset_id: int,
    gene_id_type: Optional[GeneIdentifier] = typer.Option(None, case_sensitive=False),
    as_csv: bool = typer.Option(False, "--csv", help="Output as CSV"),
) -> dict:
    """Get a Geneset by ID."""
    result = genesets.get(get_access_token(), geneset_id, gene_id_type=gene_id_type)
    if not ctx.obj["quiet"]:
        if ctx.obj["pretty"]:
            typer.echo(json.dumps(result, indent=4))
        else:
            typer.echo(json.dumps(result))
    return result


@cli.command()
def get_values_as_ensembl_mouse(
    ctx: typer.Context,
    geneset_id: int,
    in_threshold: Optional[bool] = None,
    algorithm: Optional[aon.OrthologAlgorithms] = typer.Option(
        default=None, help="Ortholog mapping algorithm. Leave empty for all algorithms."
    ),
    as_csv: bool = typer.Option(False, "--csv", help="Output as CSV"),
) -> List[dict]:
    """Get a Geneset's values as Ensembl Mouse Gene IDs."""
    # Check Geneset Species
    token = get_access_token()
    response = genesets.get(token, geneset_id)
    species = Species(response["geneset"]["species_id"])

    gene_id_type = GeneIdentifier.ENSEMBLE_GENE

    if species == Species.HOMO_SAPIENS:
        gene_id_type = GeneIdentifier.HGNC

    response = genesets.get_values(token, geneset_id, gene_id_type, in_threshold)

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
            token,
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

    if as_csv:
        result = format_csv(result)

    if not ctx.obj["quiet"]:
        if not as_csv:
            if ctx.obj["pretty"]:
                typer.echo(json.dumps(result, indent=4))
            else:
                typer.echo(json.dumps(result))
        else:
            typer.echo(result)

    return result
