"""Test the genesets API client functions."""

from unittest.mock import patch

import pytest
from geneweaver.client.api import genesets
from geneweaver.core.enum import GeneIdentifier


@pytest.mark.parametrize(
    ("geneset_id", "gene_id_type"),
    [
        (1, GeneIdentifier.MGI),
        (123456, None),
    ],
)
def test_get(geneset_id, gene_id_type):
    """Test the get function."""
    kwargs = {
        "geneset_id": geneset_id,
    }
    if gene_id_type is not None:
        kwargs["gene_id_type"] = GeneIdentifier(gene_id_type)

    with patch("geneweaver.client.api.genesets.sessionmanager") as mock_sessionmanager:
        (
            mock_sessionmanager.return_value.__enter__.return_value.get.return_value.json.return_value
        ) = {
            "geneset": {"geneset_id": geneset_id},
            "geneset_values": [{"geneset_id": geneset_id}],
        }
        result = genesets.get("fake_access_token", geneset_id, gene_id_type)
        assert result["geneset"]["geneset_id"] == geneset_id
        assert result["geneset_values"][0]["geneset_id"] == geneset_id
        assert (
            mock_sessionmanager.return_value.__enter__.return_value.get.call_count == 1
        )
        assert (
            mock_sessionmanager.return_value.__enter__.return_value.get.return_value.json.call_count
            == 1
        )


def test_get_genesets():
    """Test the get_genesets function."""
    with patch("geneweaver.client.api.genesets.sessionmanager") as mock_sessionmanager:
        (
            mock_sessionmanager.return_value.__enter__.return_value.get.return_value.json.return_value
        ) = [{"geneset_id": 1}, {"geneset_id": 2}]
        result = genesets.get_genesets("fake_access_token")
        assert len(result) == 2
        assert result[0]["geneset_id"] == 1
        assert result[1]["geneset_id"] == 2
        assert (
            mock_sessionmanager.return_value.__enter__.return_value.get.call_count == 1
        )
        assert (
            mock_sessionmanager.return_value.__enter__.return_value.get.return_value.json.call_count
            == 1
        )


def test_get_values():
    """Test the get_values function."""
    with patch("geneweaver.client.api.genesets.sessionmanager") as mock_sessionmanager:
        (
            mock_sessionmanager.return_value.__enter__.return_value.get.return_value.json.return_value
        ) = {"data": [{"gene1": 1.0}, {"gene2": 2.0}]}
        result = genesets.get_values("fake_access_token", 123)
        assert "data" in result
        assert len(result["data"]) == 2
        assert result["data"][0]["gene1"] == 1.0
        assert result["data"][1]["gene2"] == 2.0
        assert (
            mock_sessionmanager.return_value.__enter__.return_value.get.call_count == 1
        )
        assert (
            mock_sessionmanager.return_value.__enter__.return_value.get.return_value.json.call_count
            == 1
        )
