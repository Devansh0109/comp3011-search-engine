def build_index(pages):
    index = {}

    for url, text in pages.items():
        words = text.lower().split()

        for word in words:
            if word not in index:
                index[word] = {}

            if url not in index[word]:
                index[word][url] = 0

            index[word][url] += 1

    return index