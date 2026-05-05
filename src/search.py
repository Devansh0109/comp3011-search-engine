def print_word(index, word):
    word = word.lower()

    if word in index:
        print(f"Word: {word}")
        for page, data in index[word].items():
            print(f"Page: {page}, Frequency: {data['frequency']}, Positions: {data['positions']}")
    else:
        print(f"Word '{word}' not found in index")