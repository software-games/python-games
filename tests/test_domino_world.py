import pytest

from games.dominoes.domino_world import initDominos, pointsRounded


def test_initDominos():
    assert initDominos() == [
        [0, 0],
        [0, 1],
        [0, 2],
        [0, 3],
        [0, 4],
        [0, 5],
        [0, 6],
        [1, 1],
        [1, 2],
        [1, 3],
        [1, 4],
        [1, 5],
        [1, 6],
        [2, 2],
        [2, 3],
        [2, 4],
        [2, 5],
        [2, 6],
        [3, 3],
        [3, 4],
        [3, 5],
        [3, 6],
        [4, 4],
        [4, 5],
        [4, 6],
        [5, 5],
        [5, 6],
        [6, 6],
    ]


@pytest.mark.parametrize(
    "inValue, expected",
    [
        (0, 0),
        (1, 0),
        (2, 0),
        (3, 1),
        (7, 1),
        (8, 2),
        (12, 2),
        (13, 3),
        (17, 3),
        (18, 4),
        (22, 4),
        (23, 5),
    ],
)
def test_pointsRounded(inValue, expected):
    assert pointsRounded(inValue) == expected
