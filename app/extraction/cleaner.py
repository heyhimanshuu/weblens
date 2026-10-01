"""
Day 7: Turn raw HTML into a structured, cleaned document.

Wraps trafilatura (proven better on Day 6) behind a stable interface so
the rest of the RAG pipeline never has to know or care which extraction
library we use underneath.
"""

from dataclasses import dataclass

import trafilatura


class ExtractionError(Exception):
    """Raised when we can't extract meaningful content from a page at all."""
    pass


@dataclass
class CleanedDocument:
    url: str
    title: str | None
    text: str  # markdown-ish: headings preserved as '#'/'##' where detected


def clean_html(html: str, url: str) -> CleanedDocument:
    """
    Extract a CleanedDocument from raw HTML.

    Raises ExtractionError if trafilatura can't find any main content
    (e.g. an empty page, or a page that's entirely navigation/boilerplate).
    """
    # Metadata extraction is a SEPARATE call from content extraction in
    # trafilatura - it parses <title>, <meta> tags, etc. independently of
    # finding the "main content" block. That's why this can succeed even
    # when the content extraction below fails.
    metadata = trafilatura.extract_metadata(html)
    title = metadata.title if metadata else None

    # output_format="markdown" is the key choice here: it preserves
    # heading levels as '#'/'##' instead of flattening everything into
    # one undifferentiated paragraph of text. That structure is what
    # Day 8's heading-aware chunking option depends on existing at all.
    text = trafilatura.extract(html, output_format="markdown")

    # trafilatura returns None (not an empty string) when it can't find
    # confident main content. We fail LOUDLY here with a custom exception
    # rather than quietly returning an empty CleanedDocument - an empty
    # document would otherwise flow silently into chunking/embeddings as
    # garbage, and the real failure would be invisible until way later.
    if not text:
        raise ExtractionError(f"No extractable content found for {url}")

    return CleanedDocument(url=url, title=title, text=text)
