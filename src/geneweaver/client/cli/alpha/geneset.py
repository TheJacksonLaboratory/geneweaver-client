"""Geneset CLI commands."""

# ruff: noqa: B008
import json
from typing import List, Optional

import typer
from geneweaver.client.api import aon, genes, genesets
from geneweaver.client.auth import get_access_token
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
        # TODO!
        # When a human gene maps to multiple mouse genes, there should be a row for each
        # of those mouse ids to be included, and therefore the score will be the same
        # for all of those.
        #
        # When multiple human genes map to the same mouse gene, we want to keep the
        # gene that has the highest abs(score).

        aon_response = aon.ortholog_mapping(
            [g["symbol"] for g in response["data"]], Species.MUS_MUSCULUS
        )

        to_mgi_map = {i["from_gene"]: i["to_gene"] for i in aon_response}

        mgi_symbols = [
            to_mgi_map[g["symbol"]]
            for g in response["data"]
            if g["symbol"] in to_mgi_map
        ]

        gw_map_response = genes.mappings(
            token, mgi_symbols, GeneIdentifier.ENSEMBLE_GENE, Species.MUS_MUSCULUS
        )

        mgi_to_ensembl = {
            v["original_ref_id"]: v["mapped_ref_id"]
            for v in gw_map_response["gene_ids_map"]
        }

        orig_to_ensembl = {
            g["symbol"]: mgi_to_ensembl[to_mgi_map[g["symbol"]]]
            for g in response["data"]
            if g["symbol"] in to_mgi_map and to_mgi_map[g["symbol"]] in mgi_to_ensembl
        }

        result = [
            {"symbol": orig_to_ensembl[g["symbol"]], "value": g["value"]}
            for g in response["data"]
            if g["symbol"] in orig_to_ensembl
        ]

    if as_csv:
        result = format_csv(result)

    typer.echo(result)

    return result
