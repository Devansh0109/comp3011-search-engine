def print_word(index, word):
    word = word.lower()

    if word in index:
        print(f"Word: {word}")
        for page, data in index[word].items():
            print(f"Page: {page}," 
                  f"Frequency: {data['frequency']},"
                  f"Positions: {data['positions']}"
                  )
    else:
        print(f"Word '{word}' not found in index")

def find_word(index, query):
    words = query.lower().split()

    if not words:
        return []
    
    result_sets = []

    for word in words:
        if word in index:
            result_sets.append(set((index[word].keys())))
        else:
            return []
        
    results = set.intersection(*result_sets)
    return sorted(results)