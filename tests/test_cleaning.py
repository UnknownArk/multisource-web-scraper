from processing.cleaning import clean_price, clean_text, clean_rating, strip_curly_quotes

def test_clean_price():
    assert clean_price("£51.77") == 51.77
    assert clean_price("12.99") == 12.99
    assert clean_price("") is None
    assert clean_price(None) is None

def test_clean_text():
    assert clean_text("  Hello \n World  ") == "Hello World"
    assert clean_text("Hello\xa0World") == "Hello World"
    assert clean_text("   ") is None

def test_clean_rating():
    assert clean_rating("star-rating Three") == 3
    assert clean_rating("star-rating One") == 1
    assert clean_rating("not-a-rating") is None

def test_strip_curly_quotes():
    assert strip_curly_quotes("\u201cHello World\u201d") == "Hello World"
