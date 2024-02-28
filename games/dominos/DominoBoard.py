#!/usr/bin/env python3

# from random import shuffle
# from sys import argv
# from askNumberFromOneTo import askNumberFromOneTo
# import tkinter as tk
# from PlayedDomino import printPlayedDominos
from tkDomino import tkDominoBoard


class DominoBoard(tkDominoBoard):
    def __init__(self, inMaxDie=6):
        print(1, self.__class__)
        # print(2, self.super())
        # iprint(3, super(DominoBoard))
        # self.super(DominoBoard, self).__init__()
        # super().__init__()
        self.mMaxDie = inMaxDie
        self.mBoneyard = []
        self.mPlayedDominos = []

    @property
    def value(self):
        return sum(domino.playedValue() for domino in self.mPlayedDominos)

    @property
    def points(self):
        value = self.value
        return 0 if value % 5 else value / 5

    def __str__(self):
        return (
            f"{len(self.mBoneyard)} dominos in the boneyard = {self.mBoneyard}\n"
            f"Playable numbers: {self.playableNumbers()}, value = {self.value}\n"
            f"{self.mPlayedDominos}"
        )

    def pickFromBoneyard(self):
        # not clear what the rule is for other values of self.mMaxDie
        bones_available = len(self.mBoneyard) > (2 if self.mMaxDie == 6 else 0)
        return self.mBoneyard.pop() if bones_available else None

    def playableNumbers(self):
        if not self.mPlayedDominos:
            return range(self.mMaxDie + 1)
        returnValue = []
        for d in self.mPlayedDominos:
            returnValue += d.playableNumbers()
        return sorted(set(returnValue))

    def playableDominos(self, inDomino):
        returnValue = []
        for d in self.mPlayedDominos:
            pn = d.playableNumbers()
            if inDomino[0] in pn or inDomino[1] in pn:
                returnValue.append(d)
        return returnValue

    def isDominoPlayable(self, inDomino):
        if not self.mPlayedDominos:
            return True  # on an empty board, all dominos are playable
        for d in self.mPlayedDominos:
            pn = d.playableNumbers()
            if inDomino[0] in pn or inDomino[1] in pn:
                return True
        return False

    def getFreshCopy(self, inOlderDomino):
        if inOlderDomino in self.mPlayedDominos:
            # print('freshCopy NOT required')
            return inOlderDomino
        print("freshCopy WAS required")
        for d in self.mPlayedDominos:
            if d.mDomino == inOlderDomino.mDomino:
                return d
        assert True

    def setLocations(self):
        if not self.mPlayedDominos:
            return None
        for d in self.mPlayedDominos:
            d.mLocation = None
        self.mPlayedDominos[0].mLocation = [0, 0]
        horiz = []
        verts = []
        for d in self.mPlayedDominos:
            if not d.mLocation:  # for all but firstPlayedDomino
                d.setLocation()
            horiz.append(d.mLocation[0])
            verts.append(d.mLocation[1])
        assert min(horiz) < 1
        assert min(verts) < 1
        hOffset = abs(min(horiz))
        vOffset = abs(min(verts))
        if hOffset or vOffset:
            for d in self.mPlayedDominos:
                d.mLocation[0] += hOffset
                d.mLocation[1] += vOffset
        canvasDimensions = [
            (max(horiz) - min(horiz)) + 5,
            (max(verts) - min(verts)) + 3,
        ]
        return buildCanvas(canvasDimensions)

    def fillCanvas(self, inCanvas):
        for theDomino in self.mPlayedDominos:
            theDomino.fillCanvas(inCanvas)

    def locationList(self):
        return tuple(domino.mLocation for domino in self.mPlayedDominos)

    def printPlayedDominos(self):
        if not self.mPlayedDominos:
            return
        theCanvas = self.setLocations()
        self.fillCanvas(theCanvas)
        printCanvas(theCanvas)
        del theCanvas
        print(f"Playable: {self.playableNumbers()}, Value: {self.value}")


def buildCanvas(inDimensions):
    return [[" "] * (inDimensions[0] + 5) for _ in range(inDimensions[1] + 5)]


def printCanvas(inCanvas):
    theMax = 0
    for theLine in inCanvas:
        theLine = "".join(theLine).rstrip()
        if len(theLine) > theMax:
            theMax = len(theLine)
    border = ("=" * 33)[:theMax]
    print(border)
    for theLine in inCanvas:
        if s := "".join(theLine).rstrip():
            print(s)
    print(border)


if __name__ == "__main__":
    from DominoWorld import main

    main()
