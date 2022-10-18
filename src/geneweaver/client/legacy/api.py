import requests
from typing import Optional
from geneweaver.core.schema import legacy_api
from geneweaver.client.config import ClientSettings


def add_geneset_by_user(settings: ClientSettings,
                        geneset: legacy_api.AddGenesetByUser,
                        publication: Optional[legacy_api.AddGenesetByUserPublication] = None):
    url = settings.API_HOST + settings.LEGACY_PATHS.ADD_GENESET_BY_USER.format(apikey=settings.API_KEY)
    request_data = geneset.dict(exclude={'publication'})
    if publication is not None:
        request_data.update(publication.dict())
    response = requests.post(url, json=request_data)
    return response


def create_temp_geneset_original(settings: ClientSettings, geneset):
    url = settings.API_HOST + settings.LEGACY_PATHS.CREATE_TEMP_GENESET_ORIGINAL
    response = requests.post(url, json=geneset.dict())
    return response



def add_project_by_user(settings: ClientSettings,
                        project_name: str):
    url = settings.API_HOST + settings.LEGACY_PATHS.ADD_PROJECT_BY_USER.format(
        apikey=settings.API_KEY, project_name=project_name
    )
    response = requests.get(url)
    return response


def add_geneset_to_project(settings: ClientSettings,
                           geneset_id: int,
                           project_id: int):
    url = settings.API_HOST + settings.LEGACY_PATHS.ADD_GENESET_TO_PROJECT.format(
        apikey=settings.API_KEY, geneset_id=geneset_id, project_id=project_id
    )
    response = requests.get(url)
    return response
