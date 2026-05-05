import re

def tokenize(text):
    return re.findall(r"\b[a-zA-Z]+\b", text.lower())

def build_index(pages):
    index = {}

    for url, text in pages.items():
        words = tokenize(text)

        for position, word in enumerate(words):
            if word not in index:
                index[word] = {}

            if url not in index[word]:
                index[word][url] = {
                    "frequency": 0,
                    "positions": []
                }

            index[word][url]["frequency"] += 1
            index[word][url]["positions"].append(position)

    return index