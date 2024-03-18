"""Geneweaver API CLI for Geneset endpoints."""

# ruff: noqa: B008
import json
from typing import Optional

import typer
from geneweaver.client.api import genesets
from geneweaver.client.auth import get_access_token
from geneweaver.core.enum import GeneIdentifier

cli = typer.Typer()

HELP_MESSAGE = """
Tools and utilities for interacting with the Geneweaver API.
"""


@cli.command()
def get(
    ctx: typer.Context,
    geneset_id: int,
    gene_id_type: Optional[GeneIdentifier] = typer.Option(None, case_sensitive=False),
) -> dict:
    """Get a Geneset by ID."""
    result = genesets.get(get_access_token(), geneset_id, gene_id_type=gene_id_type)
    if not ctx.obj["quiet"]:
        if ctx.obj["pretty"]:
            typer.echo(json.dumps(result, indent=4))
        else:
            typer.echo(json.dumps(result))
    return result
