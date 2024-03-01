#!/usr/bin/env python3

from __future__ import annotations

from games.dominoes.ask_number_from_one_to import askNumberFromOneTo
from games.dominoes.domino_board import DominoBoard
from games.dominoes.played_domino import PlayedDomino


class DominoRunMove:
    def __init__(
        self, inAlreadyPlayedDomino, inToBePlayedSimpleDomino, points=0
    ) -> None:
        self.mAlreadyPlayedDomino = inAlreadyPlayedDomino
        self.mToBePlayedSimpleDomino = inToBePlayedSimpleDomino
        self.points = points

    def __str__(self) -> str:
        theMessage = ""
        if self.points:
            theMessage = f"{self.points} points, go again..."
        elif self.mToBePlayedSimpleDomino[0] == self.mToBePlayedSimpleDomino[1]:
            theMessage = "is a double, go again..."
        s = f"Playing {self.mToBePlayedSimpleDomino}"
        if not self.mAlreadyPlayedDomino:
            return f"{s} as firstPlayedDomino {theMessage}"
        return f"{s} on {self.mAlreadyPlayedDomino.mDomino} {theMessage}"


class DominoPlayer:
    def __init__(self, name: str, board: DominoBoard) -> None:
        self.name = name
        self.board = board
        self.points = 0
        self.dominos = []
        self.go_agains = 0
        self.hands_won = 0
        self.games_won = 0
        self.is_player_human = False  # assume humans are not interested in playing
        # self.is_player_human = True

    def __str__(self) -> str:
        s = "{} has {} dominos, {} points, {} go agains, {} hands and {} games won."
        return s.format(
            self.name,
            len(self.dominos),
            self.points,
            self.go_agains,
            self.hands_won,
            self.games_won,
        )

    def hand_as_str(self) -> str:
        return f"{self.name}'s hand: {len(self.dominos)} {self.dominos}"

    def award_points(self, points) -> None:
        if not points:
            return
        old_points = self.points
        self.points += points
        print(
            f"Awarding {points} points to {self.name} from {old_points} --> {self.points}."
        )

    def points_still_holding(self) -> int:
        returnValue = 0
        for d in self.dominos:
            returnValue += d[0] + d[1]
        assert sum(sum(domino) for domino in self.dominos) == returnValue
        return returnValue

    def isDominoPlayable(self, inIndex) -> bool:
        return self.board.isDominoPlayable(self.dominos[inIndex])

    def starIfPlayable(self, inIndex) -> str:
        return "*" if self.isDominoPlayable(inIndex) else ""

    def canPlay(self) -> bool:
        """
        If False, then this player must pick from the boneyard.
        """
        return any(self.isDominoPlayable(i) for i in range(len(self.dominos)))

    def pickFromBoneyard(self) -> list | None:
        print("Going to the boneyard... ", end="")
        theDomino = self.board.pickFromBoneyard()
        if not theDomino:
            print("EMPTY!! Passing to next player.")
            assert True  # ---------*
            return None  # TODO: Return [] instead of None
        self.dominos.append(theDomino)
        print("Got:", theDomino)
        return theDomino

    def pickFromBoneyardUntilCanPlay(self):
        while not self.canPlay():
            if not self.pickFromBoneyard():
                return False  # Can not play and boneyard is empty
        return True  # Can play

    def undo(self) -> None:  # "A domino laid is a domino played." -- anon
        if not self.board.mPlayedDominos:
            print("Nothing to undo.")
            return
        if (thePlayer := self.board.mPlayedDominos[-1].mPlayer) != self:
            print("Can not undo the move of", thePlayer.name)
            return
        self.points -= self.board.points
        theDomino = self.board.mPlayedDominos.pop()
        theDomino.notifyNeighborsOfUndo()
        self.dominos.append(theDomino.mDomino)

    def getFreshCopy(self, inOlderDomino) -> PlayedDomino:
        return self.board.getFreshCopy(inOlderDomino)

    def printARun(self, inRun) -> None:  # a list of DominoRunMoves
        """
        TODO: Return a string instead of printing
        """
        print("playARun() run length:", len(inRun))
        for i in range(len(inRun)):
            print(i + 1, inRun[i])

    def playARun(self, inRun: list[int, list[list[int]]]) -> bool:
        self.printARun(inRun)
        movesPlayed = 0
        for theMove in inRun:
            goAgain = self.playAMove(theMove)
            print(self.hand_as_str())
            self.board.printPlayedDominos()
            movesPlayed += 1
            if not goAgain:
                break
        s = "ERROR: movesPlayed {} does not match len(inRun) {}"
        assert movesPlayed == len(inRun), s.format(movesPlayed, len(inRun))
        print("RECAP:", end="")
        self.printARun(inRun)
        return goAgain

    def playAMove(self, inMove: list[list[int]]) -> bool:
        # print(inMove)
        assert inMove
        newerDomino = inMove.mToBePlayedSimpleDomino
        newerDomino = self.dominos.pop(self.dominos.index(newerDomino))
        if olderDomino := inMove.mAlreadyPlayedDomino:
            olderDomino = self.getFreshCopy(olderDomino)  # the toughest bug to find!!
            theDomino = olderDomino.newNeighbor(self, newerDomino)
        else:  # firstPlayedDomino
            theDomino = PlayedDomino(self, newerDomino)
        self.board.mPlayedDominos.append(theDomino)
        thePoints = self.board.points
        self.award_points(thePoints)
        go_again = thePoints or theDomino.isDouble()
        if go_again:
            self.go_agains += 1
        return go_again

    def playATurn(self) -> bool:  # returns wasAbleToPlay
        print(self)
        self.board.printPlayedDominos()
        if not self.pickFromBoneyardUntilCanPlay():
            print("Pass!!!")
            return False  # unable to play, passing to next player
        if self.is_player_human:
            go_again = self.playATurnHumanPlayer()
        else:
            go_again = self.playATurnComputerPlayer()
        if go_again:
            print("Go again.")
            return self.playATurn()
        print(self)
        return True  # was able to play

    # ===== Human player routines

    # class DominoHumanPlayer(DominoPlayer):
    def playATurnHumanPlayer(self) -> list[list[int]]:
        newerDomino = self.dominos[self.askWhichDominoToPlay()]
        olderDomino = self.askWhereToPlay(newerDomino)
        return self.playAMove(DominoRunMove(olderDomino, newerDomino))

    def askWhichDominoToPlay(self, inPrint=True) -> int:
        # playable = self.board.playableNumbers()
        theMax = len(self.dominos)
        if inPrint:
            for i in range(theMax):
                print(f"{i + 1}: {self.dominos[i]} {self.starIfPlayable(i)}")
            print(self.name, "which domino would you like to play?")
        whichDomino = askNumberFromOneTo(theMax)
        print("Got:", whichDomino)
        if str(whichDomino)[0] == "u":
            self.undo()
            return self.askWhichDominoToPlay()
        whichDomino -= 1  # askNumber is 1 thru 7 but dominos are 0 thru 6
        if not self.isDominoPlayable(whichDomino):
            print(f"Can not play {self.dominos[whichDomino]}!")
            return self.askWhichDominoToPlay(False)
        return whichDomino

    def askWhereToPlay(self, inDominoToPlay) -> PlayedDomino | None:
        if not self.board.mPlayedDominos:
            return None  # firstDominoPlayed has no neighbors
        potentialNeighbors = self.board.playableDominos(inDominoToPlay)
        assert potentialNeighbors
        if len(potentialNeighbors) == 1:
            return potentialNeighbors[0]
        print(f"Connect {inDominoToPlay}: to which domino?")
        theMax = len(potentialNeighbors)
        for i in range(theMax):
            print(f"{i + 1}: {potentialNeighbors[i].mDomino}")
        return potentialNeighbors[askNumberFromOneTo(theMax) - 1]

    # ===== Computer player routines

    # class DominoComputerPlayer(DominoPlayer):
    def playATurnComputerPlayer(self):
        # print(self)
        print(self.hand_as_str())
        # print('Playable: {}, Value: {}'.format(playable, self.board.value))
        theScoreAndRun = self.bestRun()
        return self.playARun(theScoreAndRun[1])  # just theRun

    def bestRun(self) -> list[int, list[list[int]]]:
        """
        Return the most valuable of an exhaustive series of lists of DominoRunMoves
        """
        if not self.dominos:
            # going out with goAgain more valuable than not goAgain
            return [12, []]
        bestScoreAndRun = [0, []]  # theRun is a list of DominoRunMoves
        self.dominos.sort()  # maintain list order across calls to pop() & append()
        for i in range(len(self.dominos)):
            if self.isDominoPlayable(i):
                d = self.dominos.pop(i)
                theScoreAndRun = self.bestRunForDomino(d)
                if theScoreAndRun[0] > bestScoreAndRun[0]:
                    bestScoreAndRun = theScoreAndRun
                self.dominos.append(d)
                self.dominos.sort()  # pop()/append() will mess up list order
        # print('bestRun:', bestScoreAndRun)
        return bestScoreAndRun

    def bestRunForDominoOnEmptyBoard(self, inDomino):
        theKeepers = [[0, 0], [0, 5], [5, 0], [5, 5]]
        if inDomino in theKeepers:
            return [0, []]  # do not waste theKeepers on an empty board
        bestScoreAndRun = [0, []]  # theRun is a list of DominoRunMoves
        theScoreAndRun = self.bestRunForDominoAndNeighbor(inDomino, None)
        if theScoreAndRun[0] > bestScoreAndRun[0]:
            bestScoreAndRun = theScoreAndRun
        return bestScoreAndRun

    def bestRunForDomino(self, inDomino):
        if not self.board.mPlayedDominos:
            return self.bestRunForDominoOnEmptyBoard(inDomino)
        bestScoreAndRun = [0, []]  # theRun is a list of DominoRunMoves
        potentialNeighbors = self.board.playableDominos(inDomino)
        for theNeighbor in potentialNeighbors:
            theScoreAndRun = self.bestRunForDominoAndNeighbor(inDomino, theNeighbor)
            if theScoreAndRun[0] > bestScoreAndRun[0]:
                bestScoreAndRun = theScoreAndRun
        return bestScoreAndRun

    def calcRunScore(self):  # (points, inNumberOfDominosPlayed, inFaceValue)
        # the 12 values goAgain above a high faceValue
        return self.board.points * 1000 + 12 + self.board.mPlayedDominos[-1].faceValue()

    def bestRunForDominoAndNeighbor(self, inDomino, inNeighbor):
        if inNeighbor:
            theDomino = inNeighbor.newNeighbor(self, inDomino)
        else:
            theDomino = PlayedDomino(self, inDomino)
        bestScoreAndRun = [0, []]  # theRun is a list of DominoRunMoves
        self.board.mPlayedDominos.append(theDomino)
        theScore = self.calcRunScore()
        theRun = [DominoRunMove(inNeighbor, inDomino, self.board.points)]
        if theScore > bestScoreAndRun[0]:
            bestScoreAndRun = [theScore, theRun]
        if theDomino.isDouble() or self.board.points:
            theScoreAndRun = self.bestRun()  # go again
            theScoreAndRun[0] += theScore
            if theScoreAndRun[0] > bestScoreAndRun[0]:
                bestScoreAndRun[0] = theScoreAndRun[0]
                bestScoreAndRun[1] = theRun + theScoreAndRun[1]
        self.board.mPlayedDominos.pop().notifyNeighborsOfUndo()
        return bestScoreAndRun


if __name__ == "__main__":
    from DominoWorld import main

    main()
