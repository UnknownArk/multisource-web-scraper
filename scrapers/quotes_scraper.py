from datetime import datetime, timezone
from urllib.parse import urljoin

from scrapers.base_scraper import BaseScraper
from config import QUOTES_START_URL

class QuotesScraper(BaseScraper):
    source_name = "Quotes to Scrape"
    start_url = QUOTES_START_URL
    record_selector = "div.quote"

    def parse_record(self, div, page_url: str) -> dict:
        text_tag = div.select_one("span.text")
        author_tag = div.select_one("small.author")
        tag_links = div.select("a.tag")

        text = text_tag.get_text(strip=True) if text_tag else None
        author = author_tag.get_text(strip=True) if author_tag else None

        tags = None
        if tag_links:
            # Sort alphabetically for consistency
            tags = ";".join(sorted(t.get_text(strip=True) for t in tag_links))

        return {
            "source": self.source_name,
            "source_url": page_url,
            "name_or_title": text,
            "category": None,
            "price_raw": None,
            "rating_raw": None,
            "author": author,
            "tags": tags,
            "description": None,
            "scraped_at": datetime.now(timezone.utc).isoformat(),
        }

    def get_next_url(self, soup, current_url: str) -> str | None:
        next_btn = soup.select_one("li.next > a")
        if not next_btn:
            return None
        return urljoin(current_url, next_btn["href"])
