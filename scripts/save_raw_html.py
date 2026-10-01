"""
Day 4: Fetch a page and save its raw HTML to disk for inspection.

Fill in the TODOs. You already have everything you need from Day 2
(app/crawler/fetcher.py, app/utils/url_validation.py).

Run it like:
    python scripts/save_raw_html.py https://example.com/some-article
"""

import sys
import re
from pathlib import Path

# TODO 1: import fetch_page from your Day 2 fetcher module
# from app.crawler.fetcher import fetch_page


def slugify(url: str) -> str:
    """Turn a URL into a safe-ish filename. Not pretty, just functional."""
    return re.sub(r"[^a-zA-Z0-9]+", "_", url).strip("_")[:100]


def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/save_raw_html.py <url>")
        sys.exit(1)

    url = sys.argv[1]

    # TODO 2: call fetch_page(url) and get the result back
    # result = ...

    # TODO 3: build an output path like data/raw/<slug>.html
    #         (make sure the data/raw/ directory exists - see Path.mkdir)
    # output_dir = Path("data/raw")
    # output_path = ...

    # TODO 4: write result.html to that file (careful with encoding - use utf-8)

    # TODO 5: print out the file path and the length of the HTML in characters,
    #         so you get instant feedback that it worked

    pass


if __name__ == "__main__":
    main()
