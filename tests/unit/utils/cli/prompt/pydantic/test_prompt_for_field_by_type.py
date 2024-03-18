"""Test the prompt_for_field_by_type function."""

from unittest.mock import Mock

import pytest
from geneweaver.client.utils.cli.prompt.pydantic import prompt_for_field_by_type

from tests.unit.utils.cli.prompt.pydantic.conftest import (
    MockModel,
)


@pytest.mark.parametrize(("field_name", "field"), MockModel.__fields__.items())
def test_prompt_for_field_by_type(field_name, field, monkeypatch):
    """Test the prompt_for_field_by_type function."""
    mock_prompt_for_missing_fields = Mock()
    mock_prompt_for_enum_selection = Mock()
    mock_prompt_for_list_selection = Mock()
    mock_prompt_for_bool = Mock()
    mock_prompt_generic = Mock()
    monkeypatch.setattr(
        "geneweaver.client.utils.cli.prompt.pydantic.prompt_for_missing_fields",
        mock_prompt_for_missing_fields,
    )
    monkeypatch.setattr(
        "geneweaver.client.utils.cli.prompt.pydantic.prompt_for_enum_selection",
        mock_prompt_for_enum_selection,
    )
    monkeypatch.setattr(
        "geneweaver.client.utils.cli.prompt.pydantic.prompt_for_list_selection",
        mock_prompt_for_list_selection,
    )
    monkeypatch.setattr(
        "geneweaver.client.utils.cli.prompt.pydantic.prompt_for_bool",
        mock_prompt_for_bool,
    )
    monkeypatch.setattr(
        "geneweaver.client.utils.cli.prompt.pydantic.prompt_generic",
        mock_prompt_generic,
    )

    prompt_for_field_by_type(field, field_name, {})

    assert (
        sum(
            (
                mock_prompt_for_missing_fields.call_count,
                mock_prompt_for_enum_selection.call_count,
                mock_prompt_for_list_selection.call_count,
                mock_prompt_for_bool.call_count,
                mock_prompt_generic.call_count,
            )
        )
        == 1
    )
