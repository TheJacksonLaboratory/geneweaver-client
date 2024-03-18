"""Test the genes API client functions."""

from unittest.mock import patch

import pytest
from geneweaver.client.api import genes
from geneweaver.core.enum import GeneIdentifier, Species


@pytest.mark.parametrize(
    (
        "source_ids",
        "target_id_type",
        "source_id_type",
        "target_species",
        "source_species",
    ),
    [
        (["MGI:1918914"], "MGI", None, None, None),
        (["MGI:1918914"], "MGI", "MGI", None, None),
        (["MGI:1918914"], "MGI", "MGI", "Mus musculus", None),
        (["MGI:1918914"], "MGI", "MGI", "Mus musculus", "Mus musculus"),
    ],
)
def test_map_homologs(
    source_ids, target_id_type, source_id_type, target_species, source_species
):
    """Test the map_homologs function."""
    kwargs = {
        "source_ids": source_ids,
        "target_id_type": GeneIdentifier(target_id_type),
    }
    if source_id_type is not None:
        kwargs["source_id_type"] = GeneIdentifier(source_id_type)

    if target_species is not None:
        kwargs["target_species"] = Species(target_species)

    if source_species is not None:
        kwargs["source_species"] = Species(source_species)

    with patch("geneweaver.client.api.genes.sessionmanager") as mock_sessionmanager:
        (
            mock_sessionmanager.return_value.__enter__.return_value.post.return_value.json.return_value
        ) = {"gene_ids_map": {source_ids[0]: ["MGI:1918914.1"]}}
        genes.map_homologs("fake_access_token", **kwargs)
