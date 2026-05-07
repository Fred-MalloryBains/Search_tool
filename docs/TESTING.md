# Testing 

Testing was split across 3 distinct files using pytest to implement this. 

The code coverage of the tests was over 95% for each feature file: 

```bash 
Name             Stmts   Miss  Cover
------------------------------------
src/crawler.py     103      4    97%
src/indexer.py      36      2    95%
src/search.py       86      1    99%
------------------------------------
TOTAL              297     7    96%
```
Using pytest's coverage module

## tests/crawler

This code tests the crawler function, using mocking and etc 

## tests/indexer 

This code tests the tokenisation and storage of the index 

## tests/search

This code tests the searching etc