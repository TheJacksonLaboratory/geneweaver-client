from unittest.mock import patch

import pytest
from typer.testing import CliRunner
from geneweaver.client.gedb import *
from typing import List
from typing import Set

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

    