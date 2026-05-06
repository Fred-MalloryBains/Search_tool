import pytest
from bs4 import BeautifulSoup
from src.crawler import Crawler


"""
Returns: crawler instance for testing
"""
@pytest.fixture
def crawler():
    return Crawler("http://quotes.toscrape.com/")

"""
Returns:
    _type_: sample HTML content for testing
"""
@pytest.fixture
def sample_html():
    with open("tests/fixtures/sample_page.html", "r") as f:
        return f.read()

"""
Returns:
    _type_: BeautifulSoup instance for testing
"""
@pytest.fixture
def soup(sample_html):
    return BeautifulSoup(sample_html, "html.parser")

"""
Verify that the scraper can fetch and parse a page successfully.
"""
def test_extract_content_basic(crawler, soup):
    content, next_page, _ = crawler.extract_content(soup)

    assert isinstance(content, list)
    assert len(content) > 0

    first = content[0]
    assert "text" in first
    assert "author" in first
    assert "tags" in first


"""
tests that the scraper correctly identifies when there are no more pages to crawl.
"""
def test_extract_content_normalisation(crawler, soup):
    content, _, _ = crawler.extract_content(soup)

    first = content[0]

    assert first["text"] == first["text"].lower()
    assert first["author"] == first["author"].lower()
    assert all(tag == tag.lower() for tag in first["tags"])


"""
Verify that the scraper correctly identifies and returns the next page URL.
"""
def test_next_page_exists(crawler, soup):
    _, next_pages, _ = crawler.extract_content(soup)

    assert isinstance(next_pages, list)
    assert next_pages is not None
    assert any("page/2" in url for url in next_pages)


"""
Verify that the scraper correctly identifies when there are no more pages to crawl.
"""
def test_empty_page(crawler):
    empty_soup = BeautifulSoup("<html></html>", "html.parser")

    content, next_pages, _ = crawler.extract_content(empty_soup)

    assert content == []
    assert next_pages == []

"""
Verify that the scraper can handle missing fields gracefully without crashing.
"""
def test_missing_fields(crawler):
    html = """
    <div class="quote">
        <span class="text">Test quote</span>
    </div>
    """
    soup = BeautifulSoup(html, "html.parser")

    # Should not crash
    content, _, _ = crawler.extract_content(soup)

    assert isinstance(content, list)

"""
Verify that the scraper can handle malformed HTML without crashing.
"""
def test_scrape_quotes_success(mocker, crawler):
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.text = "<html></html>"

    mocker.patch("requests.get", return_value=mock_response)

    soup = crawler.scrape_quotes(crawler.base_url)

    assert soup is not None


"""
Verify that the scraper can handle network errors gracefully without crashing.
"""
def test_scrape_quotes_failure(mocker, crawler):
    mock_response = mocker.Mock()
    mock_response.status_code = 404

    mocker.patch("requests.get", return_value=mock_response)

    soup = crawler.scrape_quotes(crawler.base_url)

    assert soup is None


"""
Integration test to verify that the build process correctly scrapes
and indexes content without errors.
Makes use of the mocker fixture to avoid real HTTP requests and file writes.
"""

def test_build_creates_index(tmp_path, mocker):
    # Mock indexer to avoid writing real files
    from src.crawler import Crawler

    crawler = Crawler("http://quotes.toscrape.com/")
    
    crawler.indexer.save_to_disk = mocker.Mock()

    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.text = """
    <div class="quote">
        <span class="text">Test quote</span>
        <small class="author">Author</small>
        <a class="tag">tag1</a>
    </div>
    """

    mocker.patch("requests.get", return_value=mock_response)

    crawler.build()

    crawler.indexer.save_to_disk.assert_called_once()
