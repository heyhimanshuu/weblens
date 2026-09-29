import pytest
from app.utils.url_validation import validate_url, InvalidURLError


def test_valid_https_url():
    assert validate_url("https://example.com/article") == "https://example.com/article"


def test_valid_http_url():
    assert validate_url("http://example.com") == "http://example.com"


def test_rejects_empty_string():
    with pytest.raises(InvalidURLError):
        validate_url("")


def test_rejects_non_http_scheme():
    with pytest.raises(InvalidURLError):
        validate_url("ftp://example.com/file.txt")


def test_rejects_file_scheme():
    with pytest.raises(InvalidURLError):
        validate_url("file:///etc/passwd")


def test_rejects_missing_hostname():
    with pytest.raises(InvalidURLError):
        validate_url("https://")


def test_rejects_garbage_string():
    with pytest.raises(InvalidURLError):
        validate_url("not a url at all")


def test_strips_whitespace():
    assert validate_url("  https://example.com  ") == "https://example.com"
