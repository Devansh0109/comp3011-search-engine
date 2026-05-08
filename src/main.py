"""Command-line interface for the search engine tool.

The CLI supports the coursework commands: build, load, print, find, and exit.
"""

from src.crawler import crawl
from src.indexer import build_index
from src.search import print_word, find_word
from src.storage import save_index, load_index


def display_results(query, results):
    """Display search results for a query in the command-line interface."""
    if results:
        print(f"Pages containing '{query}':")
        for page in results:
            print(page)
    else:
        print(f"No results found for '{query}'")


def main():
    """Run the interactive command-line interface."""
    index = None

    print("Search Engine Tool")
    print("Available commands: build, load, print <word>, find <query>, exit")

    while True:
        command = input("> ").strip()

        if not command:
            print("Please enter a command.")
            continue

        parts = command.split()
        action = parts[0].lower()

        if action == "exit":
            print("Exiting search tool.")
            break

        elif action == "build":
            pages = crawl()
            print(f"Number of pages crawled: {len(pages)}")

            index = build_index(pages)
            print(f"Number of unique words indexed: {len(index)}")

            save_index(index)

        elif action == "load":
            try:
                index = load_index()
            except FileNotFoundError as error:
                print(error)

        elif action == "print":
            if index is None:
                print("No index loaded. Please run 'build' or 'load' first.")
                continue

            if len(parts) < 2:
                print("Usage: print <word>")
                continue

            word = parts[1]
            print_word(index, word)

        elif action == "find":
            if index is None:
                print("No index loaded. Please run 'build' or 'load' first.")
                continue

            if len(parts) < 2:
                print("Usage: find <query>")
                continue

            query = " ".join(parts[1:])
            results = find_word(index, query)
            display_results(query, results)

        else:
            print("Unknown command. Available commands: build, load, print <word>, find <query>, exit")


if __name__ == "__main__":
    main()