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

def test_add_to_index_basic_stats(indexer):
    """Verifies frequency and positions are correctly recorded."""
    indexer.add_to_index("url_1", "hello world hello")
    
    # 'hello' appears at index 0 and 2
    assert indexer.index["hello"]["url_1"]["frequency"] == 2
    assert indexer.index["hello"]["url_1"]["positions"] == [0, 2]
    # 'world' appears once at index 1
    assert indexer.index["world"]["url_1"]["frequency"] == 1
    assert indexer.index["world"]["url_1"]["positions"] == [1]

def test_normalization_and_punctuation(indexer):
    """Tests if case is ignored and punctuation is stripped."""
    # Note: 'Self-aware' should become two words 'self' and 'aware' due to your dash regex
    indexer.add_to_index("url_1", "Self-aware! SELF-AWARE? self aware...")
    
    assert "self" in indexer.index
    assert "aware" in indexer.index
    # 'self' appears 3 times, 'aware' appears 3 times
    assert indexer.index["self"]["url_1"]["frequency"] == 3
    assert indexer.index["aware"]["url_1"]["frequency"] == 3
    # Check that no punctuation remnants exist
    assert "aware!" not in indexer.index
    assert "aware..." not in indexer.index

def test_multiple_pages(indexer):
    """Ensures words across different pages are indexed correctly."""
    indexer.add_to_index("page_a", "apple banana")
    indexer.add_to_index("page_b", "apple cherry")
    
    assert "page_a" in indexer.index["apple"]
    assert "page_b" in indexer.index["apple"]
    assert "page_b" not in indexer.index["banana"]

def test_dash_replacement(indexer):
    """Specifically tests the regex replacement for different types of dashes."""
    # Using hypen, en-dash, and em-dash
    indexer.add_to_index("url_1", "word-word—word–word")
    
    # Should be treated as 4 instances of 'word'
    assert indexer.index["word"]["url_1"]["frequency"] == 4
    assert indexer.index["word"]["url_1"]["positions"] == [0, 1, 2, 3]

def test_save_to_disk(indexer, temp_index_file):
    """Verifies that the index is correctly written to the filesystem."""
    indexer.add_to_index("url_1", "save test")
    indexer.save_to_disk()
    
    assert os.path.exists(temp_index_file)
    
    with open(temp_index_file, 'r') as f:
        data = json.load(f)
        assert "save" in data
        assert data["save"]["url_1"]["frequency"] == 1

def test_empty_string(indexer):
    """Edge case: adding an empty string should not crash or add keys."""
    indexer.add_to_index("url_1", "   ")
    assert len(indexer.index) == 0