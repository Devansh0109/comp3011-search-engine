from src.main import display_results


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