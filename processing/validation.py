from config import VALID_SOURCES

def validate_record(record: dict) -> list[str]:
    """
    Validates a cleaned record.
    Returns a list of validation failure reasons. An empty list means the record is valid.
    """
    problems = []

    if record.get("source") not in VALID_SOURCES:
        problems.append("unknown_source")

    if not record.get("name_or_title"):
        problems.append("missing_name")

    url = str(record.get("source_url") or "")
    if not url.startswith(("http://", "https://")):
        problems.append("invalid_url")

    price = record.get("price")
    if price is not None:
        if not isinstance(price, (int, float)) or price < 0:
            problems.append("invalid_price")

    rating = record.get("rating")
    if rating is not None:
        if rating not in (1, 2, 3, 4, 5):
            problems.append("invalid_rating")

    return problems
