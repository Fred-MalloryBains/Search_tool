import pytest
import os
import json
from src.indexer import Indexer
from src.search import Index

"""
Creates a temporary file path for the index.
"""
@pytest.fixture
def temp_index_file(tmp_path):
    d = tmp_path / "data"
    d.mkdir()
    return str(d / "test_index.json")

"""
Provides a fresh Indexer instance for each test.
"""
@pytest.fixture
def index(temp_index_file):
    # Create and seed the data
    writer = Indexer(filename=temp_index_file)
    writer.add_to_index("url_1", "good friends")
    writer.add_to_index("url_2", "good food")
    writer.add_to_index("url_3", "friends only")
    writer.save_to_disk()
    
    # Now create the Search object and load that same file
    search_tool = Index(filename=temp_index_file)
    search_tool.load_from_disk()
    return search_tool


# Tests for FIND (get_search_results)

"""
Verifies that a single word returns all correct pages.
"""
def test_find_single_word(index):
    results = index.get_search_results("good")
    assert results == {"url_1", "url_2"}
    assert "url_3" not in results
"""
Verifies the AND logic: only pages containing ALL words are returned.
"""
def test_find_multi_word_intersection(index):
    
    results = index.get_search_results("good friends")
    # Only url_1 has both words
    assert results == {"url_1"}
    assert len(results) == 1

"""
Verifies search works regardless of query casing.
"""
def test_find_case_insensitivity(index):
    results = index.get_search_results("GoOD FRIenDS")
    assert results == {"url_1"}

"""
Verifies that a non-existent word returns an empty set.
"""
def test_find_no_results(index):
    results = index.get_search_results("nonsense")
    assert results == set()

"""
Verifies that if one word in a phrase is missing, result is empty.
"""

def test_find_partial_missing_word(index):
    results = index.get_search_results("good missingword")
    assert results == set()

"""
Edge case: empty string query.
"""
def test_find_empty_query(index):
    
    assert index.get_search_results("") == set()
    assert index.get_search_results("   ") == set()


# Tests for PRINT (print_index) 

def test_print_index_output(index, capsys):
    """Verifies the printed output format for a known word."""
    index.print_index("good")
    captured = capsys.readouterr()
    
    # Check for keywords in your print logic
    assert "Word: 'good'" in captured.out
    assert "Page: url_1" in captured.out
    assert "Frequency: 1" in captured.out
    assert "Page: url_2" in captured.out

"""
Verifies the error message when printing a word not in index.
"""
def test_print_index_missing_word(index, capsys):
    index.print_index("unknown")
    captured = capsys.readouterr()
    assert "Word 'unknown' not found in index" in captured.out


# Tests for Load/Persistence Integration
"""
Tests the error handling when loading a file that doesn't exist.
"""
def test_load_non_existent_file(capsys):
    
    idx = Index(filename="non_existent.json")
    idx.load_from_disk()
    captured = capsys.readouterr()
    assert "Error: Index file" in captured.out
    assert "not found" in captured.out


