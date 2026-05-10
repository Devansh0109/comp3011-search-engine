from src.search import (
    print_word,
    find_word,
    calculate_tfidf_scores,
    find_phrase,
    suggest_words,
)

def test_print_word_found(capsys):
    index = {
        "hello": {
            "page1": {"frequency": 2, "positions": [0, 1]}
        }
    }

    print_word(index, "hello")

    captured = capsys.readouterr()
    assert "hello" in captured.out
    assert "page1" in captured.out


def test_print_word_not_found(capsys):
    index = {}

    print_word(index, "missing")

    captured = capsys.readouterr()
    assert "not found" in captured.out.lower()

def test_find_word_found():
    index = {
        "hello": {
            "page1": {"frequency": 1, "positions": [0]},
            "page2": {"frequency": 2, "positions": [1, 3]}
        }
    }

    results = find_word(index, "hello")

    assert "page1" in results
    assert "page2" in results


def test_find_word_not_found():
    index = {}

    results = find_word(index, "missing")
    assert results == []

def test_multi_word_query():
    index = {
        "hello": {
            "page1": {"frequency": 1, "positions": [0]},
            "page2": {"frequency": 1, "positions": [1]}
        },
        "world": {
            "page2": {"frequency": 1, "positions": [2]},
            "page3": {"frequency": 1, "positions": [0]}
        }
    }

    results = find_word(index, "hello world")
    assert results == ["page2"] or results == ["page2"]

def test_multi_word_no_match():
    index = {
        "hello": {
            "page1": {"frequency": 1, "positions": [0]}
        },
        "world": {
            "page2": {"frequency": 1, "positions": [0]}
        }
    }

    results = find_word(index, "hello world")
    assert results == []

def test_empty_query():
    index = {
        "hello": {
            "page1": {"frequency": 1, "positions": [0]}
        }
    }

    results = find_word(index, "")
    assert results == []

def test_find_word_returns_sorted_results():
    index = {
        "hello": {
            "page3": {"frequency": 1, "positions": [0]},
            "page1": {"frequency": 1, "positions": [0]},
            "page2": {"frequency": 1, "positions": [0]}
        }
    }

    results = find_word(index, "hello")

    assert results == ["page1", "page2", "page3"]

def test_tfidf_ranking_prioritises_higher_frequency_page():
    index = {
        "hello": {
            "page1": {"frequency": 1, "positions": [0]},
            "page2": {"frequency": 3, "positions": [0, 2, 4]}
        },
        "other": {
            "page3": {"frequency": 1, "positions": [0]}
        }
    }

    results = find_word(index, "hello")

    assert results[0] == "page2"


def test_tfidf_scores_only_include_pages_matching_all_query_words():
    index = {
        "hello": {
            "page1": {"frequency": 2, "positions": [0, 1]},
            "page2": {"frequency": 1, "positions": [0]}
        },
        "world": {
            "page1": {"frequency": 1, "positions": [2]}
        },
        "other": {
            "page3": {"frequency": 1, "positions": [0]}
        }
    }

    scores = calculate_tfidf_scores(index, "hello world")

    assert "page1" in scores
    assert "page2" not in scores
    assert "page3" not in scores
    assert scores["page1"] > 0

def test_calculate_tfidf_scores_with_empty_index():
    scores = calculate_tfidf_scores({}, "hello")

    assert scores == {}

def test_calculate_tfidf_scores_returns_empty_when_query_word_missing():
    index = {
        "hello": {
            "page1": {"frequency": 1, "positions": [0]}
        }
    }

    scores = calculate_tfidf_scores(index, "hello missing")

    assert scores == {}

def test_find_phrase_returns_page_for_exact_phrase():
    index = {
        "change": {
            "page1": {"frequency": 1, "positions": [0]},
            "page2": {"frequency": 1, "positions": [3]}
        },
        "world": {
            "page1": {"frequency": 1, "positions": [1]},
            "page2": {"frequency": 1, "positions": [7]}
        }
    }

    results = find_phrase(index, "change world")

    assert results == ["page1"]


def test_find_phrase_returns_empty_when_words_not_consecutive():
    index = {
        "change": {
            "page1": {"frequency": 1, "positions": [0]}
        },
        "world": {
            "page1": {"frequency": 1, "positions": [3]}
        }
    }

    results = find_phrase(index, "change world")

    assert results == []


def test_find_phrase_single_word_uses_normal_search():
    index = {
        "hello": {
            "page1": {"frequency": 1, "positions": [0]}
        }
    }

    results = find_phrase(index, "hello")

    assert results == ["page1"]


def test_suggest_words_returns_close_match_for_missing_word():
    index = {
        "love": {
            "page1": {"frequency": 1, "positions": [0]}
        },
        "life": {
            "page2": {"frequency": 1, "positions": [0]}
        }
    }

    suggestions = suggest_words(index, "lov")

    assert "lov" in suggestions
    assert "love" in suggestions["lov"]


def test_suggest_words_returns_empty_for_known_word():
    index = {
        "love": {
            "page1": {"frequency": 1, "positions": [0]}
        }
    }

    suggestions = suggest_words(index, "love")

    assert suggestions == {}