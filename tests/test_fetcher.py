import pytest
from app.crawler.fetcher import fetch_page, FetchError
from app.utils.url_validation import InvalidURLError


def test_fetch_real_page():
    """This test hits the real internet on purpose - it's a sanity check
    that the whole path (validate -> request -> parse response) works
    end-to-end against a real, stable page."""
    result = fetch_page("https://example.com")
    assert result.status_code == 200
    assert "text/html" in result.content_type
    assert "<html" in result.html.lower()


def test_fetch_invalid_url_raises():
    with pytest.raises(InvalidURLError):
        fetch_page("not-a-url")


def test_fetch_nonexistent_domain_raises():
    with pytest.raises(FetchError):
        fetch_page("https://this-domain-should-not-exist-weblens-test.com")


def test_fetch_404_raises():
    with pytest.raises(FetchError):
        fetch_page("https://httpbin.org/status/404")
