# AI Usage Documentation

AI tools were utilized during the development of this project to assist with boilerplate generation, architectural decision-making, and regex formulation.

## Tool Used
**Gemini** (Google)

## What AI Helped With
- **Architectural Design:** Suggested implementing the `BaseScraper` as an Abstract Base Class (ABC) using the Template Method pattern to handle the shared pagination and HTTP retry logic.
- **Regex Parsing:** Assisted in writing the regex `\d+(?:\.\d+)?` to extract float values from currency strings gracefully regardless of the currency symbol.
- **Deduplication Strategy:** Suggested standardizing the duplicate fingerprinting using `hashlib.sha256` after stripping punctuation.

## Representative Prompts
- *"Design a base class for a web scraper where subclasses only implement the parsing logic and next-page URL generation. Include urllib3 exponential backoff in the session."*
- *"Write a regex in Python to extract a float from strings like '£51.77' or '$12.99'."*
- *"What is a reliable way to deduplicate records based on string values that might have different capitalization or extra whitespace?"*

## Changes Made After Reviewing AI Output
- **Retry Mechanism Refinement:** The AI initially did not include specific `status_forcelist` HTTP codes for the `Retry` adapter. I added `[429, 500, 502, 503, 504]` to ensure it only retried on appropriate server errors, not on 404s.
- **Deduplication output:** The AI's initial deduplication function simply dropped the duplicates. I modified the logic to return a tuple `(unique, dupes)` so that duplicates could be written to a separate `duplicates.csv` file for auditability.
- **Data Validation:** Changed the AI's boolean validation function to return a list of error strings to feed into the JSON summary report.

## Testing and Verification
- Wrote offline unit tests using `pytest` to strictly verify the deduplication hashing and data cleaning logic without executing network requests.
- Ran the pipeline with the `--max-pages 2` flag to verify end-to-end integration.
- Manually inspected `final_dataset.csv` against the live websites to ensure price and rating accuracy.
