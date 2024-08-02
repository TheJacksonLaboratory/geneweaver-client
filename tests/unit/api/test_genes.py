"""Test the genes API client functions."""

from unittest.mock import patch

import pytest
from geneweaver.client.api import genes
from geneweaver.core.enum import GeneIdentifier, Species


@pytest.mark.parametrize(
    (
        "source_ids",
        "target_id_type",
        "species",
    ),
    [
        (["MGI:1918914"], "MGI", "Homo Sapiens"),
        (["MGI:1918914"], "MGI", "Mus Musculus"),
        (["MGI:1918914", "MGI:1918915"], "MGI", "Mus Musculus"),
        (["MGI:1918914", "MGI:1918915"], "Ensemble Gene", "Mus Musculus"),
    ],
)
def test_map_homologs(source_ids, target_id_type, species):
    """Test the map_homologs function."""
    kwargs = {
        "source_ids": source_ids,
        "target_id_type": GeneIdentifier(target_id_type),
    }

    if species is not None:
        kwargs["species"] = Species(species)

    with patch("geneweaver.client.api.genes.sessionmanager") as mock_sessionmanager:
        (
            mock_sessionmanager.return_value.__enter__.return_value.post.return_value.json.return_value
        ) = {"gene_ids_map": {source_ids[0]: ["MGI:1918914.1"]}}
        genes.mappings("fake_access_token", **kwargs)
