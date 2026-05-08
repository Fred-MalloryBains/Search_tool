# Search Engine Tool (COMP3011 Coursework 2) 🔎

## Project Overview 🕷️
This Search Engine Tool is a Python-based application developed for the **Web Services and Web Data (COMP3011)** module at the University of Leeds. The tool provides a complete pipeline for web search, including a crawler to navigate a target website, an indexer to process content into an efficient inverted index, and a search interface for querying terms.

The tool is specifically designed to work with [https://quotes.toscrape.com/](https://quotes.toscrape.com/), a website purpose-built for learning web scraping.

### Key Features 
*   **Polite Web Crawling**: Navigates the target site while respecting a minimum 6-second politeness window between requests.
*   **Inverted Indexing**: Generates a structured index that stores word statistics, including frequency and position, to facilitate fast retrieval.
*   **Case-Insensitive Search**: Normalizes text so that queries are matched regardless of casing (e.g., 'Good' matches 'good').
*   **Multi-Word Query Support**: Supports finding pages that contain multiple search terms.

---

## Installation & Setup 🧪

### Prerequisites
*   **Python 3.x**
*   **pip** (Python package installer)

### Dependencies
The project relies on the following libraries as recommended in **COMP3011_Coursework2_Brief__2025_2026.pdf**:
*   `requests`: For composing HTTP requests to the target website.
*   `beautifulsoup4`: For parsing HTML content and extracting text/links.
*   `pytest`: For running the test suite.

### Installation Steps
1.  **Clone the repository**:
    ```bash
    git clone [https://github.com/Fred-MalloryBains/Search_tool]
    cd fred-mallorybains/search_tool
    ```
2.  **Install requirements**:
    ```bash
    pip install -r requirements.txt
    ```

---

## Usage 👷‍♀️
The tool is operated via a Command-Line Interface (CLI) through `src/main.py`.

### 1. Build the Index
Crawls the website, processes the data, and saves the index to `data/index.json`.
```bash
> build
```

### 2. Load the Index 
Loads an existing index from the file system into memory for searching
```bash
> load
```

### 3. Print Word statistics
Displays the inverted index entry for a specific word
```bash
> print [word]
```

### 4. Find Pages
Returns a list of all pages containing the specified query phrase or terms
```bash
> find [query]
```

# Project Structure 🏗️

```plaintext
search_tool/
├── src/                # Source code
│   ├── crawler.py      # Web crawling logic
│   ├── indexer.py      # Inverted index creation
│   ├── search.py       # Query processing and retrieval
│   └── main.py         # CLI entry point
├── tests/              # Test suite
│   ├── fixtures/       # Mock data for testing
│   ├── test_crawler.py
│   ├── test_indexer.py
│   └── test_search.py
├── data/               # Persistent storage
│   └── index.json      # Compiled index file
├── requirements.txt    # Project dependencies
└── README.md           # Documentation
```

## Index structure

Can be found here: [Index](docs/INDEX_INFO.md)
