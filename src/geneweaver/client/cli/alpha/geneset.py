"""Geneset CLI commands."""

# ruff: noqa: B008
import json
from typing import List, Optional

import typer
from geneweaver.client.api import aon, genesets, mapping
from geneweaver.client.auth import get_access_token
from geneweaver.client.utils.cli.print.csv import format_csv
from geneweaver.core.enum import GeneIdentifier

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
    result = mapping.ensembl_mouse_mapping(
        token,
        geneset_id,
        in_threshold,
        algorithm,
    )

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
