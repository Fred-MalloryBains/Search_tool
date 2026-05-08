# Testing 

Testing is implemented using `pytest` and `pytest-mock`, achieving 96% total code coverage across the core search pipeline.

## Testsuite Overview

The suite is modularized into three distinct functional areas to ensure localized error detection:

| Test File | Focus Area | Key Edge Cases Covered | 
| --------- | ---------- | ---------------------- |  
| test_crawler.py | HTML parsing & Link discovery | "Malformed HTML, 404 errors, and duplicate URL skipping   " | 
| test_indexer.py | Text normalization & Storage | "Punctuation stripping, dash-handling, and empty string inputs   +1" |
| test_search.py | Retrieval & Ranking | "Multi-word intersections, phrase bonuses, and case-insensitivity"|


## Code coverage 

```bash 
Name             Stmts   Miss  Cover
------------------------------------
src/crawler.py     103      4    97%
src/indexer.py      36      2    95%
src/search.py       86      1    99%
------------------------------------
TOTAL              297     7    96%
```
Generated using `pytest-cov`

## tests/crawler

This code tests the crawler function, using mocking and etc 

## tests/indexer 

This code tests the tokenisation and storage of the index 

## tests/search

This code tests the searching etc