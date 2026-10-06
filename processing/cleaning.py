import re
from config import RATING_WORDS

def clean_text(value: str | None) -> str | None:
    if not value:
        return None
    text = value.replace("\xa0", " ")
    text = " ".join(text.split())
    return text if text else None

def strip_curly_quotes(value: str | None) -> str | None:
    if not value:
        return None
    return value.replace("\u201c", "").replace("\u201d", "").strip()

def clean_price(raw: str | None) -> float | None:
    if not raw:
        return None
    match = re.search(r"\d+(?:\.\d+)?", raw.replace(",", ""))
    return float(match.group()) if match else None

def clean_rating(raw: str | None) -> int | None:
    if not raw:
        return None
    for word in raw.lower().split():
        if word in RATING_WORDS:
            return RATING_WORDS[word]
    return None

def normalize_url(url: str | None) -> str | None:
    if not url:
        return None
    url = url.strip()
    if url.startswith(("http://", "https://")):
        return url
    return None

def clean_record(raw: dict) -> dict:
    """
    Applies standard cleaning functions to a raw record dictionary.
    """
    name = clean_text(raw.get("name_or_title"))
    
    if raw.get("source") == "Quotes to Scrape":
        name = strip_curly_quotes(name)

    return {
        "source": clean_text(raw.get("source")),
        "source_url": normalize_url(raw.get("source_url")),
        "name_or_title": name,
        "category": clean_text(raw.get("category")),
        "price": clean_price(raw.get("price_raw")),
        "rating": clean_rating(raw.get("rating_raw")),
        "author": clean_text(raw.get("author")),
        "tags": clean_text(raw.get("tags")),
        "description": clean_text(raw.get("description")),
        "scraped_at": raw.get("scraped_at"),
    }
