"""Test the `api.mapping` module."""

from unittest.mock import patch

import pytest
from geneweaver.client.api import mapping
from geneweaver.client.api.aon import OrthologAlgorithms
from geneweaver.core.enum import Species


@pytest.mark.parametrize("species_id", [int(species) for species in Species])
@pytest.mark.parametrize("algorithm", [algorithm for algorithm in OrthologAlgorithms])
@patch("geneweaver.client.api.mapping.genesets.get")
@patch("geneweaver.client.api.mapping.genesets.get_values")
@patch("geneweaver.client.api.mapping.aon.algorithm_id_from_name")
@patch("geneweaver.client.api.mapping.aon.ortholog_mapping")
@patch("geneweaver.client.api.mapping.map_symbols")
@patch("geneweaver.client.api.mapping.genes.mappings")
def test_ensembl_mouse_mapping(
    mock_genes_mappings,
    mock_aon_map_symbols,
    mock_aon_ortholog_mapping,
    mock_aon_algorithm_id_from_name,
    mock_genesets_get_values,
    mock_genesets_get,
    algorithm,
    species_id,
):
    """Test the `ensembl_mouse_mapping` function."""
    mock_genesets_get.return_value = {"geneset": {"species_id": species_id}}
    mock_genesets_get_values.return_value = {
        "data": [{"symbol": "A", "value": "1"}, {"symbol": "B", "value": "2"}]
    }
    mock_aon_algorithm_id_from_name.return_value = 1
    mock_aon_ortholog_mapping.return_value = [
        {"from_gene": "A", "to_gene": "A1"},
        {"from_gene": "B", "to_gene": "B1"},
    ]
    mock_genes_mappings.return_value = {
        "gene_ids_map": [
            {"original_ref_id": "A1", "mapped_ref_id": "A2"},
            {"original_ref_id": "B1", "mapped_ref_id": "B2"},
        ]
    }

    mock_aon_map_symbols.side_effect = [{"A1": "1", "B1": "2"}, {"A2": "1", "B2": "2"}]

    result = mapping.ensembl_mouse_mapping(
        "fake_access_token", 123, True, OrthologAlgorithms.HGNC
    )

    assert mock_genesets_get.call_count == 1
    assert mock_genesets_get_values.call_count == 1

    if species_id == 1:
        assert result == [{"symbol": "A", "value": "1"}, {"symbol": "B", "value": "2"}]
        expected_api_calls, expected_mapping_calls = 0, 0

    else:
        assert result == [
            {"symbol": "A2", "value": "1"},
            {"symbol": "B2", "value": "2"},
        ]
        expected_api_calls, expected_mapping_calls = 1, 2

    assert mock_aon_algorithm_id_from_name.call_count == expected_api_calls
    assert mock_aon_ortholog_mapping.call_count == expected_api_calls
    assert mock_genes_mappings.call_count == expected_api_calls
    assert mock_aon_map_symbols.call_count == expected_mapping_calls
