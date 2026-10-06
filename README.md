# Multi-Source Web Scraping ETL

A Python ETL pipeline that collects data from two public websites, cleans it, removes duplicates, and consolidates the output into a single CSV.

## Data Sources
- **Books to Scrape** (https://books.toscrape.com/): ~1,000 books across 50 pages
- **Quotes to Scrape** (https://quotes.toscrape.com/): 100 quotes across 10 pages

## Python Version & Setup
Developed on Python 3.10+ (tested on Python 3.14).

```bash
# Set up isolated environment
python -m venv venv
# Activate environment (Windows)
venv\Scripts\activate
# Install dependencies
pip install -r requirements.txt
```

## Running the Pipeline

```bash
# Run full scrape
python main.py

# Run a quick test (limits to 2 pages per source)
python main.py --max-pages 2

# Run tests
pytest tests/ -v
```

## Architecture & Error Handling
The project follows standard ETL separation of concerns. `BaseScraper` acts as an Abstract Base Class (Template Method pattern) providing shared session handling, an exponential backoff retry mechanism (via `urllib3`), and the pagination loop. Individual scrapers only provide CSS selectors and HTML parsing logic.

If a single record fails parsing, it is skipped and logged. If an entire page fails after 3 retries, the scraper logs the failure and halts that specific source, while the pipeline continues to process the other source.

## Pagination
Pagination is handled dynamically by looking for the `li.next > a` element on each page. Page URLs are never hardcoded, ensuring the scraper continues to function even if the underlying page counts change.

## Deduplication
Uses a cryptographic SHA-256 fingerprint generated from normalized key fields:
- Books: `source + title`
- Quotes: `source + author + quote[:50]`
Normalization forces lowercase and strips all punctuation to catch case-insensitive and whitespace-variant duplicates.

## Assumptions & Limitations
- Detail pages for books are skipped. Fetching 1,000 individual detail pages for `category` and `description` adds roughly 8 minutes of execution time. This is a deliberate trade-off; these fields default to `None`.
- Output is written synchronously to CSV. A production version would stream to a database.
