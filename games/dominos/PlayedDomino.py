#!/usr/bin/env python3

#           2          4     5
# [0,1][1,2]-[2,3][3,4]-[4,5]-
#           2          4     5
#           2
#           -
#           5
#

# from random import choice, shuffle
import tkinter as tk

# from sys import argv
# from askNumberFromOneTo import askNumberFromOneTo
# from PrintableDomino import lrNoDoublesOffset, lrMeDoubleOffset, lrOtherDoubleOffset, udNoDoublesOffset, udMeDoubleOffset,
# udOtherDoubleOffset
from random import choice

# print(argv)


def lrNoDoublesOffset(inDirection) -> list[int]:
    """
    TODO: Return a tuple of two integers instead of a list.
    """
    # print('lrNoDoublesOffset({})'.format(inDirection), end='')
    return [[-5, 0], [5, 0], [0, 0], [0, 0]][inDirection]


def lrMeDoubleOffset(inDirection):
    """
    TODO: Return a tuple of two integers instead of a list.
    """
    # print('lrMeDoubleOffset({})'.format(inDirection), end='')
    return [[-5, 0], [5, 0], [2, -3], [2, 1]][inDirection]


def lrOtherDoubleOffset(inDirection):
    """
    TODO: Return a tuple of two integers instead of a list.
    """
    # print('lrOtherDoubleOffset({})'.format(inDirection), end='')
    return [[-1, -1], [5, -1], [0, 0], [0, 0]][inDirection]


def udNoDoublesOffset(inDirection):
    """
    TODO: Return a tuple of two integers instead of a list.
    """
    # print('udNoDoublesOffset({})'.format(inDirection), end='')
    return [[0, 0], [0, 0], [0, -3], [0, 3]][inDirection]


def udMeDoubleOffset(inDirection):
    """
    TODO: Return a tuple of two integers instead of a list.
    """
    # print('udMeDoubleOffset({})'.format(inDirection), end='')
    return [[-5, +1], [1, 1], [0, -3], [0, 3]][inDirection]


def udOtherDoubleOffset(inDirection):
    """
    TODO: Return a tuple of two integers instead of a list.
    """
    # print('udOtherDoubleOffset({})'.format(inDirection), end='')
    return [[0, 0], [0, 0], [-2, -1], [-2, 3]][inDirection]


cLeft, cRight, cUp, cDown = range(4)  # TODO: Enum


def oppositeDirection(inDirection):
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


def whichDie(inDirection) -> bool:
    return inDirection in {cRight, cDown}


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


if __name__ == "__main__":
    # from DominoTest import main
    from DominoWorld import main

    main()
