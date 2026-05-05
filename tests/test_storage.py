import os

from src.storage import save_index, load_index


def test_save_and_load_index(tmp_path):
    index = {
        "hello": {
            "page1": {
                "frequency": 2,
                "positions": [0, 1]
            }
        }
    }

    file_path = tmp_path / "test_index.json"

    save_index(index, file_path)
    loaded_index = load_index(file_path)

    assert loaded_index == index


def test_load_missing_index_file(tmp_path):
    missing_file = tmp_path / "missing_index.json"

    try:
        load_index(missing_file)
        assert False
    except FileNotFoundError as error:
        assert "Please run 'build' first" in str(error)