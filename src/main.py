from crawler import crawl
from indexer import build_index

if __name__ == "__main__":
    pages = crawl()
    print(f"Number of pages crawled: {len(pages)}")

    index = build_index(pages)
    print(f"Number of unique words indexed: {len(index)}")

    # check one word
    word = "life"
    if word in index:
        print(f"'{word}' found in pages: {index[word]}")
    else:
        print(f"'{word}' not found")