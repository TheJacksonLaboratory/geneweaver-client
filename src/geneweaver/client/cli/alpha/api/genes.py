"""Geneweaver API CLI for Gene endpoints."""

import json
from typing import List, Optional

import typer
from geneweaver.client.api import genes
from geneweaver.client.auth import get_access_token

cli = typer.Typer()

HELP_MESSAGE = """
Tools and utilities for interacting with the Geneweaver API.
"""


@cli.command()
def map_ids(
    ctx: typer.Context,
    source_ids: List[str],
    target_id_type: genes.GeneIdentifier,
    source_id_type: Optional[genes.GeneIdentifier] = None,
    target_species: Optional[genes.Species] = None,
    source_species: Optional[genes.Species] = None,
) -> dict:
    """Map homologs between species."""
    result = genes.map_homologs(
        get_access_token(),
        source_ids=source_ids,
        target_id_type=target_id_type,
        source_id_type=source_id_type,
        target_species=target_species,
        source_species=source_species,
    )

    if len(result["gene_ids_map"]) > 0:
        if not ctx.obj["quiet"]:
            if ctx.obj["pretty"]:
                typer.echo(json.dumps(result, indent=4))
            else:
                typer.echo(json.dumps(result))

    return result
