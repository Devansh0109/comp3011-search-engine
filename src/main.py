"""Command-line interface for the search engine tool.

The CLI supports the coursework commands: build, load, print, find, and exit.
"""

from src.crawler import crawl
from src.indexer import build_index
from src.search import find_phrase, find_word, print_word, suggest_words
from src.storage import save_index, load_index

def display_help():
    """Print the available command-line commands."""
    print("Available commands:")
    print("  build             Crawl the website, build the index, and save it")
    print("  load              Load the saved index from data/index.json")
    print("  print <word>      Print frequency and positions for a word")
    print("  find <query>      Find pages containing all query words")
    print("  phrase <query>    Find pages containing an exact phrase")
    print("  help              Show this help message")
    print("  exit              Exit the search tool")

def display_results(query, results, result_type="Pages containing"):
    """Display search results for a query in the command-line interface."""
    if results:
        print(f"{result_type} '{query}':")
        for page in results:
            print(page)
    else:
        print(f"No results found for '{query}'")

def display_suggestions(index, query):
    """Display spelling suggestions for missing query words when available."""
    suggestions = suggest_words(index, query)

    for missing_word, matches in suggestions.items():
        joined_matches = ", ".join(matches)
        print(f"Did you mean for '{missing_word}': {joined_matches}?")

def main():
    """Run the interactive command-line interface."""
    index = None

    print("Search Engine Tool")
    display_help()

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

        elif action == "help":
            display_help()

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

            if not results:
                display_suggestions(index, query)

        elif action == "phrase":
            if index is None:
                print("No index loaded. Please run 'build' or 'load' first.")
                continue

            if len(parts) < 2:
                print("Usage: phrase <query>")
                continue

            phrase = " ".join(parts[1:])
            results = find_phrase(index, phrase)
            display_results(phrase, results, result_type="Pages containing phrase")

            if not results:
                display_suggestions(index, phrase)

        else:
            print("Unknown command. Type 'help' to see available commands.")

if __name__ == "__main__":
    main()