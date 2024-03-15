"""
This module contains a client API for interacting with the 
gene expression service. The search operations on the db 
are supported using a json object. This intentionally
obfuscates the underlying BigQuery database for the reasons
of security and scalability.
"""
from dataclasses import dataclass
from typing import List

from enum import Enum
import requests
import json
import csv

from geneweaver.core.config import settings

SourceType = Enum('Source', ['IMPUTED', 'EXPERIMENT'])
"""
The source either experimentally determined or imputed using 
machine learning ridge regression. For strain recommender, the
imputed sources are most often used.
@usage: from org.jax.gedb import SourceType
"""

# TODO Should data access objects go in api?
@dataclass
class DataRequest:
    """
    This request mirrors the available fields in:
    gene-expr-service/src/main/java/org/jax/jcpg/dao/DataRequest.java
    You cannot rename fields in the client without breaking the API
    These are a subset of the fields. TODO (low priority): Add all.
    """
    geneIds: List[str] = None
    strains: List[str] = None
    sourceType: SourceType = None
 
# TODO Should data access objects go in api?
@dataclass
class DataResult:
    """
    This result mirrors the available fields in:
    gene-expr-service/src/main/java/org/jax/jcpg/dao/DataResult.java
    You cannot rename fields in the client without breaking the API.
    These are a subset of the fields. TODO (low priority): Add all.
    """
    values: List[float] = None
    weights: List[float] = None
    geneIds: List[str] = None
    strains: List[str] = None
    tissue: str = None
     
class GeneExpressionDatabaseClient():
    """
    This is the client object to which you make DataRequests and from which
    you get a list of DataResults for your search. It is possible to construct
    searches which the server takes a very long time to construct. In general 
    the examples of supported searches are listed on the swagger page of the server.
    e.g. at https://geneweaver-dev.jax.org/gedb/ under for instance the 'gene/expression/search'
    endpoint.
    """
    
    def __init__(self, url: str = settings.GEDB):
       """
       Create a GeneExpressionDatabaseClient from a URL.
       @param url: The URL to which we will connect when making gedb server queries.
       """
       self.url = url

  
    def search(self, drequest: DataRequest) -> List[DataResult]:
        """
        Do a gene expression search on the Gene Expression Database
        using fields available in the DataRequest object.
        @param drequest: The request which we want to make to the client
        to get results.
        """
        url = self._get_search_url()
        
        response = requests.post(url, None, drequest.__dict__)
        if not response.ok:
            response.raise_for_status()
        
        # TODO Not sure if need to deal with typing here.
        # Need to write test to check.
        return json.loads(response.text)
    
    def distinct(self, field: str) -> List[str]:
        """
        Get list of unique fields from metadata.
        For instance to get the strains return field = "tissue"
        Available fields are listed in swagger e.g. https://geneweaver-dev.jax.org/gedb/ under 
        meta/distinct/strain.
        """
        url = "{}/{}".format(self._get_distinct_url(), field)
        return json.loads(requests.get(url).text)
    
    def _get_search_url(self):
        return "{}{}".format(self.url, "gene/expression/search")
    
    def _get_distinct_url(self):
        return "{}{}".format(self.url, "meta/distinct")
