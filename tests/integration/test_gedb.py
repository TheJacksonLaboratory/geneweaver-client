from unittest.mock import patch

import pytest
import os

from typer.testing import CliRunner
from geneweaver.client.gedb import *
from typing import List
from typing import Set
from pathlib import Path
from collections import OrderedDict

runner = CliRunner()


def test_init_client_no_args():
    client = GeneExpressionDatabaseClient()
    assert client is not None, "Unexpectedly cannot make a client with no args"
    
    
def test_init_client_on_dev():
    client = GeneExpressionDatabaseClient("https://geneweaver-dev.jax.org/gedb")
    assert client is not None, "Unexpectedly cannot make a client with dev uri"
    
def test_get_tissues():
    client = GeneExpressionDatabaseClient("https://geneweaver-dev.jax.org/gedb")
    tissues:  [str] = client.distinct("tissue")
    assert "heart" in tissues, "Tissue set must contain heart"
    assert "striatum" in tissues, "Tissue set must contain striatum"
    
def test_search_expressions():
    
    gedbc = GeneExpressionDatabaseClient("https://geneweaver-dev.jax.org/gedb")
    genes = get_genes("tests/integration/connective_tissue_disorder_log2fc_mouse.csv")
    all_strains = gedbc.distinct("strain")
    
    drequest = DataRequest(geneIds     = genes, 
                           strains     = all_strains, 
                           sourceType  = SourceType.IMPUTED)
    
    imputations: List[DataResult] = gedbc.search(drequest)    

    print(imputations)
    # TODO Test result


def get_genes(path: str) -> OrderedDict:
    
    # We keep the keys in order here as
    # it is easier to use the debugger and
    # check the dict
    gene_values = OrderedDict()
    with open(path,'r') as file:
 
        # reading each line from original text file
        for line in file.readlines():
            
            line = line.strip()
            if not (line.startswith('#')):
                sa = line.split(',')
                #     {"gene_id": sa[0],
                #      "log2fc" : sa[1],
                #      "species": sa[2]}
                gene_values[sa[0]] = sa[1]
                
    return gene_values
