from src.crawler import crawl
from src.indexer import build_index
from src.search import print_word, find_word

def main():
    pages = crawl()
    print(f"Number of pages crawled: {len(pages)}")

    index = build_index(pages)
    print(f"Number of unique words indexed: {len(index)}")

    print_word(index, "life")

    results = find_word(index, "life")

    if results:
        print(f"Pages containing 'life':")
        for page in results:
            print(page)
    else:
        print("No results found")

    # check one word
    word = "life"
    if word in index:
        print(f"'{word}' found in pages: {index[word]}")
    else:
        print(f"'{word}' not found")


if __name__ == "__main__":
    main()