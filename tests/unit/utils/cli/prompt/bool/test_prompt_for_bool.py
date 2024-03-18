"""Test the prompt_for_bool function."""

from unittest.mock import Mock

import pytest
from geneweaver.client.utils.cli.prompt.bool import prompt_for_bool


@pytest.mark.parametrize("field_name", ["test", "test_field", "test_field_name", None])
def test_prompt_for_bool(field_name, monkeypatch):
    """Test the prompt_for_bool function."""
    mock_prompt = Mock()
    monkeypatch.setattr(
        "geneweaver.client.utils.cli.prompt.bool.typer.confirm", mock_prompt
    )
    assert mock_prompt.call_count == 0

    prompt_for_bool(field_name)

    assert mock_prompt.call_count == 1
    if field_name is not None:
        assert f"{field_name.capitalize()}" in mock_prompt.call_args_list[0][0][0]
    else:
        assert "Please enter a boolean value" in mock_prompt.call_args_list[0][0][0]
