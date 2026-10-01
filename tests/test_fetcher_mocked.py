"""
Day 5: Testing fetch_page()'s edge cases WITHOUT hitting the real internet.

We use unittest.mock.patch to replace requests.get with a fake version
that returns whatever response object we construct - so we can simulate
a timeout, a bad content-type, etc. instantly and reliably.
"""

from unittest.mock import patch, Mock
import pytest
import requests

from app.crawler.fetcher import fetch_page, FetchError


def test_timeout_raises_fetch_error():
    """Simulate requests.get() timing out, without actually waiting."""
    # TODO 1: patch where requests.get is USED (the fetcher module)
    with patch("app.crawler.fetcher.requests.get") as mock_get:
        # Calling the mock now raises Timeout, like a real timeout would
        mock_get.side_effect = requests.exceptions.Timeout()

        # TODO 2: fetch_page should catch Timeout and re-raise FetchError
        with pytest.raises(FetchError):
            fetch_page("https://example.com")


def test_non_html_content_type_raises_fetch_error():
    """A 200 response that is a PDF, not HTML, must be rejected."""
    # TODO 3: fake response with the attributes fetch_page() reads
    fake_response = Mock()
    fake_response.status_code = 200
    fake_response.headers = {"Content-Type": "application/pdf"}
    fake_response.content = b"%PDF-1.4 fake pdf bytes"
    fake_response.text = ""

    # TODO 4: make requests.get return the fake, then expect FetchError
    with patch("app.crawler.fetcher.requests.get") as mock_get:
        mock_get.return_value = fake_response
        with pytest.raises(FetchError):
            fetch_page("https://example.com")


def test_successful_fetch_does_not_touch_real_network():
    """A fake successful HTML response comes back exactly as given."""
    # TODO 5: fake successful response with made-up content
    fake_html = "<html><body>made-up content xyz-12345</body></html>"

    fake_response = Mock()
    fake_response.status_code = 200
    fake_response.headers = {"Content-Type": "text/html; charset=utf-8"}
    # .content must be real bytes because fetch_page calls len() on it
    fake_response.content = fake_html.encode("utf-8")
    fake_response.text = fake_html

    with patch("app.crawler.fetcher.requests.get") as mock_get:
        mock_get.return_value = fake_response

        result = fetch_page("https://example.com/fake-page")

    assert result.html == fake_html
    assert result.status_code == 200
    assert "text/html" in result.content_type
    # Proves the fake was used: requests.get was called exactly once
    mock_get.assert_called_once()
