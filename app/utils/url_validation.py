"""
URL validation utilities.

Why this exists as its own module:
We never want to hand a raw, unchecked user string to an HTTP client.
This is step one of treating user input (and eventually webpage content)
as untrusted - a theme that will come back hard on the security day (Day 34+).
"""

from urllib.parse import urlparse


class InvalidURLError(ValueError):
    """Raised when a URL fails validation. A custom exception type
    makes it easy for callers to catch *this specific* failure mode
    rather than a generic ValueError that could mean anything."""
    pass


ALLOWED_SCHEMES = {"http", "https"}


def validate_url(url: str) -> str:
    """
    Validate that `url` is a well-formed http(s) URL.

    Returns the (possibly normalized) URL string if valid.
    Raises InvalidURLError if not.

    This does NOT yet check for SSRF risks like localhost/private IPs -
    that's a deliberate later step (Day 34), once we understand the
    full threat model. Today is just "is this structurally a real URL".
    """
    if not url or not isinstance(url, str):
        raise InvalidURLError("URL must be a non-empty string.")

    url = url.strip()

    try:
        parsed = urlparse(url)
    except ValueError as e:
        # urlparse rarely raises, but malformed input (e.g. bad IPv6) can
        raise InvalidURLError(f"Could not parse URL: {e}") from e

    if parsed.scheme not in ALLOWED_SCHEMES:
        raise InvalidURLError(
            f"URL scheme must be one of {ALLOWED_SCHEMES}, got: '{parsed.scheme}'"
        )

    if not parsed.netloc:
        raise InvalidURLError("URL is missing a hostname.")

    return url
