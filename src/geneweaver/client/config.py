"""GeneWeaver Client configuration module."""
from typing import Optional, Type

from pydantic import BaseModel, BaseSettings, validator


class LegacyClientPaths(BaseModel):
    """Configuration schema for legacy client paths."""

    KEYWORD_SEARCH_GUEST: str = "/api/get/search/bykeyword/{apikey}/{search_term}/"

    GET_GENESETS_BY_GENE_REF_ID: str = (
        "/api/get/geneset/bygeneid/{apikey}/{gene_ref_id}/{gdb_name}/"
    )
    GET_GENESETS_BY_GENE_REF_ID_HOMOLOGY: str = (
        "/api/get/geneset/bygeneid/{apikey}/{gene_ref_id}/{gdb_name}/homology"
    )
    GET_GENESET_BY_USER: str = "/api/get/geneset/byuser/{apikey}/"
    GET_ONTOLOGY_BY_GENESET_ID: str = (
        "/api/get/ontologies/bygeneset/{apikey}/{geneset_id}/"
    )

    GET_GENESET_BY_ID: str = "/api/get/geneset/byid/{genesetid}/"
    GET_GENES_BY_GENESET_ID: str = "/api/get/genes/bygenesetid/{geneset_id}/"

    GET_GENE_BY_GENE_ID: str = "/api/get/gene/bygeneid/{gene_id}/"
    GET_PROJECTS_BY_USER: str = "/api/get/project/byuser/{apikey}/"
    GET_GENESET_BY_PROJECT_ID: str = (
        "/api/get/geneset/byprojectid/{apikey}/{project_id}/"
    )
    GET_PROBES_BY_GENE: str = "/api/get/probes/bygeneid/{apikey}/{gene_ref_id}/"
    GET_PLATFORM_BY_ID: str = "/api/get/platform/byid/{apikey}/{platform_id}/"
    GET_SNP_BY_GENE_ID: str = "/api/get/snp/bygeneid/{apikey}/{gene_ref_id}/"
    GET_PUBLICATION_BY_ID: str = "/api/get/publication/byid/{apikey}/{publication_id}/"
    GET_SPECIES_BY_ID: str = "/api/get/species/byid/{apikey}/{species_id}/"
    GET_RESULTS_BY_USER: str = "/api/get/results/byuser/{apikey}/"
    GET_RESULT_BY_TASK_ID: str = "/api/get/result/bytaskid/{apikey}/{task_id}/"
    GET_GENE_DATABASE_BY_ID: str = (
        "/api/get/genedatabase/byid/{apikey}/{gene_database_id}/"
    )

    ADD_PROJECT_BY_USER: str = "/api/add/project/byuser/{apikey}/{project_name}/"
    ADD_GENESET_TO_PROJECT: str = (
        "/api/add/geneset/toproject/{apikey}/{project_id}/{geneset_id}/"
    )
    ADD_GENESET_BY_USER: str = "/api/add/geneset/byuser/{apikey}/"

    DELETE_GENESET_FROM_PROJECT: str = (
        "/api/delete/geneset/fromproject/{apikey}/{project_id}/{geneset_id}/"
    )

    ADD_PROJECT_BY_NAME: str = "/addProjectByName"

    CREATE_TEMP_GENESET_ORIGINAL: str = "/createtempgeneset_original"
    CREATE_TEMP_GENESET_LARGE: str = "/createtempgeneset_large"


class ClientSettings(BaseSettings):
    """Settings class for GeneWeaver Client."""

    AUTH_DOMAIN = "geneweaver.auth0.com"
    AUTH_CLIENT_ID = "tvcvnbBJQr15jFds8ZkwgHoqRJ0IuGJC"
    AUTH_ALGORITHMS = ["RS256"]
    AUTH_SCOPES = ["openid", "profile", "email"]

    API_HOST: str = "https://geneweaver.org"
    API_PATH: str = "/api/v2"

    API_URL: Optional[str] = None

    LEGACY_PATHS: LegacyClientPaths = LegacyClientPaths()

    @validator("API_URL")
    def validate_api_url(
        cls: Type["ClientSettings"], v: Optional[str], values: dict  # noqa: N805
    ) -> str:
        """Construct the API URL if not explicitly set."""
        if not v:
            return values["API_HOST"] + values["API_PATH"]
        return v

    API_KEY: Optional[str] = None

    class Config:
        """Settings configuration."""

        env_file = ".env"
        env_prefix = "GW_CLIENT_"


settings = ClientSettings()
