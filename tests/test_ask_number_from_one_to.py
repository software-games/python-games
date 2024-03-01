import io

import pytest

from games.dominoes.ask_number_from_one_to import askNumberFromOneTo


@pytest.mark.parametrize(
    "inMax, user_input, expected",
    [
        (6, 1, 1),
        (6, 3, 3),
        (6, 6, 6),
        (6, 1.00001, 1),  # Floats are converted to ints
        (6, "u", "u"),  # Signal to undo...
        (6, "undo", "u"),
        (6, "0\n1", 1),  # Retry on invalid input...
        (6, "7\n6", 6),
        (6, "three\n3", 3),
    ],
)
def test_askNumberFromOneTo(inMax, user_input, expected, monkeypatch):
    """
    How can we mock input() in order to test askNumberFromOneTo()?
    """
    monkeypatch.setattr("sys.stdin", io.StringIO(str(user_input)))
    assert askNumberFromOneTo(inMax) == expected


@pytest.mark.parametrize("user_input", ["q", "quit"])
def test_askNumberFromOneTo_quit(user_input, monkeypatch):
    """
    How can we mock input() in order to test askNumberFromOneTo()?
    """
    monkeypatch.setattr("sys.stdin", io.StringIO(str(user_input)))
    with pytest.raises(AssertionError):
        askNumberFromOneTo(6)
