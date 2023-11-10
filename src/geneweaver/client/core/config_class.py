"""GeneWeaver Client configuration module."""
from typing import Optional, Type

from pydantic import BaseSettings, validator


class Settings(BaseSettings):
    """Settings class for GeneWeaver Client."""

    AUTH_DOMAIN = "geneweaver.auth0.com"
    AUTH_CLIENT_ID = "tvcvnbBJQr15jFds8ZkwgHoqRJ0IuGJC"
    AUTH_ALGORITHMS = ["RS256"]
    AUTH_SCOPES = ["openid", "profile", "email"]

    API_HOST: str = "https://geneweaver.org"
    API_V1_PATH: str = "/api/v1"
    API_V2_PATH: str = "/api/v2"
    API_V3_PATH: str = "/api/v3"
    API_PATH: Optional[dict] = None

    def api_v3_path(self):
        return self.API_HOST + self.API_V3_PATH

    @validator("API_PATH")
    def validate_api_path(
        cls: Type["ClientSettings"], v: Optional[dict], values: dict  # noqa: N805
    ) -> dict:
        """Construct the API URL if not explicitly set."""
        if not v:
            return {
                "v1": values["API_HOST"] + values["API_V1_PATH"],
                "v2": values["API_HOST"] + values["API_V2_PATH"],
                "v3": values["API_HOST"] + values["API_V3_PATH"],
            }
        return v

    API_URL: Optional[str] = None

    class Config:
        """Settings configuration."""

        env_file = ".env"
        env_prefix = "GW_CLIENT_"
