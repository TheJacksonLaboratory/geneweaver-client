# noqa: E501
"""Gene expression service.

The search operations on the db
are supported using a json object. This intentionally
wraps the underlying BigQuery database for the reasons
of security and scalability.
"""
import io
from collections import OrderedDict
from dataclasses import dataclass, fields
from enum import Enum
from io import StringIO
from typing import List, Mapping, Set

import numpy
import pandas
import requests
from geneweaver.client.core.config import settings
from pandas import DataFrame
from requests.models import Response

SourceType = Enum("Source", ["IMPUTED", "EXPERIMENT"])
"""
The source either experimentally determined or imputed using
machine learning ridge regression. For strain recommender, the
imputed sources are most often used.
@usage: from org.jax.gedb import SourceType
"""

Sex = Enum("Sex", ["Female", "Male", "Both"])
"""
The imputed sex field. This is not direct biological sex
but a representation of the input sex(s) to the alg.
"""


# TODO Should data access objects go in api?
@dataclass
class DataRequest:
    """Object to request data e.g. a search.

    This request mirrors the available fields in:
    gene-expr-service/src/main/java/org/jax/jcpg/dao/DataRequest.java
    You cannot rename fields in the client without breaking the API
    These are a subset of the fields. TODO (low priority): Add all.
    """

    geneIds: List[str] = None  # noqa: N815
    strains: List[str] = None  # noqa: N815
    tissue: str = None  # noqa: N815
    sourceType: SourceType = None  # noqa: N815


# TODO Should data access objects go in api?
@dataclass
class DataResult:
    """Object which contains results.

    This result mirrors the available fields in:
    gene-expr-service/src/main/java/org/jax/jcpg/dao/DataResult.java
    You cannot rename fields in the client without breaking the API.
    These are a subset of the fields. TODO (low priority): Add all.
    """

    values: List[float] = None  # noqa: N815
    names: List[str] = None  # noqa: N815
    weights: List[float] = None  # noqa: N815
    geneIds: List[str] = None  # noqa: N815
    strains: List[str] = None  # noqa: N815
    strain: str = None  # noqa: N815
    tissue: str = None  # noqa: N815
    sexes: List[str] = None  # noqa: N815


@dataclass
class StrainResult:
    """Object which contains results for strain search."""

    gene_ids: List[str] = None  # noqa: N815
    gene_names: List[str] = None  # noqa: N815
    strain: str = None  # noqa: N815
    strain_expressions: Mapping[str, List[float]] = None  # noqa: N815


@dataclass
class NullVarianceRequest:
    """Simple object for getting spearmanrho variance."""

    id: str = None  # noqa: N815
    scores: List[float] = None  # noqa: N815
    rSz: int = 1000  # noqa: N815


# TODO Should data access objects go in api?
@dataclass
class Metadata:
    """Object to contain Metadata.

    The Metadata is available for various properties by searching
    the database.
    """

    ingestid: str = None  # noqa: N815
    modelversion: str = None  # noqa: N815
    population: str = None  # noqa: N815
    tissue: str = None  # noqa: N815
    sourcetype: SourceType = None  # noqa: N815
    species: str = None  # noqa: N815
    uberon: str = None  # noqa: N815
    bucketname: str = None  # noqa: N815
    dataobject: str = None  # noqa: N815
    weightobject: str = None  # noqa: N815
    metaobject: str = None  # noqa: N815


@dataclass
class Bulk:
    """Object to contain Bulk expression data."""

    genename: str = None  # noqa: N815
    geneid: str = None  # noqa: N815
    exprnames: List[str] = None  # noqa: N815
    exprvalues: List[float] = None  # noqa: N815
    weightvalues: List[float] = None  # noqa: N815
    ingestid: str = None  # noqa: N815


class GeneExpressionDatabaseClient:
    """Gene Expression Database Client.

    Client object to which you make DataRequests and from which
    you get a list of DataResults for your search. It is possible to construct
    searches which the server takes a very long time to construct. In general
    the examples of supported searches are listed on the swagger page of the server.
    e.g. at https://geneweaver-dev.jax.org/gedb/ under for instance
    the 'gene/expression/search' endpoint.
    """

    def __init__(self, url: str = None, auth_proxy: str = None) -> None:
        """Create a GeneExpressionDatabaseClient from a URL.

        @param url: The optional URL to which we will connect
        when making gedb server queries.
        @param auth_proxy: The optional value of a cookie to
        connect to https version of the API.
        """
        if url is None:
            url = settings.GEDB
        self.url = url
        self.auth_proxy = auth_proxy

    def search(self, drequest: DataRequest) -> List[DataResult]:
        """Do a gene expression search on the Gene Expression Database.

        using fields available in the DataRequest object.
        @param drequest: The request which we want to make to the client
        to get results.
        """
        url = self._get_search_url()

        response = self._post(url, drequest.__dict__)

        # TODO Not sure if need to deal with typing here.
        # Need to write test to check.
        return [self._class_from_args(DataResult, item) for item in response.json()]

    def search_expression(self, drequest: DataRequest) -> List[StrainResult]:
        """Do a gene expression search on the Gene Expression Database.

        using fields available in the DataRequest object.
        This call is the same as search, however it specifically
        orders the expressions by strain, individual and sex which
        is the required ordering for concordance calculation.

        @param drequest: The request which we want to make to the client
        to get results.
        """
        url = self._get_search_expression_url()

        response = self._post(url, drequest.__dict__)

        # TODO Not sure if need to deal with typing here.
        # Need to write test to check.
        return [self._class_from_args(StrainResult, item) for item in response.json()]

    def distinct(self, field: str) -> Set[str]:
        """Get list of unique fields from metadata.

        @param field: For instance to get the
         strains return field = "tissue"
        Available fields are listed in swagger
        e.g. https://geneweaver-dev.jax.org/gedb/ under
        meta/distinct/strain.
        """
        url = "{}/{}".format(self._get_distinct_url(), field)

        response = self._get(url)

        return response.json()

    def get_meta(self, tissue: str) -> List[Metadata]:
        """Get metadata from database."""
        url = "{}/{}".format(self._get_meta_url(), tissue)
        response = self._get(url)
        return [self._class_from_args(Metadata, item) for item in response.json()]

    def _class_from_args(self, class_name: object, arg_dict: dict) -> object:
        field_set = {f.name for f in fields(class_name) if f.init}
        filtered = {k: v for k, v in arg_dict.items() if k in field_set}
        return class_name(**filtered)

    def read_expression_data(self, ingest_id: str) -> DataFrame:
        """Get expression data from database.

        Reads full data for a given ingest_id, inefficient and slow.
        Do not use, too slow, use search and
        """
        url = "{}/{}".format(self._get_bulk_url(), ingest_id)

        with requests.Session() as s:
            download = s.get(url)
            decoded_content = download.content.decode("utf-8")
            frame: DataFrame = pandas.read_csv(io.StringIO(decoded_content))
            return frame

    def sort_by_field(
        self, prop: str, expressions: List[DataResult]
    ) -> Mapping[str, List[DataResult]]:
        """Sort the data results by any of their properties.

        @param property: String e.g. "strain" to sort by strain
        @param the raw list of data results returned from a 'search' call.
        """
        ret = {}
        for dr in expressions:
            pvalue = getattr(dr, prop)

            collection = ret.get(pvalue, None)
            if collection is None:
                collection = []
                ret[pvalue] = collection
            collection.append(dr)

        return ret

    def frame(
        self, data: Mapping[str, StrainResult], strain: str, indiv_name: str, sex: Sex
    ) -> DataFrame:
        """Convert a dictionary of gene expression to frame."""
        res: StrainResult = data[strain]

        ids: List[str] = res.gene_ids
        exprs: List[float] = res.strain_expressions[
            "{}@{}".format(indiv_name, sex.name)
        ]
        ret: DataFrame = pandas.DataFrame(
            {"gene_id": numpy.array(ids), "expr": numpy.array(exprs)}
        )
        return ret

    def random(self, ingest_id: str, size: int, count: int = 1) -> List[DataFrame]:
        """Get a random gene expression frame.

        @param ingest_id: from which we ingested data
        @param size: size of the geneset
        """
        url = "{}/{}?gsize={}&random_size={}".format(
            self._get_random_url(), ingest_id, size, count
        )
        response = self._get(url)

        csv_data: List[str] = list(response.text.split("\n"))

        # We return them as one long array which should be faster on the BQ side.
        # Then we split them into sections of size count
        ret: List[List[str]] = self._split_list(csv_data, size)

        return [self._frame(r) for r in ret]

    def random_spearmanrho(
        self, ingest_id: str, scores: List[float], r_size: int = 1, timeout: int = 3600
    ) -> List[float]:
        """Get a random gene expression frame and process random rhos.

        @param ingest_id: from which we ingested data
        @param size: size of the geneset
        """
        url = self._get_random_spearmanrho_url()
        nvr: NullVarianceRequest = NullVarianceRequest(
            id=ingest_id, scores=list(scores), rSz=r_size
        )
        response = self._post(url, nvr.__dict__, timeout=timeout)

        rhos: List[float] = response.json()

        return rhos

    def _split_list(self, lst: List, chunk_size: int) -> List[List]:
        return list(zip(*[iter(lst)] * chunk_size))

    def _frame(self, randoms: List[str]) -> DataFrame:
        # Make them into a frame.
        csv_content = "\n".join(randoms) + "\n"
        csv_content = "{}{}".format("indiv_name,score\n", csv_content)
        ret: DataFrame = pandas.read_csv(StringIO(csv_content))
        return ret

    def _get_search_url(self) -> str:
        return "{}{}".format(self.url, "/gene/expression/search")

    def _get_search_expression_url(self) -> str:
        return "{}{}".format(self.url, "/gene/expression/search-expression")

    def _get_distinct_url(self) -> str:
        return "{}{}".format(self.url, "/meta/distinct")

    def _get_meta_url(self) -> str:
        return "{}{}".format(self.url, "/meta/where/tissue/is")

    def _get_bulk_url(self) -> str:
        return "{}{}".format(self.url, "/bulk/all/where/ingest/is")

    def _get_random_url(self) -> str:
        return "{}{}".format(self.url, "/bulk/random/where/ingest/is")

    def _get_random_spearmanrho_url(self) -> str:
        return "{}{}".format(self.url, "/bulk/random/spearmanrho/")

    def _post(self, url: str, postable_object: dict, timeout: int = 3600) -> Response:

        cookies = None
        if self.auth_proxy is not None:
            cookies = {"_oauth2_proxy": self.auth_proxy}

        with requests.Session() as s:
            response = s.post(
                url, None, postable_object, cookies=cookies, timeout=timeout
            )

            if not response.ok:
                response.raise_for_status()

            return response

    def _get(self, url: str) -> Response:

        cookies = None
        if self.auth_proxy is not None:
            cookies = {"_oauth2_proxy": self.auth_proxy}

        with requests.Session() as s:
            response = s.get(url, cookies=cookies)

            if not response.ok:
                response.raise_for_status()

            return response

    def read_scores(self, path: str) -> Mapping[str, str]:
        """Will read first two columns of csv file.

        into a dictionary of gene: log2fc for use in concordance calc.
        @param path: Path to read.
        """
        # We keep the keys in order here as
        # it is easier to use the debugger and
        # check the dict
        gene_values = OrderedDict()
        with open(path, "r") as file:
            # reading each line from original text file
            for line in file.readlines():
                line = line.strip()
                if not (line.startswith("#")):
                    sa = line.split(",")
                    # Ingore other columns, just use first two.
                    gene_values[sa[0]] = sa[1]

        return gene_values
