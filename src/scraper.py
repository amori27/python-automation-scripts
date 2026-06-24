"""Web Scraper Module.

This module provides web scraping capabilities using
requests and BeautifulSoup.
"""

import requests
from bs4 import BeautifulSoup
from typing import Any


class WebScraper:
    """Handles web scraping operations."""

    def __init__(self, headers: dict[str, str] | None = None):
        """Initialize the WebScraper.

        Args:
            headers: Optional HTTP headers.
        """
        self.headers = headers or {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        self.session = requests.Session()

    def fetch_page(self, url: str) -> str | None:
        """Fetch HTML content of a page.

        Args:
            url: URL to fetch.

        Returns:
            HTML content or None on error.
        """
        try:
            response = self.session.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            return response.text
        except requests.RequestException:
            return None

    def scrape_page(
        self,
        url: str,
        selectors: dict[str, str] | None = None
    ) -> dict[str, Any]:
        """Scrape a page with specified selectors.

        Args:
            url: URL to scrape.
            selectors: Dict of CSS selectors.

        Returns:
            Scraped data.
        """
        html = self.fetch_page(url)
        if not html:
            return {"error": "Failed to fetch page"}

        soup = BeautifulSoup(html, 'html.parser')
        result = {"url": url}

        if selectors:
            for key, selector in selectors.items():
                elements = soup.select(selector)
                result[key] = [el.text.strip() for el in elements]
        else:
            result["title"] = soup.title.string if soup.title else None
            result["text"] = soup.get_text(separator="\n", strip=True)

        return result

    def scrape_links(self, url: str) -> list[str]:
        """Extract all links from a page.

        Args:
            url: URL to scrape.

        Returns:
            List of URLs.
        """
        html = self.fetch_page(url)
        if not html:
            return []

        soup = BeautifulSoup(html, 'html.parser')
        links = []

        for a_tag in soup.find_all('a', href=True):
            href = a_tag['href']
            if href.startswith('http'):
                links.append(href)

        return links

    def scrape_table(
        self,
        url: str,
        table_selector: str = "table"
    ) -> list[dict[str, str]]:
        """Scrape table data from a page.

        Args:
            url: URL to scrape.
            table_selector: CSS selector for table.

        Returns:
            List of row dictionaries.
        """
        html = self.fetch_page(url)
        if not html:
            return []

        soup = BeautifulSoup(html, 'html.parser')
        table = soup.select_one(table_selector)

        if not table:
            return []

        rows = []
        headers = [th.text.strip() for th in table.select('th')]

        for tr in table.select('tr'):
            cells = [td.text.strip() for td in tr.select('td')]
            if cells:
                if headers:
                    rows.append(dict(zip(headers, cells)))
                else:
                    rows.append({"col_" + str(i): v for i, v in enumerate(cells)})

        return rows

    def close(self) -> None:
        """Close the session."""
        self.session.close()


def scrape_multiple_pages(urls: list[str], selectors: dict[str, str]) -> list[dict[str, Any]]:
    """Scrape multiple pages.

    Args:
        urls: List of URLs.
        selectors: CSS selectors.

    Returns:
        List of scraped data.
    """
    scraper = WebScraper()
    results = []

    for url in urls:
        result = scraper.scrape_page(url, selectors)
        results.append(result)

    scraper.close()
    return results
