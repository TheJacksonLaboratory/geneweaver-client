"""A module to interact with the graph service.

This module contains a client API for interacting with the
graph service. The find and search operations on the graph
are supported. The find is used for variant mapping and can
include long-running searches, for instance 100k variants
mapped from one species to another. The search contains simpler
and shorter running operations, for instance to get orthologs.
This intentionally obfuscates the underlying graph database
for the reasons of security and scalability.
"""

# ruff: noqa: E501, N803
import csv
import json
from enum import Enum
from typing import Optional

import requests

Source = Enum("Source", ["BAYLOR", "HOMOLOGENE" "ENSEMBL"])
"""
@usage: from geneweaver.client.api.graph import Source
"""

SearchType = Enum(
    "SearchType",
    [
        "EQTL_BP_TO_GENES",
        "EQTL_TISSUE_TO_GENES",
        "GENE_ID",
        "PEAKS",
        "EQTL_BP_TO_PEAKS",
        "ORTHOLOG",
    ],
)
"""
@usage: from geneweaver.client.api.graph import SearchType
"""


class SearchRequest:
    """A class to hold the search request properties.

    This is just a type to give a prospective search
    subroutine user a fighting chance at knowing the
    available properties.
    """

    def __init__(
        self,
        searchType: SearchType = SearchType.EQTL_BP_TO_GENES,
        delimiter: str = ",",
        species: str = "Mus musculus",
        geneIds: Optional[list] = None,
        eqtls: Optional[list] = None,
        rsId: Optional[str] = None,
        tissue: Optional[str] = None,
        studyId: Optional[str] = None,
        source: Optional[Source] = None,
    ) -> None:
        """Initialize a SearchRequest object."""
        # Defaulted properties
        self.searchType: SearchType = searchType
        self.delimiter: str = delimiter
        self.species: str = species

        # Available properties
        self.geneIds: list = geneIds
        self.eqtls: list = eqtls
        self.rsId: str = rsId
        self.tissue: str = tissue
        self.studyId: str = studyId
        self.source: Source = source  # BAYLOR, ENSEMBL, HOMOLOGENE


class Position:
    """A class to hold a position on a chromosome."""

    def __init__(self, bp: str, chr: str) -> None:  # noqa: A002
        """Initialize a Position object."""
        self.bp = bp
        self.chr = chr


class VariantGraphClient:
    """A client to wrap calling the variant graph API."""

    def __init__(self, url: str = "https://graph-api.geneweaver.org/") -> None:
        """Create a VariantGraphClient from a URL.

        :param url: The URL to which we will connect when making graph server queries.
        TODO Authentication?
        """
        self.url = url

    def heartbeat(self) -> dict:
        """Check the server connection.

        Check if we are connected to a server which is in turn connected to a graph
        database.

        :return: a dict with parameters to define if connected and to where.
        """
        response = requests.get(self._get_connected_url())
        if not response.ok:
            response.raise_for_status()
        return json.loads(response.text)

    def get_orthologs(
        self, geneset: list, species: str = "Mus musculus", source: Source = None
    ) -> dict:
        """Get the orthologs for a geneset.

        The species is the species to which we are mapping. So if a geneid in the
        geneset is human it will find the mouse mapped gene. If the geneid is
        already mouse then no mapping will be found.

        :param geneset: list of geneIds
        :param species: String for species to which we map, default of mouse.
                        Must be binomial name, case-sensitive.
        :param source: None, BAYLOR, HOMOLOGENE or ENSEMBL.
                        To get homologs use source = Source.HOMOLOGENE

        :return: all the orthologs found in the geneset which map.
                If there are geneids of the target species, these are not in the dict.
        """
        request = {
            "geneIds": geneset,
            "searchType": "ORTHOLOG",  # Even homologs are 'searchType' ORTHOLOG
            "species": species,
        }  # species to map to

        if source is not None:
            request["source"] = str(source)

        csv_lines = self.search(request)

        reader = csv.reader(csv_lines)
        omap = {
            row[0]: row[1]
            for row in reader
            if len(row) > 0 and not row[0].startswith("gf.geneId")
        }

        return omap

    def search(self, request: SearchRequest) -> list:
        """Perform a search.

        :param request: object with fields defining possible search.
        :return: list of csv values depending on the searchtype.

        Search using a SearchRequest to return as csv. In the returned
        results 'g' is the code for the gene, 'e' the eqtl, 'v' the variant and 'p'Â the peak.

        So for instance a result of:
            g.chr    g.geneName    g.geneId    e.tissueName    e.tissueGroup    e.bp    e.uberon    e.lod    v.start    v.end    v.rsId
            3    Rpsa-ps10    ENSMUSG00000047676    bone    null    101555002    null    6.069993732615    101204207    101204207    rs31201108
            3    Rpsa-ps10    ENSMUSG00000047676    bone    null    101555002    null    6.069993732615    101204207    101204207    rs31201108
            3    Rpsa-ps10    ENSMUSG00000047676    bone    null    101555002    null    6.069993732615    101204207    101204207    rs31201108
            For EQTL the 'e.bp' will in bp38/mm10 and the other coordinates are in bp39/mm11. In general the coordinates of
            the underlying database and the results are bp39/mm11."

            - Examples
            - 1. Given an eQTL in b38 coordinates or rsid, find gene names, gene ids mapped to this eQTL, tissue, UBERON_id, and lod score.
            {eqtls: [{
                 bp : 101555002,
                 chr : 7
            }]}

            You can also provide the rsId if you know it:
            {eqts: [{
                 bp : 101555002,
                 chr : 7,
                }],"
                rsId: rs31201108
            }
            Other fields are available, such as species, see the 'SearchRequest' documentation below
            Even if the EQTL did not link to a variant you can find it:
            {eqtls: [{
                 bp : 9239543,
                 chr : 17
            }]}

            - 2. Given a gene name or gene id, find all eQTL variants associated to this gene.
            {
                 geneIds : [ENSMUSG00000037661],
                 searchType : GENE_ID
            }

            This also works for multiple gene ids in a single query:
            {
                 geneIds : [ENSMUSG00000037661, ENSMUSG00000044117, ENSMUSG00000065968],
                 searchType : GENE_ID
            }

            - 3. Given a peak type and peak location, find all variants in the peak.

        Todo: Fill out more details here
        ----
            - 4. Given an eQTL in b38 coordinates or rsid, find all peaks overlapping this variant.

        Todo: Fill out more details here
        ----

        """
        response = requests.post(self._get_search_url(), None, request)
        if not response.ok:
            response.raise_for_status()

        csv_lines = response.text.split("\n")
        return csv_lines

    def _get_search_url(self) -> str:
        return self.url + "variant/graph/search"

    def _get_connected_url(self) -> str:
        return self.url + "variant/graph/heartbeat"
