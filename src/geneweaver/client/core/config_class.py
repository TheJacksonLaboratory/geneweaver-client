"""GeneWeaver Client configuration module."""

from typing import Optional, Type

from pydantic import BaseSettings, validator


class Settings(BaseSettings):
    """Settings class for GeneWeaver Client."""

    AUTH_DOMAIN = "geneweaver.auth0.com"
    AUTH_CLIENT_ID = "tvcvnbBJQr15jFds8ZkwgHoqRJ0IuGJC"
    AUTH_ALGORITHMS = ["RS256"]
    AUTH_SCOPES = ["openid", "profile", "email", "offline_access"]

    API_HOST: str = "https://geneweaver-prod.jax.org"
    API_PATH: str = "/api"

    API_URL: Optional[str] = None

    GEDB: Optional[str] = None

    @validator("API_URL")
    def validate_api_url(
        cls: Type["Settings"], v: Optional[str], values: dict  # noqa: N805
    ) -> str:
        """Construct the API URL if not explicitly set."""
        if not v:
            return values["API_HOST"] + values["API_PATH"]
        return v

    API_KEY: Optional[str] = None

    @validator("GEDB")
    def validate_gedb_url(
        cls: Type["Settings"], v: Optional[str], values: dict  # noqa: N805
    ) -> str:
        """Construct the GEDB if not explicitly set."""
        if not v:
            return values["API_HOST"] + "/gedb"
        return v

    class Config:
        """Settings configuration."""

        env_file = ".env"
        env_prefix = "GW_CLIENT_"
