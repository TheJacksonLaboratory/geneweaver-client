"""Test the AON symbol map algorithm."""

from typing import Dict, List, Tuple, Union

import pytest
from geneweaver.client.utils.aon import map_symbols


@pytest.mark.parametrize(
    ("original", "mappings", "expected"),
    [
        # Test case: single mapping, direct match
        ({"gene1": 10}, [("gene1", "mouse_gene1")], {"mouse_gene1": 10}),
        # Test case: multiple mappings, direct matches
        (
            {"gene1": 10, "gene2": 20},
            [("gene1", "mouse_gene1"), ("gene2", "mouse_gene2")],
            {"mouse_gene1": 10, "mouse_gene2": 20},
        ),
        # Test case: human gene maps to multiple mouse genes, same score
        (
            {"gene1": 15},
            [("gene1", "mouse_gene1"), ("gene1", "mouse_gene2")],
            {"mouse_gene1": 15, "mouse_gene2": 15},
        ),
        # Test case: multiple human genes map to the same mouse gene,
        # keep highest absolute score
        (
            {"gene1": 10, "gene2": -25},
            [("gene1", "mouse_gene"), ("gene2", "mouse_gene")],
            {"mouse_gene": -25},
        ),
        # Test case: no mapping available
        ({"gene1": 10}, [("gene2", "mouse_gene1")], {}),
        # Test case: one mapping available, one not
        (
            {"gene1": 10, "gene2": 20},
            [("gene1", "mouse_gene1"), ("gene3", "mouse_gene3")],
            {"mouse_gene1": 10},
        ),
        # Test case: multiple mappings to the same mouse gene with same absolute value
        (
            {"gene1": 10, "gene2": -10},
            [("gene1", "mouse_gene"), ("gene2", "mouse_gene")],
            {"mouse_gene": 10},
        ),
    ],
)
def test_map_symbols(
    original: Dict[str, Union[int, float]],
    mappings: List[Tuple[str, str]],
    expected: Dict[str, Union[int, float]],
):
    """Test that the function correctly maps gene symbols."""
    result = map_symbols(original, mappings)
    assert result == expected


@pytest.mark.parametrize(
    ("original", "mappings"),
    [
        # Test case: empty original
        ({}, [("gene1", "mouse_gene1")]),
        # Test case: empty mappings
        ({"gene1": 10}, []),
    ],
)
def test_map_symbols_empty_cases(
    original: Dict[str, Union[int, float]], mappings: List[Tuple[str, str]]
):
    """Test that the function returns an empty dictionary when given empty input."""
    result = map_symbols(original, mappings)
    assert result == {}


@pytest.mark.parametrize(
    ("original", "mappings", "expected_exception"),
    [
        # Test case: mappings contain non-hashable keys
        ({"gene1": 10}, [([1, 2, 3], "mouse_gene1")], TypeError),
        ({"gene3": 0}, [({1, 2, 3}, "mouse_gene1")], TypeError),
        ({"gene4": 9}, [([1], "mouse_gene1")], TypeError),
        ({"gene8": 98123}, [({2}, "mouse_gene1")], TypeError),
        # Test case: original contains non-numeric values
        (
            {"gene1": "10", "gene2": "9"},
            [("gene1", "mouse_gene1"), ("gene2", "mouse_gene1")],
            TypeError,
        ),
        (
            {"gene4": "10", "gene8": "9"},
            [("gene4", "mapped_1"), ("gene8", "mapped_1")],
            TypeError,
        ),
    ],
)
def test_map_symbols_exceptions(
    original: Dict[Union[str, int], Union[int, float]],
    mappings: List[Tuple[Union[str, int], str]],
    expected_exception,
):
    """Test that the function raises the expected exception when given invalid input."""
    with pytest.raises(expected_exception):
        map_symbols(original, mappings)
