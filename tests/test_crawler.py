from unittest.mock import patch, Mock
from src.crawler import crawl
import requests


def test_crawler_extracts_page_text():
    html = """
    <html>
        <body>
            <div class="quote">
                <span class="text">Test quote here</span>
            </div>
        </body>
    </html>
    """

    mock_response = Mock()
    mock_response.text = html
    mock_response.raise_for_status.return_value = None

    with patch("src.crawler.requests.get", return_value=mock_response):
        with patch("src.crawler.time.sleep", return_value=None):
            pages = crawl()

    assert len(pages) == 1
    assert "https://quotes.toscrape.com" in pages
    assert "Test quote here" in pages["https://quotes.toscrape.com"]


def test_crawler_follows_next_page_link():
    first_page_html = """
    <html>
        <body>
            <p>First page</p>
            <li class="next"><a href="/page/2/">Next</a></li>
        </body>
    </html>
    """

    second_page_html = """
    <html>
        <body>
            <p>Second page</p>
        </body>
    </html>
    """

    first_response = Mock()
    first_response.text = first_page_html
    first_response.raise_for_status.return_value = None

    second_response = Mock()
    second_response.text = second_page_html
    second_response.raise_for_status.return_value = None

    with patch("src.crawler.requests.get", side_effect=[first_response, second_response]):
        with patch("src.crawler.time.sleep", return_value=None):
            pages = crawl()

    assert len(pages) == 2
    assert "https://quotes.toscrape.com" in pages
    assert "https://quotes.toscrape.com/page/2/" in pages

def test_crawler_handles_request_exception(capsys):
    with patch("src.crawler.requests.get", side_effect=requests.exceptions.RequestException("Network error")):
        pages = crawl()

    captured = capsys.readouterr()

    assert pages == {}
    assert "Error fetching" in captured.out
    assert "Network error" in captured.out