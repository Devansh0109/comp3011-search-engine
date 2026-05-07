import math

def print_word(index, word):
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

    pages = set()

    for word_data in index.values():
        pages.update(word_data.keys())

    return pages


def calculate_tfidf_scores(index, query):

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
    scores = calculate_tfidf_scores(index, query)

    return sorted(scores.keys(), key=lambda page: (-scores[page], page))