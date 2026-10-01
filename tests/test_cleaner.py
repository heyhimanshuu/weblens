"""
Day 7: Test the cleaner against a small, HANDWRITTEN HTML fixture -
not a live page. We want to know exactly what should and shouldn't
survive, so we control the input completely (same principle as Day 5's
mocking: deterministic tests over flaky real-world ones).
"""

import pytest
from app.extraction.cleaner import clean_html, ExtractionError

SAMPLE_HTML = """
<html>
<head><title>The Real Page Title</title></head>
<body>
    <nav>
        <a href="/">Home</a> | <a href="/about">About</a> | <a href="/contact">Contact</a>
    </nav>
    <div class="cookie-banner">We use cookies. Accept all cookies now.</div>
    <article>
        <h1>Main Heading</h1>
        <p>This is the actual real content of the article that we care about.
        It has enough text that trafilatura should recognize it as the main
        content block rather than boilerplate.</p>
        <h2>A Subheading</h2>
        <p>More real content under the subheading, also long enough to be
        taken seriously as article text rather than noise.</p>
    </article>
    <footer>
        <p>Copyright 2026. All rights reserved. Privacy Policy | Terms of Service</p>
    </footer>
</body>
</html>
"""

# A page with genuinely NO extractable text anywhere - this is the real
# "nothing here" case. (A nav bar that merely CONTAINS text, like
# "Home | About", is not this case - trafilatura will happily return
# that text back if it's literally the only thing on the page, since it
# has nothing else to compare it against. Verified this empirically
# rather than assuming it.)
EMPTY_HTML = "<html><body><nav></nav></body></html>"


def test_extracts_title():
    # Verified empirically: when both a <title> tag and an <h1> exist,
    # trafilatura's metadata heuristic prefers the <h1> text. This makes
    # sense in general - <title> tags often carry SEO suffixes like
    # " - SiteName" while <h1> is usually the clean, human-facing title -
    # but it's a real behavior worth knowing, not the naive assumption
    # that <title> always wins.
    result = clean_html(SAMPLE_HTML, "https://example.com/article")
    assert result.title == "Main Heading"


def test_extracts_main_content():
    result = clean_html(SAMPLE_HTML, "https://example.com/article")
    assert "actual real content" in result.text


def test_strips_navigation():
    # This is the real test of whether cleaning did anything at all -
    # a naive BeautifulSoup .get_text() approach would FAIL this test,
    # which is exactly the Day 6 comparison made concrete as an assertion.
    result = clean_html(SAMPLE_HTML, "https://example.com/article")
    assert "Home" not in result.text
    assert "About" not in result.text


def test_strips_cookie_banner():
    result = clean_html(SAMPLE_HTML, "https://example.com/article")
    assert "cookies" not in result.text.lower()


def test_preserves_heading_structure():
    # We care that BOTH headings survived - not just that SOME content
    # came through. This is what tomorrow's heading-aware chunking relies on.
    result = clean_html(SAMPLE_HTML, "https://example.com/article")
    assert "Main Heading" in result.text
    assert "A Subheading" in result.text


def test_raises_on_no_extractable_content():
    with pytest.raises(ExtractionError):
        clean_html(EMPTY_HTML, "https://example.com")
