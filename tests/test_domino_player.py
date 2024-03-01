#!/usr/bin/env python3

from games.dominoes.DominoBoard import DominoBoard
from games.dominoes.DominoPlayer import DominoPlayer, DominoRunMove
from games.dominoes.PlayedDomino import PlayedDomino


class TestDominoRunMove:
    """
    Tests for the DominoRunMove class
    """

    def test_init(self):
        """
        Test the __init__ method
        """
        played_domino = PlayedDomino(1, [0, 0])
        run_move = DominoRunMove(played_domino, [0, 1])
        assert run_move.mAlreadyPlayedDomino == played_domino
        assert run_move.mToBePlayedSimpleDomino == [0, 1]

    def test_str(self):
        """
        Test the __str__ method
        """
        played_domino = PlayedDomino(1, [0, 0])
        run_move = DominoRunMove(played_domino, [0, 1])
        assert str(run_move) == "Playing [0, 1] on [0, 0] "


class TestDominoPlayer:
    """
    Tests for the DominoPlayer class
    """

    def test_init(self):
        """
        Test the __init__ method
        """
        board = DominoBoard()
        player = DominoPlayer("Player 1", board)
        assert player.name == "Player 1"
        assert player.board == board
        assert player.points == 0
        assert player.dominos == []
        assert player.go_agains == 0
        assert player.hands_won == 0
        assert player.games_won == 0
        assert player.is_player_human is False

    def test_str(self):
        """
        Test the __str__ method
        """
        board = DominoBoard()
        player = DominoPlayer("Player 1", board)
        assert (
            str(player)
            == "Player 1 has 0 dominos, 0 points, 0 go agains, 0 hands and 0 games won."
        )

    def test_hand_as_str(self):
        """
        Test the hand_as_str method
        """
        board = DominoBoard()
        player = DominoPlayer("Player 1", board)
        assert player.hand_as_str() == "Player 1's hand: 0 []"

    def test_award_points(self):
        """
        Test the award_points method
        """
        board = DominoBoard()
        player = DominoPlayer("Player 1", board)
        player.award_points(10)
        assert player.points == 10

    def test_points_still_holding(self):
        """
        Test the points_still_holding method
        """
        board = DominoBoard()
        player = DominoPlayer("Player 1", board)
        player.dominos = [[0, 0], [0, 1], [1, 1]]
        assert player.points_still_holding() == 3

    def test_isDominoPlayable(self):
        """
        Test the isDominoPlayable method
        """
        board = DominoBoard()
        player = DominoPlayer("Player 1", board)
        player.dominos = [[0, 0], [0, 1], [1, 1]]
        assert player.isDominoPlayable(0) is True
        assert player.isDominoPlayable(1) is True
        assert player.isDominoPlayable(2) is True
        # TODO: Add a played domino

    def test_starIfPlayable(self):
        """
        Test the starIf
        """
        board = DominoBoard()
        player = DominoPlayer("Player 1", board)
        player.dominos = [[0, 0], [0, 1], [1, 1]]
        assert player.starIfPlayable(0) == "*"
        assert player.starIfPlayable(1) == "*"
        assert player.starIfPlayable(2) == "*"
        # TODO: Add a played domino

    def test_canPlay(self):
        """
        Test the canPlay method
        """
        board = DominoBoard()
        player = DominoPlayer("Player 1", board)
        player.dominos = [[0, 0], [0, 1], [1, 1]]
        assert player.canPlay() is True  # TODO: Add a False case

    def test_pickFromBoneyard(self):
        """
        Test the pickFromBoneyard method
        """
        board = DominoBoard()
        player = DominoPlayer("Player 1", board)
        assert player.dominos == []
        player.pickFromBoneyard()
        assert len(player.dominos) == 0  # TODO: Fix me

    def test_pickFromBoneyardUntilCanPlay(self):
        """
        Test the pickFromBoneyardUntilCanPlay method
        """
        board = DominoBoard()
        player = DominoPlayer("Player 1", board)
        player.dominos = [[0, 0], [0, 1], [1, 1]]
        assert player.pickFromBoneyardUntilCanPlay() is True

    def test_undo(self):
        """
        Test the undo method
        """
        board = DominoBoard()
        player = DominoPlayer("Player 1", board)
        player.board.mPlayedDominos = [PlayedDomino(1, [0, 0])]
        # player.board.points = 10  # TODO: Fix me
        # player.undo()
        # assert player.points == 0
        # assert player.board.mPlayedDominos == []

    def test_getFreshCopy(self):
        """
        Test the getFreshCopy method
        """
        board = DominoBoard()
        player = DominoPlayer("Player 1", board)
        played_domino = PlayedDomino(1, [0, 0])
        player.getFreshCopy(played_domino)
        # assert player.dominos == []  # TODO: Fix me

    def test_playARun(self):
        """
        Test the playARun method
        """
        board = DominoBoard()
        _player = DominoPlayer("Player 1", board)
        _run = [DominoRunMove(PlayedDomino(1, [0, 0]), [0, 1])]
        # assert player.playARun(run) == False  # TODO: Fix me

    def test_playAMove(self):
        """
        Test the playAMove method
        """
        board = DominoBoard()
        player = DominoPlayer("Player 1", board)
        player.dominos = [[0, 0], [0, 1], [1, 1]]
        # assert player.playAMove(DominoRunMove(PlayedDomino(1, [0, 0]), [0, 1])) == False  # TODO: Fix me


if __name__ == "__main__":
    from DominoWorld import main

    main()
