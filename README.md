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
- TF-IDF-style ranking
- benchmarking and complexity analysis
- critical use of Generative AI during development

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
- Uses a request timeout to avoid hanging indefinitely
- Handles request exceptions gracefully
- Builds an inverted index from the crawled page text
- Stores word frequency for each page
- Stores word position information for each page
- Supports case-insensitive search
- Handles punctuation using regex-based tokenisation
- Saves the generated index to `data/index.json`
- Loads the saved index from the file system
- Provides an interactive command-line interface
- Supports single-word and multi-word queries
- Uses intersection logic for multi-word queries
- Ranks matching pages using a TF-IDF-style relevance score
- Handles missing words, empty queries, unknown commands, and missing index files gracefully
- Includes automated tests using `pytest`
- Includes test coverage reporting using `pytest-cov`
- Includes a benchmark script for build and search performance

---

## Project Structure

```text
comp3011-search-engine/
├── benchmark.py
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
pytest-cov
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

The matching pages are ranked using a TF-IDF-style relevance score.

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

This is more useful than a basic index that only records whether a word appears on a page. Storing positional data also gives the index more flexibility if phrase search or proximity-based ranking were added in the future.

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

This was an improvement over a simpler `.split()` approach, which would treat words such as `life`, `life,`, and `life.` as different tokens.

---

## Search Logic

Single-word search returns all pages containing the given word.

Multi-word search works by:

1. retrieving the set of pages for each word
2. calculating the intersection of these page sets
3. returning only pages that contain all query words
4. ranking the matching pages using a TF-IDF-style relevance score

For example:

```text
find change world
```

returns only pages that contain both `change` and `world`.

If two pages have the same relevance score, they are sorted alphabetically by URL. This keeps the output deterministic and easier to test.

---

## TF-IDF-Style Ranking

The basic requirement for the `find` command is to return pages that contain the search query terms. As an additional enhancement, the search tool ranks matching pages using a TF-IDF-style relevance score.

The score is based on:

```text
term frequency × inverse document frequency
```

Term frequency comes from the inverted index and represents how often a query word appears on a page.

Inverse document frequency gives more weight to words that appear in fewer pages.

For a multi-word query, the tool first finds pages that contain all query words. It then calculates a combined relevance score for each matching page and returns the pages in ranked order.

If two pages have the same score, they are sorted alphabetically by URL to keep the output deterministic and easy to test.

This ranking feature goes beyond the basic requirement of simply returning matching pages and makes the search results more meaningful.

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

Using JSON keeps the saved index human-readable and easy to inspect during development and marking.

---

## Complexity Analysis

The main operations in the search engine are crawling, indexing, loading, printing, and searching.

### Crawling

If the website has `P` pages, the crawler visits each page once.

```text
Time complexity: O(P)
Space complexity: O(P)
```

The crawler also follows a required 6-second politeness delay between requests, so the practical runtime is affected by the number of pages crawled.

---

### Indexing

If the crawled pages contain `N` total word tokens, the indexer processes each token once.

```text
Time complexity: O(N)
Space complexity: O(U + O)
```

Where:

- `U` is the number of unique words
- `O` is the total number of stored word occurrences and positions

The index stores frequency and positional information, so it requires more space than a basic word-to-page index, but it provides richer search statistics.

---

### Single-Word Search

For a single-word query, the search tool directly looks up the word in the inverted index.

```text
Average lookup time: O(1)
Result processing and ranking: O(R log R)
```

Where `R` is the number of matching pages. The `R log R` factor comes from sorting and ranking the results.

---

### Multi-Word Search

For a multi-word query with `Q` query terms, the tool retrieves the page set for each term and calculates the intersection.

```text
Time complexity: O(Q × R)
```

Where `R` is the average number of pages containing each query term.

After matching pages are found, the tool calculates a TF-IDF-style score and sorts the results.

---

### Storage

Saving and loading the index require reading or writing the full JSON index file.

```text
Time complexity: O(S)
Space complexity: O(S)
```

Where `S` is the size of the saved index file.

---

### Design Trade-Off

The project uses a nested dictionary for the inverted index because it provides fast word lookups and makes the data easy to save as JSON.

The trade-off is that storing positions increases memory usage, but it improves the quality of the index and allows more detailed search statistics to be displayed.

Another design choice was to focus the crawler on the paginated quote pages rather than crawling author and tag pages. The paginated pages contain the main searchable quote content required for the assignment, while author and tag pages could introduce duplicate or less relevant content into the index.

---

## Benchmarking

A small benchmark script is included in `benchmark.py`.

Run it with:

```bash
python3 benchmark.py
```

The benchmark measures:

- total build time
- number of pages crawled
- number of unique indexed words
- search time for example queries

Example benchmark output:

```text
Build Benchmark
Pages crawled: 10
Unique words indexed: 842
Total build time: 64.44 seconds
Index loaded from data/index.json

Search Benchmark
Query: 'life' | Results: 10 | Search time: 0.000136 seconds
Query: 'love' | Results: 10 | Search time: 0.000119 seconds
Query: 'change world' | Results: 2 | Search time: 0.000113 seconds
Query: 'xyzabc' | Results: 0 | Search time: 0.000111 seconds
```

The build time is mainly affected by the required 6-second politeness delay between page requests. Search queries are much faster because they use the saved inverted index instead of crawling the website again.

---

## Testing

The project uses `pytest` for automated testing.

Run all tests with:

```bash
pytest
```

To run the tests with coverage reporting:

```bash
pytest --cov=src --cov-report=term-missing
```

The test suite currently contains **35 tests** and achieves approximately **98% total coverage** across the `src/` package.

The test suite covers:

- crawler text extraction
- crawler pagination
- crawler request exception handling
- crawler behaviour using mocked HTTP requests
- tokenisation
- index creation
- word frequency counting
- word position tracking
- single-word search
- multi-word search
- TF-IDF-style relevance scoring
- ranking pages by query relevance
- empty queries
- missing words
- deterministic result ordering
- saving and loading the index
- command-line result display
- command-line `build`, `load`, `print`, `find`, `exit`, empty input, and unknown command behaviour

Crawler tests use mocking rather than live network requests. This makes the tests faster, more reliable, and independent of the target website being available during testing.

Testing the command-line interface was important because the CLI controls the required coursework commands. Mocking `input()` allowed the interactive command loop to be tested automatically without manual input.

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
- TF-IDF-style ranking
- automated testing and edge-case handling
- command-line interface testing using mocked input
- test coverage reporting using `pytest-cov`
- benchmarking and complexity analysis
- final documentation and README improvements

This iterative approach helped validate each component before adding further functionality.

GitHub issues were also used to document the main development tasks and show the progression from initial setup to final testing and documentation.

---

## GenAI Usage Declaration and Critical Evaluation

Generative AI was used as a development support tool during this coursework. The main tools used were ChatGPT and Claude. They were used to support planning, debugging, explanation, testing strategy, and review. They were not used as a replacement for understanding or validation.

GenAI helped in several useful ways:

- planning the project structure around separate crawler, indexer, search, storage, and CLI modules
- interpreting the coursework brief and mapping features to marking criteria
- debugging early Python environment issues such as `python` versus `python3`, missing dependencies, virtual environments, and import path problems
- suggesting an incremental development workflow with meaningful Git commits
- helping design unit tests for individual components
- reviewing the project against the marking rubric
- identifying that the CLI loop needed stronger automated testing
- suggesting benchmarking and complexity analysis as evidence for higher-band criteria

However, AI-generated suggestions were not accepted blindly. Some early suggestions were useful starting points but were too basic for a high-mark submission. For example, the initial inverted index design only stored which pages contained a word. This was later improved to store both frequency and positional information, which better matches the coursework requirement for word statistics.

Another example was tokenisation. A simple `.split()` approach was easy to implement, but it caused punctuation problems because words such as `life`, `life,`, and `life.` could be treated differently. This was improved using regex-based tokenisation, making the index cleaner and the search behaviour more reliable.

The search function also developed beyond the minimum requirement. The basic requirement was to return pages containing the query terms. After the core functionality was working, a TF-IDF-style ranking system was added so that matching pages could be ordered by relevance rather than only being returned alphabetically. This was added carefully after the basic intersection logic was already working and tested.

GenAI also had limitations. Some suggestions focused on making the code work quickly, but not necessarily on proving correctness. For example, the original test suite covered the indexer and search logic but did not test enough of the command-line interface. After reviewing this limitation, additional tests were added using mocked `input()` to cover the `build`, `load`, `print`, `find`, `exit`, empty input, and unknown command paths.

Using GenAI affected the development process by speeding up debugging and helping generate ideas, but the final implementation was refined through manual testing, automated tests, code review, and design decisions. The final project reflects an iterative process where AI suggestions were checked, improved, and adapted to the assignment requirements.

Overall, GenAI was most useful as a guide and reviewer. It helped identify possible improvements, but the important decisions were validated through testing, Git history, benchmark results, and understanding of the search engine concepts implemented in the code.

---

## Notes

- The crawler uses a 6-second politeness delay between requests.
- Running `build` takes longer than `load` because it crawls all pages.
- The saved index file is located at `data/index.json`.
- The benchmark script is located at `benchmark.py`.
- The project can be tested using `pytest`.
- Coverage can be checked using `pytest --cov=src --cov-report=term-missing`.
- The command-line interface supports `build`, `load`, `print`, `find`, and `exit`.

---

## Author

Devansh Singhal

COMP3011 Web Services and Web Data  
Coursework 2: Search Engine Tool