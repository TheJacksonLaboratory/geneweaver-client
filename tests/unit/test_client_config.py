"""Unit tests for the geneweaver.client.core.config module."""
# ruff: noqa: ANN001, ANN201
# TODO: This instance needs to be provided and configured as a fixture so that
#  it can override which .env files to use for testing.
from geneweaver.client.core.config import Settings, settings


def test_client_settings_schema():
    """Test the Settings class."""
    schema = Settings.schema()
    assert "API_HOST" in schema["properties"]
    assert "API_PATH" in schema["properties"]
    assert "API_URL" in schema["properties"]
    assert "API_KEY" in schema["properties"]


# TODO: This test needs its settings instance to be provided and configured as
#  a fixture so that we can override which .env files to use for testing.
def test_client_settings_default():
    """Test the Settings class."""
    assert settings.API_HOST == "https://geneweaver-prod.jax.org"
    assert settings.API_PATH == "/api/v2"
    assert settings.API_URL == "https://geneweaver-prod.jax.org/api"
    # TODO: See comment above.
    # assert settings.API_KEY is None


def test_client_settings_kwargs():
    """Test the instantiating Settings class with kwargs."""
    these_settings = Settings(
        API_HOST="test_0",
        API_KEY="test_1",
        API_PATH="test_2",
        API_URL="test_3",
    )
    assert these_settings.API_HOST == "test_0"
    assert these_settings.API_KEY == "test_1"
    assert these_settings.API_PATH == "test_2"
    assert these_settings.API_URL == "test_3"


def test_client_settings_kwargs_generate_api_url():
    """Test the instantiating Settings class with kwargs, leaving out API_URL."""
    these_settings = Settings(
        API_HOST="test_0",
        API_KEY="test_1",
        API_PATH="test_2",
    )
    assert these_settings.API_HOST == "test_0"
    assert these_settings.API_KEY == "test_1"
    assert these_settings.API_PATH == "test_2"
    assert these_settings.API_URL == "test_0test_2"
