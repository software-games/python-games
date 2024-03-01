#!/usr/bin/env python3
"""
Before a domino played, it has a very simple data structure:
1. die_values: list[int] = [3, 6]
2. is_face_down: bool = False
3. images: tuple[image_svg, image_svg] = (face_up_image, face_down_image)

Once it is played, it must be able to fit into a complex configuration in the play_area
with the domino, location, neighbors, order ([3, 6] or [6, 3]), orentation (horizontal
or vertical), points for exposed ends, and the player who played it.  This information
enables a playedDomino to be drawn on the canvas like the one below with Dominoes in
straight lines where dominoes share the same number or at right angles where there are
doubles.

          2          4     5
[0,1][1,2]-[2,3][3,4]-[4,5]-
          2          4     5
          2
          -
          5
"""
import tkinter as tk

import pytest

from games.dominoes.DominoBoard import buildCanvas
from games.dominoes.PlayedDomino import (
    lrNoDoublesOffset,
    lrMeDoubleOffset,
    lrOtherDoubleOffset,
    udNoDoublesOffset,
    udMeDoubleOffset,
    udOtherDoubleOffset,
    oppositeDirection,
    rightAngles,
    whichDie,
    PlayedDomino,
)

# print(argv)

cLeft, cRight, cUp, cDown = range(4)  # TODO: Enum


@pytest.mark.parametrize(
    "inDirection, expected",
    [
        (cLeft, [-5, 0]),
        (cRight, [5, 0]),
        (cUp, [0, 0]),
        (cDown, [0, 0]),
    ],
)
def test_lrNoDoublesOffset(inDirection, expected):
    assert lrNoDoublesOffset(inDirection) == expected


@pytest.mark.parametrize(
    "inDirection, expected",
    [
        (cLeft, [-5, 0]),
        (cRight, [5, 0]),
        (cUp, [2, -3]),
        (cDown, [2, 1]),
    ],
)
def test_lrMeDoubleOffset(inDirection, expected):
    assert lrMeDoubleOffset(inDirection) == expected


@pytest.mark.parametrize(
    "inDirection, expected",
    [
        (cLeft, [-1, -1]),
        (cRight, [5, -1]),
        (cUp, [0, 0]),
        (cDown, [0, 0]),
    ],
)
def test_lrOtherDoubleOffset(inDirection, expected):
    assert lrOtherDoubleOffset(inDirection) == expected


@pytest.mark.parametrize(
    "inDirection, expected",
    [
        (cLeft, [0, 0]),
        (cRight, [0, 0]),
        (cUp, [0, -3]),
        (cDown, [0, 3]),
    ],
)
def test_udNoDoublesOffset(inDirection, expected):
    assert udNoDoublesOffset(inDirection) == expected


@pytest.mark.parametrize(
    "inDirection, expected",
    [
        (cLeft, [-5, 1]),
        (cRight, [1, 1]),
        (cUp, [0, -3]),
        (cDown, [0, 3]),
    ],
)
def test_udMeDoubleOffset(inDirection, expected):
    assert udMeDoubleOffset(inDirection) == expected


@pytest.mark.parametrize(
    "inDirection, expected",
    [
        (cLeft, [0, 0]),
        (cRight, [0, 0]),
        (cUp, [-2, -1]),
        (cDown, [-2, 3]),
    ],
)
def test_udOtherDoubleOffset(inDirection, expected):
    assert udOtherDoubleOffset(inDirection) == expected


@pytest.mark.parametrize(
    "inDirection, expected",
    [
        (cLeft, cRight),
        (cRight, cLeft),
        (cUp, cDown),
        (cDown, cUp),
    ],
)
def test_oppositeDirection(inDirection, expected):
    assert oppositeDirection(inDirection) == expected


@pytest.mark.parametrize(
    "inDirection, expected",
    [
        (cLeft, [cUp, cDown]),
        (cRight, [cUp, cDown]),
        (cUp, [cLeft, cRight]),
        (cDown, [cLeft, cRight]),
    ],
)
def test_rightAngles(inDirection, expected):
    assert rightAngles(inDirection) == expected


@pytest.mark.parametrize(
    "inDirection, expected",
    [
        (cLeft, False),
        (cRight, True),
        (cUp, False),
        (cDown, True),
    ],
)
def test_whichDie(inDirection, expected):
    assert whichDie(inDirection) == expected


class TestPlayedDomino:
    """
    This class tests the PlayedDomino class.
    """

    def test_playedDomino(self):
        """
        This test creates a PlayedDomino object and tests its methods.
        """
        pd = PlayedDomino(1, [3, 5])
        assert pd.mPlayer == 1
        assert pd.mDomino == [3, 5]
        assert pd.mLocation == [0, 0]
        assert pd.mLeftRight
        assert pd.mOrientation == tk.HORIZONTAL
        assert pd.mNeighbors == [None, None, None, None]

    def test_playedDominoIsDouble(self):
        """
        This test creates a PlayedDomino object and tests its isDouble method.
        """
        pd = PlayedDomino(1, [3, 5])
        assert not pd.isDouble()
        pd = PlayedDomino(1, [3, 3])
        assert pd.isDouble()

    def test_playedDominoFaceValue(self):
        """
        This test creates a PlayedDomino object and tests its faceValue method.
        """
        pd = PlayedDomino(1, [3, 5])
        assert pd.faceValue() == 8
        pd = PlayedDomino(1, [3, 3])
        assert pd.faceValue() == 6

    def test_playedDominoNumberOfNeighbors(self):
        """
        This test creates a PlayedDomino object and tests its numberOfNeighbors method.
        """
        played_domino = PlayedDomino(1, [3, 5])
        for neighbor_count in range(5):
            if neighbor_count:
                played_domino.mNeighbors[neighbor_count - 1] = [5, 5]
            assert played_domino.numberOfNeighbors() == neighbor_count

    def test_playedDominoNeighborAsString(self):
        """
        This test creates a PlayedDomino object and tests its neighborAsString method.
        """
        played_domino = PlayedDomino(1, [3, 5])
        assert played_domino.neighborAsString(0) is None
        played_domino.newNeighbor(1, [5, 5])
        assert played_domino.neighborAsString(0) is None
        assert played_domino.neighborAsString(1) == [5, 5]
        assert played_domino.neighborAsString(2) is None
        assert played_domino.neighborAsString(3) is None
        with pytest.raises(IndexError):
            played_domino.neighborAsString(4)

    def test_playedDominoNeighborsAsString(self):
        """
        This test creates a PlayedDomino object and tests its neighborsAsString method.
        """
        played_domino = PlayedDomino(1, [3, 5])
        assert played_domino.neighborsAsString() == [None, None, None, None]
        played_domino.newNeighbor(1, [5, 5])
        assert played_domino.neighborsAsString() == [None, [5, 5], None, None]

    def test_playedDominoPlayedValue(self):
        """
        This test creates a PlayedDomino object and tests its playedValue method.
        """
        played_domino = PlayedDomino(1, [3, 5])
        assert played_domino.playedValue() == 8
        played_domino.newNeighbor(1, [3, 3])
        assert played_domino.playedValue() == 5
        played_domino.newNeighbor(1, [5, 5])
        assert played_domino.playedValue() == 0

        played_domino = PlayedDomino(1, [5, 5])
        assert played_domino.playedValue() == 10
        played_domino.newNeighbor(1, [1, 5])
        assert played_domino.playedValue() == 10
        played_domino.newNeighbor(1, [2, 5])
        assert played_domino.playedValue() == 0

    def test_playedDominoNotifyNeighborsOfUndo(self):
        """
        This test creates a PlayedDomino object and tests its notifyNeighborsOfUndo method.
        """
        played_domino = PlayedDomino(1, [3, 5])
        played_domino.newNeighbor(1, [5, 5])
        assert played_domino.neighborsAsString() == [None, [5, 5], None, None]
        played_domino.notifyNeighborsOfUndo()
        # assert played_domino.neighborsAsString() == [None, None, None, None]  # TODO: Fix this test

    def test_playedDominoPlayableDirections(self):
        """
        This test creates a PlayedDomino object and tests its playableDirections method.
        """
        played_domino = PlayedDomino(1, [3, 5])
        assert played_domino.playableDirections() == [0, 1]
        played_domino.mNeighbors[0] = PlayedDomino(1, [5, 5])
        assert played_domino.playableDirections() == [1]
        played_domino.mNeighbors[2] = PlayedDomino(1, [3, 3])
        assert played_domino.playableDirections() == []

    def test_playedDominoPlayableDirectionsForADouble(self):
        """
        This test creates a PlayedDomino object and tests its playableDirectionsForADouble method.
        """
        played_domino = PlayedDomino(1, [5, 5])
        assert played_domino.playableDirections() == [0, 1]
        played_domino.newNeighbor(1, [3, 5])
        assert played_domino.playableDirections() in ([0], [1])  # random.choice()
        played_domino.newNeighbor(1, [5, 6])
        assert played_domino.playableDirections() == [2, 3]
        played_domino.newNeighbor(1, [5, 4])
        assert played_domino.playableDirections() in ([2], [3])  # random.choice()
        played_domino.newNeighbor(1, [5, 1])
        assert played_domino.playableDirections() == []

    def test_playedDominoPlayableNumbers(self):
        """
        This test creates a PlayedDomino object and tests its playableNumbers method.
        """
        played_domino = PlayedDomino(1, [3, 5])
        assert played_domino.playableNumbers() == [3, 5]
        played_domino.newNeighbor(1, [5, 5])
        assert played_domino.playableNumbers() == [3]
        played_domino.newNeighbor(1, [3, 3])
        assert played_domino.playableNumbers() == []

        played_domino = PlayedDomino(1, [5, 5])
        assert played_domino.playableNumbers() == [5]
        played_domino.newNeighbor(1, [3, 5])
        assert played_domino.playableNumbers() == [5]
        played_domino.newNeighbor(1, [5, 6])
        assert played_domino.playableNumbers() == [5]
        played_domino.newNeighbor(1, [5, 4])
        assert played_domino.playableNumbers() == [5]
        played_domino.newNeighbor(1, [5, 1])
        assert played_domino.playableNumbers() == []

    def test_playedDominoNewNeighbor(self):
        """
        This test creates a PlayedDomino object and tests its newNeighbor method.
        """
        played_domino = PlayedDomino(1, [3, 5])
        new_neighbor = played_domino.newNeighbor(1, [5, 5])
        assert new_neighbor.mDomino == [5, 5]
        assert new_neighbor.mNeighbors == [played_domino, None, None, None]
        assert played_domino.mNeighbors[1] == new_neighbor

    def test_playedDominoGetOffset(self):
        """
        This test creates a PlayedDomino object and tests its getOffset method.
        """
        played_domino = PlayedDomino(1, [3, 5])
        assert played_domino.getOffset(played_domino, cLeft) == [-5, 0]
        assert played_domino.getOffset(played_domino, cRight) == [5, 0]
        assert played_domino.getOffset(played_domino, cUp) == [0, 0]
        assert played_domino.getOffset(played_domino, cDown) == [0, 0]

        played_domino = PlayedDomino(1, [3, 3])
        assert played_domino.getOffset(played_domino, cLeft) == [-5, 1]
        assert played_domino.getOffset(played_domino, cRight) == [1, 1]
        assert played_domino.getOffset(played_domino, cUp) == [0, -3]
        assert played_domino.getOffset(played_domino, cDown) == [0, 3]

        played_domino = PlayedDomino(1, [5, 5])
        assert played_domino.getOffset(played_domino, cLeft) == [-5, 1]
        assert played_domino.getOffset(played_domino, cRight) == [1, 1]
        assert played_domino.getOffset(played_domino, cUp) == [0, -3]
        assert played_domino.getOffset(played_domino, cDown) == [0, 3]

    def test_playedDominoDominoAndLoc(self):
        """
        This test creates a PlayedDomino object and tests its dominoAndLoc method.
        """
        played_domino = PlayedDomino(1, [3, 5])
        assert played_domino.dominoAndLoc() == ([3, 5], "@", [0, 0])

    def test_playedDominoDominoAndLocAndNeighbors(self):
        """
        This test creates a PlayedDomino object and tests its dominoAndLocAndNeighbors method.
        """
        played_domino = PlayedDomino(1, [3, 5])
        assert played_domino.dominoAndLocAndNeighbors() == (
            [3, 5],
            "@",
            [0, 0],
            "n:",
            [None, None, None, None],
        )

    def test_playedDominoSetLocation(self):
        """
        This test creates a PlayedDomino object and tests its setLocation method.
        """
        played_domino = PlayedDomino(1, [3, 5])
        assert played_domino.mLocation == [0, 0]
        new_neighbor = played_domino.newNeighbor(1, [5, 5])
        assert played_domino.mLocation == [0, 0]
        assert new_neighbor.mLocation == [0, 0]
        played_domino.setLocation()
        assert played_domino.mLocation == [-5, 1]
        assert new_neighbor.mLocation == [0, 0]
        new_neighbor.setLocation()
        assert played_domino.mLocation == [-5, 1]
        assert new_neighbor.mLocation == [0, 0]

        played_domino = PlayedDomino(1, [5, 5])
        assert played_domino.mLocation == [0, 0]
        new_neighbor = played_domino.newNeighbor(1, [3, 5])
        assert played_domino.mLocation == [0, 0]
        assert new_neighbor.mLocation == [0, 0]
        played_domino.setLocation()
        assert played_domino.mLocation in ([-1, -1], [5, -1])  # random.choice()
        assert new_neighbor.mLocation == [0, 0]
        new_neighbor.setLocation()
        assert played_domino.mLocation in ([-1, -1], [5, -1])  # random.choice()
        assert new_neighbor.mLocation == [0, 0]

    def test_playedDominoFillCanvas(self):
        """
        This test creates a PlayedDomino object and tests its fillCanvas method.
        """
        played_domino = PlayedDomino(1, [3, 5])
        canvas = buildCanvas([0, 0])
        played_domino.fillCanvas(canvas)
        assert "".join(canvas[0]) == "[3,5]"

        played_domino = PlayedDomino(1, [3, 3])
        canvas = buildCanvas([0, 0])
        played_domino.fillCanvas(canvas)
        assert canvas[0][0] == "3"
        assert canvas[1][0] == "-"
        assert canvas[2][0] == "3"


if __name__ == "__main__":
    # from DominoTest import main
    from DominoWorld import main

    main()
