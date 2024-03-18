"""Test the is_list_of_str_or_int function."""

from typing import Any, List, Tuple, Union

import pytest
from geneweaver.client.utils.cli.prompt.list import is_list_of_str_or_int


@pytest.mark.parametrize("field_type", [List[str], List[int]])
def test_is_list_of_str_or_int(field_type):
    """Test the is_list_of_str_or_int function."""
    assert is_list_of_str_or_int(field_type) is True


@pytest.mark.parametrize(
    "field_type",
    [List[float], List[bool], List[dict], dict, Tuple, Any, Union[str, int]],
)
def test_is_list_of_str_or_int__false(field_type):
    """Test the is_list_of_str_or_int function with invalid input."""
    assert is_list_of_str_or_int(field_type) is False
