import pytest
from bs4 import BeautifulSoup
from src.crawler import Crawler

@pytest.fixture
def crawler():
    return Crawler("http://quotes.toscrape.com/")


@pytest.fixture
def sample_html():
    with open("tests/fixtures/sample_page.html", "r") as f:
        return f.read()


@pytest.fixture
def soup(sample_html):
    return BeautifulSoup(sample_html, "html.parser")


def test_extract_content_basic(crawler, soup):
    content, next_page = crawler.extract_content(soup)

    assert isinstance(content, list)
    assert len(content) > 0

    first = content[0]
    assert "text" in first
    assert "author" in first
    assert "tags" in first


def test_extract_content_normalisation(crawler, soup):
    content, _ = crawler.extract_content(soup)

    first = content[0]

    assert first["text"] == first["text"].lower()
    assert first["author"] == first["author"].lower()
    assert all(tag == tag.lower() for tag in first["tags"])


def test_next_page_exists(crawler, soup):
    _, next_page = crawler.extract_content(soup)

    assert next_page is not None
    assert "page/2" in next_page


def test_empty_page(crawler):
    empty_soup = BeautifulSoup("<html></html>", "html.parser")

    content, next_page = crawler.extract_content(empty_soup)

    assert content == []
    assert next_page is None


def test_missing_fields(crawler):
    html = """
    <div class="quote">
        <span class="text">Test quote</span>
    </div>
    """
    soup = BeautifulSoup(html, "html.parser")

    # Should not crash
    content, _ = crawler.extract_content(soup)

    assert isinstance(content, list)


def test_scrape_quotes_success(mocker, crawler):
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.text = "<html></html>"

    mocker.patch("requests.get", return_value=mock_response)

    soup = crawler.scrape_quotes(crawler.base_url)

    assert soup is not None


def test_scrape_quotes_failure(mocker, crawler):
    mock_response = mocker.Mock()
    mock_response.status_code = 404

    mocker.patch("requests.get", return_value=mock_response)

    soup = crawler.scrape_quotes(crawler.base_url)

    assert soup is None


## integration test

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
    

def test_scrape_quotes_url_construction(mocker, crawler):
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.text = "<html></html>"

    mock_get = mocker.patch("requests.get", return_value=mock_response)

    crawler.scrape_quotes(crawler.base_url, page=3)

    assert "page/3" in mock_get.call_args[0][0]
    
