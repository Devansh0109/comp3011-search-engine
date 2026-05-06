# COMP3011 Coursework 2: Search Engine Tool

## Project Overview

This project is a command-line search engine tool developed for **COMP3011 Web Services and Web Data Coursework 2**.

The tool crawls the target website, builds an inverted index of the crawled page content, saves the index to the file system, and allows users to search for pages containing specific search terms.

The project demonstrates key search engine concepts including:

- web crawling
- HTML parsing
- inverted indexing
- word frequency tracking
- positional indexing
- query processing
- persistent index storage
- command-line interaction
- automated testing

The implementation is written in Python and uses `requests` for HTTP requests and `BeautifulSoup` for parsing HTML pages.

---

## Target Website

The crawler is designed to crawl the following website:

```text
https://quotes.toscrape.com/
```

This website contains multiple pages of quotes and is designed for web scraping practice.

---

## Key Features

- Crawls all paginated pages of the target website
- Respects a politeness delay of 6 seconds between requests
- Builds an inverted index from the crawled page text
- Stores word frequency for each page
- Stores word position information for each page
- Supports case-insensitive search
- Handles punctuation using regex-based tokenisation
- Saves the generated index to `data/index.json`
- Loads the saved index from the file system
- Provides an interactive command-line interface
- Supports single-word and multi-word queries
- Handles missing words and empty queries gracefully
- Includes automated tests using `pytest`

---

## Project Structure

```text
comp3011-search-engine/
├── data/
│   └── index.json
├── src/
│   ├── __init__.py
│   ├── crawler.py
│   ├── indexer.py
│   ├── main.py
│   ├── search.py
│   └── storage.py
├── tests/
│   ├── __init__.py
│   ├── test_crawler.py
│   ├── test_indexer.py
│   ├── test_main.py
│   ├── test_search.py
│   └── test_storage.py
├── requirements.txt
├── run.py
└── README.md
```

---

## Installation and Setup

### 1. Clone the repository

```bash
git clone <your-github-repository-url>
cd comp3011-search-engine
```

### 2. Create a virtual environment

```bash
python3 -m venv venv
```

### 3. Activate the virtual environment

On macOS/Linux:

```bash
source venv/bin/activate
```

On Windows:

```bash
venv\Scripts\activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

---

## Dependencies

The project uses the following Python libraries:

```text
requests
beautifulsoup4
pytest
```

These dependencies are listed in `requirements.txt`.

---

## How to Run the Search Tool

Run the command-line tool using:

```bash
python3 -m src.main
```

Alternatively, you can run:

```bash
python3 run.py
```

After running the tool, the following interactive prompt should appear:

```text
Search Engine Tool
Available commands: build, load, print <word>, find <query>, exit
>
```

---

## Available Commands

### 1. `build`

The `build` command crawls the website, builds the inverted index, and saves the generated index to `data/index.json`.

```text
> build
```

Example output:

```text
Crawling: https://quotes.toscrape.com
Crawling: https://quotes.toscrape.com/page/2/
Crawling: https://quotes.toscrape.com/page/3/
...
Number of pages crawled: 10
Number of unique words indexed: 842
Index saved to data/index.json
```

The exact number of unique words may vary slightly depending on tokenisation.

Because the crawler follows a 6-second politeness delay between requests, the `build` command may take around one minute to complete.

---

### 2. `load`

The `load` command loads the saved index from `data/index.json`.

```text
> load
```

Example output:

```text
Index loaded from data/index.json
```

If the index file does not exist, the program displays an error message asking the user to run `build` first.

---

### 3. `print <word>`

The `print` command displays the inverted index entry for a particular word.

```text
> print life
```

Example output:

```text
Word: life
Page: https://quotes.toscrape.com, Frequency: 4, Positions: [70, 94, 196, 272]
Page: https://quotes.toscrape.com/page/2/, Frequency: 10, Positions: [8, 207, 228, 488, 524, 588, 598, 599, 617, 630]
```

This output shows:

- the pages where the word appears
- how many times the word appears on each page
- the word positions within each page

---

### 4. `find <query>`

The `find` command returns pages containing the given query term or terms.

Single-word example:

```text
> find love
```

Multi-word example:

```text
> find change world
```

Example output:

```text
Pages containing 'change world':
https://quotes.toscrape.com
https://quotes.toscrape.com/page/2/
```

Multi-word search uses intersection logic, meaning only pages containing **all** query terms are returned.

---

### 5. `exit`

The `exit` command closes the command-line tool.

```text
> exit
```

Example output:

```text
Exiting search tool.
```

---

## Example Demo Session

```text
> load
Index loaded from data/index.json

> print life
Word: life
Page: https://quotes.toscrape.com, Frequency: 4, Positions: [70, 94, 196, 272]
Page: https://quotes.toscrape.com/page/2/, Frequency: 10, Positions: [8, 207, 228, 488, 524, 588, 598, 599, 617, 630]

> find love
Pages containing 'love':
https://quotes.toscrape.com
https://quotes.toscrape.com/page/10/
https://quotes.toscrape.com/page/2/
https://quotes.toscrape.com/page/3/
https://quotes.toscrape.com/page/4/
https://quotes.toscrape.com/page/5/
https://quotes.toscrape.com/page/6/
https://quotes.toscrape.com/page/7/
https://quotes.toscrape.com/page/8/
https://quotes.toscrape.com/page/9/

> find change world
Pages containing 'change world':
https://quotes.toscrape.com
https://quotes.toscrape.com/page/2/

> find xyzabc
No results found for 'xyzabc'

> find
Usage: find <query>

> print
Usage: print <word>

> exit
Exiting search tool.
```

---

## Inverted Index Design

The inverted index is stored as a nested dictionary.

Example structure:

```python
{
    "life": {
        "https://quotes.toscrape.com": {
            "frequency": 4,
            "positions": [70, 94, 196, 272]
        }
    }
}
```

This structure was chosen because it allows direct lookup of a word and provides useful statistics for each page.

For each word, the index stores:

- the page URL
- the frequency of the word on that page
- the positions where the word occurs

This is more useful than a basic index that only records whether a word appears on a page.

---

## Tokenisation

The indexer uses regex-based tokenisation to handle punctuation and case consistently.

For example:

```text
Life, life. LIFE!
```

is tokenised as:

```text
life life life
```

This means the search is case-insensitive and punctuation does not create separate word entries.

---

## Search Logic

Single-word search returns all pages containing the given word.

Multi-word search works by:

1. retrieving the set of pages for each word
2. calculating the intersection of these page sets
3. returning only pages that contain all query words

For example:

```text
find change world
```

returns only pages that contain both `change` and `world`.

Search results are sorted before being returned so that output is deterministic and easier to test.

---

## Storage

The generated inverted index is saved as a JSON file:

```text
data/index.json
```

This allows the index to be reused without crawling the website every time.

The workflow is:

```text
build → crawl website → build index → save index
load  → load saved index → search using print/find
```

---

## Testing

The project uses `pytest` for automated testing.

Run all tests with:

```bash
pytest
```

The test suite covers:

- crawler text extraction
- crawler pagination
- crawler behaviour using mocked HTTP requests
- tokenisation
- index creation
- word frequency counting
- word position tracking
- single-word search
- multi-word search
- empty queries
- missing words
- deterministic result ordering
- saving and loading the index
- command-line result display

Crawler tests use mocking rather than live network requests. This makes the tests faster, more reliable, and independent of the target website being available during testing.

---

## Development Workflow

The project was developed incrementally using Git.

The implementation started with a basic crawler and simple inverted index. It was then improved step-by-step to include:

- politeness delay
- request error handling
- frequency tracking
- positional indexing
- regex tokenisation
- JSON index persistence
- command-line interface
- automated testing and edge-case handling

This iterative approach helped validate each component before adding further functionality.

---

## GenAI Usage Declaration

Generative AI was used as a development support tool during this coursework.

It was used to help with:

- planning the project structure
- understanding the assignment requirements
- debugging Python import and dependency issues
- designing the inverted index structure
- improving the testing strategy
- reviewing possible code improvements
- preparing the development workflow

The code was not used blindly. AI-generated suggestions were tested, modified, and improved throughout development.

For example, the initial indexing approach was basic and was later improved to store both frequency and positional data. Similarly, the first tokenisation approach used simple string splitting, but this was later replaced with regex tokenisation to handle punctuation and case more accurately.

AI was useful for speeding up development and debugging, but it also required critical evaluation. Some early suggestions were too simple for the assignment requirements and had to be refined to better match the marking criteria and demonstrate understanding of search engine concepts.

---

## Notes

- The crawler uses a 6-second politeness delay between requests.
- Running `build` takes longer than `load` because it crawls all pages.
- The saved index file is located at `data/index.json`.
- The project can be tested using `pytest`.
- The command-line interface supports `build`, `load`, `print`, `find`, and `exit`.

---

## Author

Devansh Singhal

COMP3011 Web Services and Web Data  
Coursework 2: Search Engine Tool