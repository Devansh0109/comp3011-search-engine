import time

from src.crawler import crawl
from src.indexer import build_index
from src.search import find_word
from src.storage import load_index, save_index


def benchmark_build_process():
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


if __name__ == "__main__":
    benchmark_build_process()
    benchmark_search_process()