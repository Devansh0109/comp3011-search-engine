from src.crawler import crawl
from src.indexer import build_index
from src.search import print_word, find_word
from src.storage import save_index, load_index

def main():
    pages = crawl()
    print(f"Number of pages crawled: {len(pages)}")

    index = build_index(pages)
    print(f"Number of unique words indexed: {len(index)}")

    save_index(index)

    loaded_index = load_index()

    print_word(loaded_index, "life")

    query = "life love"
    results = find_word(loaded_index, query)

    if results:
        print(f"Pages containing '{query}':")
        for page in results:
            print(page)
    else:
        print(f"No results found for '{query}'")

if __name__ == "__main__":
    main()