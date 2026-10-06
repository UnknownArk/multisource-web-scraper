from processing.deduplication import deduplicate

def test_exact_duplicate_detected():
    records = [
        {"source": "Books to Scrape", "name_or_title": "Same Book", "author": None},
        {"source": "Books to Scrape", "name_or_title": "Same Book", "author": None},
    ]
    unique, dupes = deduplicate(records)
    assert len(unique) == 1
    assert len(dupes) == 1

def test_case_insensitive_duplicate():
    records = [
        {"source": "Books to Scrape", "name_or_title": "Example Book", "author": None},
        {"source": "Books to Scrape", "name_or_title": "EXAMPLE BOOK", "author": None},
    ]
    unique, dupes = deduplicate(records)
    assert len(unique) == 1
    assert len(dupes) == 1

def test_different_books_not_duplicates():
    records = [
        {"source": "Books to Scrape", "name_or_title": "Book One", "author": None},
        {"source": "Books to Scrape", "name_or_title": "Book Two", "author": None},
    ]
    unique, dupes = deduplicate(records)
    assert len(unique) == 2
    assert len(dupes) == 0
