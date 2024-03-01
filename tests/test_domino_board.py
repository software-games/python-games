from __future__ import annotations

# from games.dominoes.domino_board import DominoBoard, buildCanvas, printCanvas

from games.dominoes.domino_board import buildCanvas


def test_buildCanvas():
    assert buildCanvas([1, 1]) == [
        [" ", " ", " ", " ", " ", " "],
        [" ", " ", " ", " ", " ", " "],
        [" ", " ", " ", " ", " ", " "],
        [" ", " ", " ", " ", " ", " "],
        [" ", " ", " ", " ", " ", " "],
        [" ", " ", " ", " ", " ", " "],
    ]
