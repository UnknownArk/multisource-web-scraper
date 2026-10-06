from processing.validation import validate_record

def test_valid_record():
    record = {
        "source": "Books to Scrape",
        "source_url": "https://books.toscrape.com/catalogue/book_1/",
        "name_or_title": "A Good Book",
        "price": 12.99,
        "rating": 4,
    }
    assert validate_record(record) == []

def test_missing_name_caught():
    record = {
        "source": "Books to Scrape",
        "source_url": "https://books.toscrape.com/catalogue/book_1/",
        "name_or_title": None,
    }
    assert "missing_name" in validate_record(record)

def test_invalid_url_caught():
    record = {
        "source": "Quotes to Scrape",
        "source_url": "not-a-url",
        "name_or_title": "Some quote",
    }
    assert "invalid_url" in validate_record(record)

def test_invalid_rating_caught():
    record = {
        "source": "Books to Scrape",
        "source_url": "https://books.toscrape.com/",
        "name_or_title": "Some Book",
        "rating": 9,
    }
    assert "invalid_rating" in validate_record(record)
