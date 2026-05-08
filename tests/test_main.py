from unittest.mock import patch
from src.main import display_results, main


def test_display_results_with_matches(capsys):
    display_results("hello", ["page1", "page2"])

    captured = capsys.readouterr()

    assert "Pages containing 'hello':" in captured.out
    assert "page1" in captured.out
    assert "page2" in captured.out


def test_display_results_with_no_matches(capsys):
    display_results("missing", [])

    captured = capsys.readouterr()

    assert "No results found for 'missing'" in captured.out

def test_main_exit_command(capsys):
    with patch("builtins.input", side_effect=["exit"]):
        main()

    captured = capsys.readouterr()

    assert "Search Engine Tool" in captured.out
    assert "Exiting search tool." in captured.out


def test_main_empty_command(capsys):
    with patch("builtins.input", side_effect=["", "exit"]):
        main()

    captured = capsys.readouterr()

    assert "Please enter a command." in captured.out


def test_main_unknown_command(capsys):
    with patch("builtins.input", side_effect=["randomcommand", "exit"]):
        main()

    captured = capsys.readouterr()

    assert "Unknown command" in captured.out


def test_main_find_before_loading_index(capsys):
    with patch("builtins.input", side_effect=["find hello", "exit"]):
        main()

    captured = capsys.readouterr()

    assert "No index loaded" in captured.out


def test_main_print_before_loading_index(capsys):
    with patch("builtins.input", side_effect=["print hello", "exit"]):
        main()

    captured = capsys.readouterr()

    assert "No index loaded" in captured.out


def test_main_load_then_find(capsys):
    mock_index = {
        "hello": {
            "page1": {
                "frequency": 1,
                "positions": [0]
            }
        }
    }

    with patch("builtins.input", side_effect=["load", "find hello", "exit"]):
        with patch("src.main.load_index", return_value=mock_index):
            main()

    captured = capsys.readouterr()

    assert "Pages containing 'hello':" in captured.out
    assert "page1" in captured.out


def test_main_load_then_print(capsys):
    mock_index = {
        "hello": {
            "page1": {
                "frequency": 1,
                "positions": [0]
            }
        }
    }

    with patch("builtins.input", side_effect=["load", "print hello", "exit"]):
        with patch("src.main.load_index", return_value=mock_index):
            main()

    captured = capsys.readouterr()

    assert "Word: hello" in captured.out
    assert "page1" in captured.out


def test_main_load_missing_file(capsys):
    with patch("builtins.input", side_effect=["load", "exit"]):
        with patch("src.main.load_index", side_effect=FileNotFoundError("Index file not found")):
            main()

    captured = capsys.readouterr()

    assert "Index file not found" in captured.out


def test_main_find_without_query(capsys):
    mock_index = {
        "hello": {
            "page1": {
                "frequency": 1,
                "positions": [0]
            }
        }
    }

    with patch("builtins.input", side_effect=["load", "find", "exit"]):
        with patch("src.main.load_index", return_value=mock_index):
            main()

    captured = capsys.readouterr()

    assert "Usage: find <query>" in captured.out


def test_main_print_without_word(capsys):
    mock_index = {
        "hello": {
            "page1": {
                "frequency": 1,
                "positions": [0]
            }
        }
    }

    with patch("builtins.input", side_effect=["load", "print", "exit"]):
        with patch("src.main.load_index", return_value=mock_index):
            main()

    captured = capsys.readouterr()

    assert "Usage: print <word>" in captured.out


def test_main_build_command(capsys):
    mock_pages = {
        "page1": "hello world"
    }

    mock_index = {
        "hello": {
            "page1": {
                "frequency": 1,
                "positions": [0]
            }
        }
    }

    with patch("builtins.input", side_effect=["build", "exit"]):
        with patch("src.main.crawl", return_value=mock_pages):
            with patch("src.main.build_index", return_value=mock_index):
                with patch("src.main.save_index"):
                    main()

    captured = capsys.readouterr()

    assert "Number of pages crawled: 1" in captured.out
    assert "Number of unique words indexed: 1" in captured.out