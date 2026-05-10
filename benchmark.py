"""Benchmark script for measuring build and search performance."""

import time
from src.crawler import crawl
from src.indexer import build_index
from src.search import find_word, find_phrase, suggest_words
from src.storage import load_index, save_index


def benchmark_build_process():
    """Measure the time taken to crawl, index, and save the website data."""
    start_time = time.perf_counter()

    pages = crawl()
    index = build_index(pages)
    save_index(index)

    end_time = time.perf_counter()

    print("Build Benchmark")
    print(f"Pages crawled: {len(pages)}")
    print(f"Unique words indexed: {len(index)}")
    print(f"Total build time: {end_time - start_time:.2f} seconds")


def benchmark_search_process():
    """Measure search time for several example queries."""
    index = load_index()

    queries = [
        "life",
        "love",
        "change world",
        "xyzabc"
    ]

    print("\nSearch Benchmark")

    for query in queries:
        start_time = time.perf_counter()
        results = find_word(index, query)
        end_time = time.perf_counter()

        print(
            f"Query: '{query}' | "
            f"Results: {len(results)} | "
            f"Search time: {end_time - start_time:.6f} seconds"
        )

def benchmark_phrase_search_process():
    """Measure phrase search time for example phrase queries."""
    index = load_index()

    phrases = [
        "universal truth",
        "good thing",
        "creating yourself"
    ]

    print("\nPhrase Search Benchmark")

    for phrase in phrases:
        start_time = time.perf_counter()
        results = find_phrase(index, phrase)
        end_time = time.perf_counter()

        print(
            f"Phrase: '{phrase}' | "
            f"Results: {len(results)} | "
            f"Phrase search time: {end_time - start_time:.6f} seconds"
        )


def benchmark_suggestion_process():
    """Measure suggestion generation time for misspelled query terms."""
    index = load_index()

    queries = [
        "lov",
        "lif",
        "xyzabc"
    ]

    print("\nSuggestion Benchmark")

    for query in queries:
        start_time = time.perf_counter()
        suggestions = suggest_words(index, query)
        end_time = time.perf_counter()

        print(
            f"Query: '{query}' | "
            f"Suggestions: {suggestions} | "
            f"Suggestion time: {end_time - start_time:.6f} seconds"
        )

if __name__ == "__main__":
    benchmark_build_process()
    benchmark_search_process()
    benchmark_phrase_search_process()
    benchmark_suggestion_process()