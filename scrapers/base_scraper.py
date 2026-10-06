import time
import logging
from abc import ABC, abstractmethod

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from bs4 import BeautifulSoup

from config import (
    REQUEST_DELAY, REQUEST_TIMEOUT, 
    MAX_RETRIES, BACKOFF_FACTOR, RETRY_STATUS_CODES
)

class BaseScraper(ABC):
    """
    Abstract base class for scrapers. Handles HTTP sessions,
    retries, and the pagination loop.
    """
    source_name: str = ""
    start_url: str = ""
    record_selector: str = ""

    def __init__(self):
        self.session = self._build_session()
        self.logger = logging.getLogger(self.__class__.__name__)

    def _build_session(self) -> requests.Session:
        session = requests.Session()
        session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        })

        retry_strategy = Retry(
            total=MAX_RETRIES,
            backoff_factor=BACKOFF_FACTOR,
            status_forcelist=RETRY_STATUS_CODES,
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        
        return session

    def fetch(self, url: str):
        try:
            time.sleep(REQUEST_DELAY)
            response = self.session.get(url, timeout=REQUEST_TIMEOUT)
            response.raise_for_status()
            response.encoding = "utf-8"
            return BeautifulSoup(response.text, "lxml")
        except requests.RequestException as e:
            self.logger.error("Failed to fetch %s: %s", url, e)
            return None

    def scrape_all(self, max_pages: int | None =None) -> list:
        records = []
        url = self.start_url
        page_num = 1

        while url:
            if max_pages and page_num > max_pages:
                self.logger.info("Reached max_pages limit (%d). Stopping.", max_pages)
                break
                
            self.logger.info("[%s] Scraping page %d: %s", self.source_name, page_num, url)
            soup = self.fetch(url)

            if soup is None:
                self.logger.error("[%s] Fetch failed for page %d. Halting source.", self.source_name, page_num)
                break

            for element in soup.select(self.record_selector):
                try:
                    record = self.parse_record(element, url)
                    if record:
                        records.append(record)
                except Exception as e:
                    self.logger.warning("Failed to parse a record on %s: %s", url, e)

            url = self.get_next_url(soup, url)
            page_num += 1

        return records

    @abstractmethod
    def parse_record(self, element, page_url: str) -> dict:
        pass

    @abstractmethod
    def get_next_url(self, soup, current_url: str) -> str | None:
        pass
