"""Test the prompt_to_keep_field function."""
from unittest.mock import Mock

import pytest
from geneweaver.client.utils.cli.prompt.pydantic import prompt_to_keep_field


@pytest.mark.parametrize("field_name", ["prompt_field", "prompt_field_2"])
@pytest.mark.parametrize(
    "input_dict",
    [
        {"test_field": "test_value"},
        {"test_field": "test_value", "test_field_2": "test_value_2"},
        {},
    ],
)
@pytest.mark.parametrize("field_in_dict", [True, False])
@pytest.mark.parametrize("response", [True, False])
def test_prompt_to_keep_field(
    field_name, input_dict, field_in_dict, response, monkeypatch
):
    """Test the prompt_to_keep_field function."""
    mock_prompt = Mock(return_value=response)
    monkeypatch.setattr(
        "geneweaver.client.utils.cli.prompt.pydantic.typer.confirm", mock_prompt
    )

    if field_in_dict:
        input_dict[field_name] = "test_value"

    result = prompt_to_keep_field(input_dict, field_name)

    if response is True:
        assert field_name in input_dict
        assert field_name in result
    else:
        assert field_name not in input_dict
        assert field_name not in result

    assert result == input_dict
    assert result is input_dict

    if field_in_dict:
        assert mock_prompt.call_count == 1
