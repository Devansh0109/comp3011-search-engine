"""Indexer module for building an inverted index.

The index maps each token to the pages where it appears and stores both
frequency and positional information for each page.
"""

import re

def tokenize(text):
    """Convert raw page text into lowercase word tokens without punctuation."""
    return re.findall(r"\b[a-zA-Z]+\b", text.lower())

def build_index(pages):
    """Build an inverted index with frequency and position statistics."""
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