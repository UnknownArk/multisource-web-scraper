import csv
import json
import logging
import argparse
import time
from datetime import datetime, timezone
from pathlib import Path

from config import OUTPUT_DIR, LOG_DIR, LOG_FILE, OUTPUT_COLUMNS
from scrapers.books_scraper import BooksScraper
from scrapers.quotes_scraper import QuotesScraper
from processing.cleaning import clean_record
from processing.validation import validate_record
from processing.deduplication import deduplicate

def setup_logging():
    LOG_DIR.mkdir(exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[
            logging.FileHandler(LOG_FILE, encoding="utf-8"),
            logging.StreamHandler(),
        ],
    )

def parse_args():
    parser = argparse.ArgumentParser(description="Multi-Source Web Scraper ETL")
    parser.add_argument("--source", choices=["all", "books", "quotes"], default="all")
    parser.add_argument("--max-pages", type=int, default=None, help="Limit pages per source")
    return parser.parse_args()

def write_csv(records: list, path: Path):
    OUTPUT_DIR.mkdir(exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=OUTPUT_COLUMNS, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(records)
    logging.getLogger("main").info("Wrote %d records to %s", len(records), path.name)

def write_summary(stats: dict, path: Path):
    OUTPUT_DIR.mkdir(exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(stats, f, indent=4)
    logging.getLogger("main").info("Summary written to %s", path.name)

def main():
    args = parse_args()
    setup_logging()
    logger = logging.getLogger("main")
    start_time = time.time()

    logger.info("Starting pipeline. Target: %s, max_pages: %s", args.source, args.max_pages)

    # 1. EXTRACT
    raw_books, raw_quotes = [], []

    if args.source in ("all", "books"):
        try:
            raw_books = BooksScraper().scrape_all(max_pages=args.max_pages)
        except Exception as e:
            logger.error("Books scraper encountered critical failure: %s", e)

    if args.source in ("all", "quotes"):
        try:
            raw_quotes = QuotesScraper().scrape_all(max_pages=args.max_pages)
        except Exception as e:
            logger.error("Quotes scraper encountered critical failure: %s", e)

    all_raw = raw_books + raw_quotes
    logger.info("Extraction complete. Raw total: %d", len(all_raw))

    # 2. TRANSFORM (Clean)
    cleaned = [clean_record(r) for r in all_raw]
    
    # 3. TRANSFORM (Validate)
    valid, rejected = [], []
    rejection_reasons = {}

    for record in cleaned:
        problems = validate_record(record)
        if problems:
            rejected.append(record)
            for problem in problems:
                rejection_reasons[problem] = rejection_reasons.get(problem, 0) + 1
        else:
            valid.append(record)

    logger.info("Validation complete. Valid: %d, Rejected: %d", len(valid), len(rejected))

    # 4. TRANSFORM (Deduplicate)
    unique, dupes = deduplicate(valid)
    logger.info("Deduplication complete. Unique: %d, Duplicates: %d", len(unique), len(dupes))

    # 5. LOAD (Output)
    write_csv(unique, OUTPUT_DIR / "final_dataset.csv")
    if dupes:
        write_csv(dupes, OUTPUT_DIR / "duplicates.csv")
        
    duration = round(time.time() - start_time, 2)
    expected_final = len(cleaned) - len(rejected) - len(dupes)
    reconciliation_ok = (expected_final == len(unique))

    stats = {
        "run_started_at": datetime.now(timezone.utc).isoformat(),
        "duration_seconds": duration,
        "collected_per_source": {
            "Books to Scrape": len(raw_books),
            "Quotes to Scrape": len(raw_quotes),
        },
        "total_raw": len(all_raw),
        "total_after_cleaning": len(cleaned),
        "rejected_count": len(rejected),
        "rejected_by_reason": rejection_reasons,
        "duplicates_detected": len(dupes),
        "final_record_count": len(unique),
        "reconciliation_ok": reconciliation_ok,
    }
    
    write_summary(stats, OUTPUT_DIR / "summary_report.json")
    logger.info("Pipeline finished in %ss. Reconciliation OK: %s", duration, reconciliation_ok)

if __name__ == "__main__":
    main()
