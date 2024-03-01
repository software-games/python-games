#!/usr/bin/env python3

from random import shuffle

import pytest

from games.dominoes.DominoBoard import DominoBoard

# from sys import argv
# from askNumberFromOneTo import askNumberFromOneTo
# from PlayedDomino import PlayedDomino
from games.dominoes.DominoPlayer import DominoPlayer

gPassesInARow = 0


def initDominos(inMaxDie=6) -> list[list[int]]:
    return [[x, y] for x in range(inMaxDie + 1) for y in range(x, inMaxDie + 1)]


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


def pointsRounded(inValue, n=5) -> int:
    return int(round((inValue + n // 2) // n))


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


def ZZpointsRounded(inValue) -> int:
    return inValue / 5 + int(inValue % 5 > 2)


# for i in range(20):
#    print(i, pointsRounded(i), ZZpointsRounded(i))


class DominoWorld:
    def __init__(self, inMaxDie=6, inNumberOfPlayers=2) -> None:
        self.mDominos = initDominos(inMaxDie)
        self.mBoard = DominoBoard(inMaxDie)
        self.mPlayers = []
        for i in range(inNumberOfPlayers):
            theName = f"Player {i}"
            self.mPlayers.append(DominoPlayer(theName, self.mBoard))
        self.mWhoseTurnMajor = 0
        self.mWhoseTurnMinor = 0
        self.mGamesEndingInADraw = 0

    def __str__(self) -> str:
        p = ""
        for thePlayer in self.mPlayers:
            p += str(thePlayer) + "\n"
        return p  # + str(self.mBoard)

    def deal(self, inDominosPerPlayer=7) -> None:
        self.mBoard.mPlayedDominos = []
        shuffle(self.mDominos)
        shuffle(self.mDominos)
        shuffle(self.mDominos)
        # shuffle(shuffle(shuffle(self.mDominos)))
        d = 0  # start with the first domino.
        for thePlayer in self.mPlayers:
            thePlayer.dominos = sorted(self.mDominos[d : d + inDominosPerPlayer])
            d += inDominosPerPlayer
        self.mBoard.mBoneyard = self.mDominos[d:]

    def reorientDominos(self) -> None:
        for d in self.mDominos:
            if d[0] > d[1]:
                d.reverse()

    def playersHaveDominos(self) -> bool:
        return all(thePlayer.dominos for thePlayer in self.mPlayers)

    def playATurn(self) -> None:
        global gPassesInARow
        p = self.mWhoseTurnMinor % len(self.mPlayers)
        # print(f"playATurn: {self.mWhoseTurnMinor} {p}")
        print(f"{'=' * 10} NEW TURN {'=' * 10}")
        if self.mPlayers[p].playATurn():
            gPassesInARow = 0
        else:
            gPassesInARow += 1
        if gPassesInARow > 1:
            for p in self.mPlayers:
                p.dominos = []
        self.mWhoseTurnMinor += 1

    def playAHand(self) -> None:
        self.mWhoseTurnMinor = self.mWhoseTurnMajor
        self.mWhoseTurnMajor += 1
        self.deal()
        # print(self)
        while self.playersHaveDominos():
            self.playATurn()
        totalValue = 0
        for p in self.mPlayers:
            handValue = p.points_still_holding()
            totalValue += handValue
            if handValue:
                print(p.hand_as_str(), "still holds", handValue, "...", end="")
        for p in self.mPlayers:
            if not p.dominos:  # the player that won
                p.award_points(pointsRounded(totalValue))
                p.hands_won += 1
                break
        print()
        theWinner = self.checkForWinner()
        if theWinner and theWinner != -1:
            print(f"{'=' * 10} NEW HAND {'=' * 10}")

    def playAGame(self, inHumanWantsToPlay) -> str:
        self.mPlayers[0].is_player_human = inHumanWantsToPlay
        # self.mBoard.clearBoard()
        theWinner = None
        while not theWinner:
            self.playAHand()
            self.reorientDominos()
            theWinner = self.checkForWinner()
        if theWinner == -1:
            self.mGamesEndingInADraw += 1
            theWinner = None
        if inHumanWantsToPlay:
            print(self)
        # if theWinner:
        #    for thePlayer in self.mPlayers:
        #        if theWinner == thePlayer.mName:
        #            thePlayer.mGamesWon += 1
        print("The winner is", theWinner)
        return theWinner

    def highestScore(self) -> int:
        highScore = 0
        for p in self.mPlayers:
            if p.points > highScore:
                highScore = p.points
        return highScore

    def checkForWinner(self) -> str:
        highScore = self.highestScore()
        if highScore < 25:
            return None
        for p in self.mPlayers:
            if p.points == highScore:
                return p.name


def main() -> None:
    print("Enter 1 to play 100 computer vs. computer games.")
    print("Enter 2 to play 1 human vs. computer game.")
    i = 2  # askNumberFromOneTo(2)
    humanWantsToPlay = i != 1
    if not i:
        i = 100
    dw = DominoWorld()
    while i:
        i -= 1
        dw.playAGame(humanWantsToPlay)
    print("=" * 10)
    print(dw)

    # dw = DominoWorld()
    # print(dw)
    # print('==========')
    # dw.playAGame(True)
    # while dw.highestScore() < 25:
    #    print('Spining the bones...')
    # dw.playAHand()
    # dw.reorientDominos()
    # print('==========')
    # print(dw)


if __name__ == "__main__":
    main()
