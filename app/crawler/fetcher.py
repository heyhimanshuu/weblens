"""
Basic static page fetching.

This is the "HTTP-first" half of the fetch strategy from the architecture
doc. If this isn't enough (JS-heavy page, too little content), Day 31-32
adds a Playwright fallback on top of this - this module doesn't need to
know that fallback exists.
"""

from dataclasses import dataclass

import requests

from app.utils.url_validation import validate_url, InvalidURLError

DEFAULT_TIMEOUT_SECONDS = 10
MAX_CONTENT_BYTES = 5_000_000  # 5MB - a sane ceiling so a huge file can't hang the pipeline later


class FetchError(Exception):
    """Base class for all fetch failures. Callers can catch this without
    needing to know about requests' internal exception hierarchy."""
    pass


@dataclass
class FetchResult:
    url: str
    status_code: int
    content_type: str
    html: str


def fetch_page(url: str, timeout: int = DEFAULT_TIMEOUT_SECONDS) -> FetchResult:
    """
    Fetch a webpage over HTTP(S).

    Raises:
        InvalidURLError: if the URL fails validation.
        FetchError: for any network/HTTP-level failure.
    """
    validated_url = validate_url(url)  # raises InvalidURLError itself

    try:
        response = requests.get(
            validated_url,
            timeout=timeout,
            headers={"User-Agent": "WeblensBot/0.1 (+learning project)"},
        )
    except requests.exceptions.Timeout as e:
        raise FetchError(f"Request timed out after {timeout}s: {url}") from e
    except requests.exceptions.ConnectionError as e:
        raise FetchError(f"Connection failed for {url}: {e}") from e
    except requests.exceptions.RequestException as e:
        # Catch-all for anything else requests can raise (SSL errors, etc.)
        raise FetchError(f"Request failed for {url}: {e}") from e

    if response.status_code != 200:
        raise FetchError(f"Non-200 status ({response.status_code}) for {url}")

    content_type = response.headers.get("Content-Type", "")
    if "text/html" not in content_type:
        raise FetchError(
            f"Expected text/html, got Content-Type '{content_type}' for {url}"
        )

    if len(response.content) > MAX_CONTENT_BYTES:
        raise FetchError(
            f"Page too large ({len(response.content)} bytes) for {url}"
        )

    return FetchResult(
        url=validated_url,
        status_code=response.status_code,
        content_type=content_type,
        html=response.text,
    )
