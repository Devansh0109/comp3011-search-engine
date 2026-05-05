from src.search import print_word, find_word

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

