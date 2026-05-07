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

@pytest.fixture
def search_with_metadata(tmp_path):
    path = str(tmp_path / "meta_index.json")
    data = {
        "index": {
            "apple": {
                "url_1": {"frequency": 1, "positions": [0]},
                "url_2": {"frequency": 5, "positions": [0, 10, 20, 30, 40]}
            }
        },
        "metadata": {
            "url_1": {"tags": ["apple", "fruit"]},
            "url_2": {"tags": ["tech"]}
        }
    }
    with open(path, 'w') as f:
        json.dump(data, f)
    
    s = Index(filename=path)
    s.load_from_disk()
    return s

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


def test_metadata_boost(search_with_metadata):
    # url_1 has frequency 1 but has "apple" in tags (1.5x boost)
    # url_2 has frequency 5 but no tag boost.
    search_with_metadata.total_docs = 10  # Set total_docs for IDF calculation
    results = search_with_metadata.get_search_results("apple")
    ranked = search_with_metadata.calculate_relevance(results, "apple")
    # This ensures the ranking logic is actually executed
    assert len(ranked) == 2
    assert ranked[0][1] > 0
    
def test_phrase_bonus_logic(index):
    # Setup index specifically for phrase testing
    index.index["hot"] = {"url_x": {"frequency": 1, "positions": [10]}}
    index.index["dog"] = {"url_x": {"frequency": 1, "positions": [11]}} # Adjacent
    index.total_docs = 10
    
    results = {"url_x"}
    ranked = index.calculate_relevance(results, "hot dog")
    
    # The score should be high because (10 + 1) == 11
    assert ranked[0][0] == "url_x"
    assert ranked[0][1] > 5.0 # Base bonus is 5.0
    
def test_display_results_integration(index, capsys):
    results = {"url_1", "url_2"}
    index.display_results(results, "good")
    captured = capsys.readouterr()
    
    assert "Results found in 2 pages" in captured.out
    assert "Score:" in captured.out
    
def test_display_no_results(index, capsys):
    index.display_results(set(), "nothing")
    captured = capsys.readouterr()
    assert "No results found." in captured.out