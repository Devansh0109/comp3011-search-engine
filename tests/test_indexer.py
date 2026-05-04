import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.indexer import build_index

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