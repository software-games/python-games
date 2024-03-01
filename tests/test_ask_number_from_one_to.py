#!/usr/bin/env python3
import io

import pytest


def askNumberFromOneTo(inMax):
    intMax = int(inMax)
    if intMax < 1:
        return 1
    # print('inMax:', inMax, 'intMax:', intMax)
    print(f"Enter a number from 1 to {inMax}: ")
    s = input(f"Enter a number from 1 to {intMax}: ").lower()
    assert s[0] != "q"
    if s[0] == "u":
        return s[0]
    try:
        i = int(float(s))
    except (TypeError, ValueError):
        i = 0
    print("s:", s, "i:", i)
    return i if 1 <= i <= intMax else askNumberFromOneTo(intMax)


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


def main():
    print(f"Got: {askNumberFromOneTo(10.34)}")


if __name__ == "__main__":
    main()
