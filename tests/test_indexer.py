from src.indexer import build_index

def test_tokenization_removes_punctuation():
    pages = {
        "page1": "Life, life. LIFE!"
    }

    index = build_index(pages)

    assert "life" in index
    assert index["life"]["page1"]["frequency"] == 3
    assert index["life"]["page1"]["positions"] == [0, 1, 2]


def test_tokenization_ignores_special_characters():
    pages = {
        "page1": "hello!!! world???"
    }

    index = build_index(pages)

    assert "hello" in index
    assert "world" in index
    assert "hello!!!" not in index

def test_basic_index():
    pages = {
        "page1": "hello world",
        "page2": "hello there"
    }

    index = build_index(pages)

    assert "hello" in index
    assert "world" in index
    assert "there" in index

    assert "page1" in index["hello"]
    assert "page2" in index["hello"]

    assert index["hello"]["page1"]["frequency"] == 1
    assert index["hello"]["page2"]["frequency"] == 1

    assert isinstance(index["hello"]["page1"]["positions"], list)

def test_empty_pages():
    pages = {}
    index = build_index(pages)

    assert index == {}

def test_word_frequency():
    pages = {
        "page1": "hello hello world"
    }

    index = build_index(pages)

    assert index["hello"]["page1"]["frequency"] == 2
    assert index["hello"]["page1"]["positions"] == [0, 1]

    assert index["world"]["page1"]["frequency"] == 1
    assert index["world"]["page1"]["positions"] == [2]

def test_word_positions():
    pages = {
        "page1": "hello world hello"
    }

    index = build_index(pages)

    assert index["hello"]["page1"]["frequency"] == 2
    assert index["hello"]["page1"]["positions"] == [0, 2]