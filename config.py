from pathlib import Path

# File Paths
BASE_DIR = Path(__file__).parent
OUTPUT_DIR = BASE_DIR / "output"
LOG_DIR = BASE_DIR / "logs"
LOG_FILE = LOG_DIR / "scraper.log"

# Website URLs
BOOKS_START_URL = "https://books.toscrape.com/"
QUOTES_START_URL = "https://quotes.toscrape.com/"

# Network Settings
REQUEST_DELAY = 0.5
REQUEST_TIMEOUT = 10
MAX_RETRIES = 3
BACKOFF_FACTOR = 1.0
RETRY_STATUS_CODES = [429, 500, 502, 503, 504]

# Output Schema
OUTPUT_COLUMNS = [
    "source",
    "source_url",
    "name_or_title",
    "category",
    "price",
    "rating",
    "author",
    "tags",
    "description",
    "scraped_at",
]

# Validation & Cleaning Config
VALID_SOURCES = {"Books to Scrape", "Quotes to Scrape"}

RATING_WORDS = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
}