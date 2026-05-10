"""Search module for printing index entries and finding ranked results.

The search logic supports single-word and multi-word queries. Multi-word
queries use set intersection so that only pages containing all query terms
are returned. Matching pages are ranked using a TF-IDF-style score.
"""

import math
import difflib
import re

def tokenize_query(query):
    """Convert a user query into lowercase word tokens without punctuation."""
    return re.findall(r"\b[a-zA-Z]+\b", query.lower())

def print_word(index, word):
    """Print the inverted index entry for a single word."""
    word = word.lower()

    if word in index:
        print(f"Word: {word}")
        for page, data in index[word].items():
            print(
                f"Page: {page}, "
                f"Frequency: {data['frequency']}, "
                f"Positions: {data['positions']}"
            )
    else:
        print(f"Word '{word}' not found in index")

def get_all_pages(index):
    """Return all page URLs stored in the inverted index."""
    pages = set()

    for word_data in index.values():
        pages.update(word_data.keys())

    return pages


def calculate_tfidf_scores(index, query):
    """Calculate TF-IDF-style scores for pages matching all query words."""
    words = query.lower().split()

    if not words:
        return {}

    all_pages = get_all_pages(index)
    total_pages = len(all_pages)

    if total_pages == 0:
        return {}

    result_sets = []

    for word in words:
        if word not in index:
            return {}

        result_sets.append(set(index[word].keys()))

    matching_pages = set.intersection(*result_sets)
    scores = {}

    for page in matching_pages:
        score = 0

        for word in words:
            term_frequency = index[word][page]["frequency"]
            document_frequency = len(index[word])

            inverse_document_frequency = math.log(total_pages / document_frequency)

            score += term_frequency * inverse_document_frequency

        scores[page] = score

    return scores

def find_word(index, query):
    """Return ranked pages containing all words in the query."""
    scores = calculate_tfidf_scores(index, query)

    return sorted(scores.keys(), key=lambda page: (-scores[page], page))

def find_phrase(index, phrase):
    """Return pages where all words in a phrase appear consecutively."""
    words = tokenize_query(phrase)

    if not words:
        return []

    if len(words) == 1:
        return find_word(index, words[0])

    for word in words:
        if word not in index:
            return []

    candidate_pages = set(index[words[0]].keys())

    for word in words[1:]:
        candidate_pages = candidate_pages.intersection(index[word].keys())

    matching_pages = []

    for page in candidate_pages:
        first_word_positions = index[words[0]][page]["positions"]

        for start_position in first_word_positions:
            phrase_found = True

            for offset, word in enumerate(words[1:], start=1):
                expected_position = start_position + offset
                word_positions = index[word][page]["positions"]

                if expected_position not in word_positions:
                    phrase_found = False
                    break

            if phrase_found:
                matching_pages.append(page)
                break

    return sorted(matching_pages)


def suggest_words(index, query, max_suggestions=3):
    """Suggest close indexed words for query terms that are not found."""
    suggestions = {}
    vocabulary = list(index.keys())

    for word in tokenize_query(query):
        if word not in index:
            matches = difflib.get_close_matches(
                word,
                vocabulary,
                n=max_suggestions,
                cutoff=0.75
            )

            if matches:
                suggestions[word] = matches

    return suggestions