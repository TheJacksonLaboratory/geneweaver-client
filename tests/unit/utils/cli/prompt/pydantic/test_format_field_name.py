"""Test the format field name function."""
import pytest
from geneweaver.client.utils.cli.prompt.pydantic import format_field_name


@pytest.mark.parametrize(
    ("field_name", "expected_output"),
    [
        ("test_field", "Test field"),
        ("test_field_1", "Test field 1"),
        ("test_field_1_2", "Test field 1 2"),
        ("TEST_FIELD", "Test field"),
        ("TEST_FIELD_1", "Test field 1"),
        ("TEST_FIELD_1_2", "Test field 1 2"),
    ],
)
def test_format_field_name(field_name, expected_output):
    """Test the format_field_name function."""
    assert format_field_name(field_name) == expected_output
