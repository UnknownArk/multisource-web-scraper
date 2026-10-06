import re
import hashlib

def make_fingerprint(record: dict) -> str:
    """
    Creates a normalized SHA-256 fingerprint for deduplication.
    Ignores casing, punctuation, and irregular whitespace.
    """
    source = record.get("source", "")
    name = record.get("name_or_title", "") or ""

    if source == "Books to Scrape":
        key = f"{source} {name}"
    else:
        author = record.get("author", "") or ""
        key = f"{source} {author} {name[:50]}"

    normalized = re.sub(r"[^\w\s]", "", key.lower())
    normalized = " ".join(normalized.split())

    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()

def deduplicate(records: list[dict]) -> tuple[list[dict], list[dict]]:
    """
    Separates a list of records into unique records and duplicates.
    Returns (unique_records, duplicate_records).
    """
    seen = set()
    unique = []
    duplicates = []

    for record in records:
        fp = make_fingerprint(record)
        if fp in seen:
            duplicates.append(record)
        else:
            seen.add(fp)
            unique.append(record)

    return unique, duplicates
