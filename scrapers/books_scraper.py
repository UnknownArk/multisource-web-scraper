from datetime import datetime, timezone
from urllib.parse import urljoin

from scrapers.base_scraper import BaseScraper
from config import BOOKS_START_URL

class BooksScraper(BaseScraper):
    source_name = "Books to Scrape"
    start_url = BOOKS_START_URL
    record_selector = "article.product_pod"

    def parse_record(self, article, page_url: str) -> dict:
        link_tag = article.select_one("h3 > a")
        price_tag = article.select_one("p.price_color")
        rating_tag = article.select_one("p.star-rating")

        title = link_tag.get("title") if link_tag else None
        href = urljoin(page_url, link_tag["href"]) if link_tag and link_tag.get("href") else None
        
        price_raw = price_tag.get_text(strip=True) if price_tag else None
        rating_raw = " ".join(rating_tag.get("class", [])) if rating_tag else None

        return {
            "source": self.source_name,
            "source_url": href,
            "name_or_title": title,
            "category": None,      # Opted out of fetching detail pages to save time
            "price_raw": price_raw,
            "rating_raw": rating_raw,
            "author": None,
            "tags": None,
            "description": None,   # Opted out of fetching detail pages to save time
            "scraped_at": datetime.now(timezone.utc).isoformat(),
        }

    def get_next_url(self, soup, current_url: str) -> str | None:
        next_btn = soup.select_one("li.next > a")
        if not next_btn:
            return None
        return urljoin(current_url, next_btn["href"])
