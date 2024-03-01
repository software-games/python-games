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
# from random import choice, shuffle
import tkinter as tk

# from sys import argv
# from askNumberFromOneTo import askNumberFromOneTo
# from PrintableDomino import lrNoDoublesOffset, lrMeDoubleOffset, lrOtherDoubleOffset, udNoDoublesOffset, udMeDoubleOffset,
# udOtherDoubleOffset
from random import choice

import pytest

from DominoBoard import buildCanvas

# print(argv)

cLeft, cRight, cUp, cDown = range(4)  # TODO: Enum


def lrNoDoublesOffset(inDirection) -> list[int]:
    """
    TODO: Return a tuple of two integers instead of a list.
    """
    # print('lrNoDoublesOffset({})'.format(inDirection), end='')
    return [[-5, 0], [5, 0], [0, 0], [0, 0]][inDirection]


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


def lrMeDoubleOffset(inDirection):
    """
    TODO: Return a tuple of two integers instead of a list.
    """
    # print('lrMeDoubleOffset({})'.format(inDirection), end='')
    return [[-5, 0], [5, 0], [2, -3], [2, 1]][inDirection]


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


def lrOtherDoubleOffset(inDirection):
    """
    TODO: Return a tuple of two integers instead of a list.
    """
    # print('lrOtherDoubleOffset({})'.format(inDirection), end='')
    return [[-1, -1], [5, -1], [0, 0], [0, 0]][inDirection]


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


def udNoDoublesOffset(inDirection):
    """
    TODO: Return a tuple of two integers instead of a list.
    """
    # print('udNoDoublesOffset({})'.format(inDirection), end='')
    return [[0, 0], [0, 0], [0, -3], [0, 3]][inDirection]


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


def udMeDoubleOffset(inDirection):
    """
    TODO: Return a tuple of two integers instead of a list.
    """
    # print('udMeDoubleOffset({})'.format(inDirection), end='')
    return [[-5, +1], [1, 1], [0, -3], [0, 3]][inDirection]


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


def udOtherDoubleOffset(inDirection):
    """
    TODO: Return a tuple of two integers instead of a list.
    """
    # print('udOtherDoubleOffset({})'.format(inDirection), end='')
    return [[0, 0], [0, 0], [-2, -1], [-2, 3]][inDirection]


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


def oppositeDirection(inDirection) -> int:
    """
    TODO: Dict lookup instead of if-elif-else.
    """
    if inDirection == cLeft:
        return cRight
    if inDirection == cRight:
        return cLeft
    if inDirection == cUp:
        return cDown
    if inDirection == cDown:
        return cUp
    assert True, f"Invalid direction: {inDirection}"


def rightAngles(inDirection) -> list[int]:
    """
    TODO: Return a tuple of two integers instead of a list.
    """
    return [cUp, cDown] if inDirection in {cLeft, cRight} else [cLeft, cRight]


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


def whichDie(inDirection) -> bool:
    return inDirection in {cRight, cDown}


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


class PlayedDomino:
    def __init__(self, inPlayer, inDomino, inNeighbor=None, inDirection=cLeft) -> None:
        self.mPlayer = inPlayer
        self.mDomino = inDomino
        self.mLocation = [0, 0]
        self.mLeftRight = inDirection in {cLeft, cRight}
        if self.isDouble():
            self.mLeftRight = not self.mLeftRight
        if self.mLeftRight:
            self.mOrientation = tk.HORIZONTAL
        else:
            self.mOrientation = tk.VERTICAL
        oppDir = oppositeDirection(inDirection)
        if inNeighbor:  # flip inDomino if required
            matchToDie = inNeighbor.mDomino[whichDie(inDirection)]
            assert matchToDie in self.mDomino, "These dominos do not match!"
            if self.mDomino[whichDie(oppDir)] != matchToDie:
                self.mDomino.reverse()
        self.mNeighbors = [None, None, None, None]
        self.mNeighbors[oppDir] = inNeighbor

    def __str__(self) -> str:
        s = "Domino: {}, isD: {}, pd: {}, fv: {}, pv: {}, Neighbors: {}"
        return s.format(
            self.mDomino,
            self.isDouble(),
            self.playableDirections(),
            self.faceValue(),
            self.playedValue(),
            self.mNeighbors,
        )

    def isDouble(self) -> bool:
        return self.mDomino[0] == self.mDomino[1]

    def faceValue(self) -> int:
        return self.mDomino[0] + self.mDomino[1]

    def numberOfNeighbors(self) -> int:
        return len(self.mNeighbors) - self.mNeighbors.count(None)

    def neighborAsString(self, inDirection) -> str:
        theNeighbor = self.mNeighbors[inDirection]
        if theNeighbor:
            return theNeighbor.mDomino
        return theNeighbor

    def neighborsAsString(self) -> list[str]:
        return [self.neighborAsString(i) for i in range(len(self.mNeighbors))]

    def playedValue(self) -> int:
        neighborCount = self.numberOfNeighbors()
        if neighborCount > 1:  # already boxed in
            return 0
        if self.isDouble() or not neighborCount:  # firstDominoPlayed
            return self.faceValue()
        for i in range(len(self.mNeighbors)):
            if self.mNeighbors[i]:
                return self.mDomino[whichDie(oppositeDirection(i))]
        assert True, "Error in playedValue()!"

    def notifyNeighborsOfUndo(self) -> None:
        """
        Break neighbors' links to me
        """
        for theDirection in range(len(self.mNeighbors)):
            if self.mNeighbors[theDirection]:
                oppDir = oppositeDirection(theDirection)
                # print('Notify Before:', self.mNeighbors[theDirection].neighborsAsString())
                self.mNeighbors[theDirection].mNeighbors[oppDir] = None
                # print(' Notify After:', self.mNeighbors[theDirection].neighborsAsString())

    def playableDirections(self) -> list[int]:
        if self.isDouble():
            return self.playableDirectionsForADouble()
        neighborCount = self.numberOfNeighbors()
        if neighborCount > 1:
            return []
        if not neighborCount:  # firstDominoPlayed
            if self.mLeftRight:
                return [cLeft, cRight]
            else:
                return [cUp, cDown]
        for i in range(len(self.mNeighbors)):
            if self.mNeighbors[i]:
                return [oppositeDirection(i)]
        assert True, "Error in playableDirections()!"

    def playableDirectionsForADouble(self) -> list[int]:
        neighborCount = self.numberOfNeighbors()
        if neighborCount == 4:
            return []
        if neighborCount == 3:
            return [self.mNeighbors.index(None)]
        if neighborCount == 2:
            for i in range(len(self.mNeighbors)):
                if self.mNeighbors[i]:
                    return rightAngles(i)
        if neighborCount == 1:
            for i in range(len(self.mNeighbors)):
                if self.mNeighbors[i]:
                    return [oppositeDirection(i)]
        if not neighborCount:  # firstDominoPlayed
            if self.mLeftRight:
                return rightAngles(cLeft)
            else:
                return rightAngles(cUp)
        assert True, "Error in playableDirectionsForADouble()!"

    def playableNumbers(self) -> list[int]:
        return sorted(
            {self.mDomino[whichDie(dir)] for dir in self.playableDirections()}
        )

    def newNeighbor(self, inPlayer, inDomino) -> object:
        playableDirections = self.playableDirections()
        assert playableDirections
        if self.isDouble():
            theDirection = choice(playableDirections)
        else:
            theDirection = playableDirections[0]
            if len(playableDirections) > 1 and self.mDomino[1] in inDomino:
                theDirection = playableDirections[1]
        d = PlayedDomino(inPlayer, inDomino, self, theDirection)
        self.mNeighbors[theDirection] = d
        # print('newN Older:', self.mDomino, self.neighborsAsString())
        # print('newN Newer:',    d.mDomino,    d.neighborsAsString())
        return d

    def getOffset(self, inDomino, inDirection) -> list[int]:
        if self.mLeftRight:
            if self.isDouble():
                return lrMeDoubleOffset(inDirection)
            elif inDomino.isDouble():
                return lrOtherDoubleOffset(inDirection)
            else:
                return lrNoDoublesOffset(inDirection)
        else:  # noqa: PLR5501
            if self.isDouble():
                return udMeDoubleOffset(inDirection)
            elif inDomino.isDouble():
                return udOtherDoubleOffset(inDirection)
            else:
                return udNoDoublesOffset(inDirection)

    def dominoAndLoc(self) -> str:
        return self.mDomino, "@", self.mLocation

    def dominoAndLocAndNeighbors(self) -> str:
        return self.mDomino, "@", self.mLocation, "n:", self.neighborsAsString()

    def setLocation(self) -> None:
        for i in range(len(self.mNeighbors)):
            theNeighbor = self.mNeighbors[i]
            if theNeighbor and theNeighbor.mLocation:
                oppDir = oppositeDirection(i)
                self.mLocation = theNeighbor.getOffset(self, oppDir)
                self.mLocation[0] += theNeighbor.mLocation[0]
                self.mLocation[1] += theNeighbor.mLocation[1]
                return

    def fillCanvas(self, inCanvas) -> None:
        # print(self.mDomino, '@', self.mLocation, self.neighborsAsString())
        if self.mLeftRight:
            s = str(self.mDomino).replace(" ", "")
            for i in range(len(s)):
                inCanvas[self.mLocation[1]][self.mLocation[0] + i] = s[i]
        else:
            inCanvas[self.mLocation[1] + 0][self.mLocation[0]] = str(self.mDomino[0])
            inCanvas[self.mLocation[1] + 1][self.mLocation[0]] = "-"
            inCanvas[self.mLocation[1] + 2][self.mLocation[0]] = str(self.mDomino[1])


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
