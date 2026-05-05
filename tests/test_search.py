import pytest
import os
import json
from src.indexer import Indexer

@pytest.fixture
def temp_index_file(tmp_path):
    """Creates a temporary file path for the index."""
    d = tmp_path / "data"
    d.mkdir()
    return str(d / "test_index.json")

@pytest.fixture
def indexer(temp_index_file):
    """Provides a fresh Indexer instance for each test."""
    return Indexer(filename=temp_index_file)

