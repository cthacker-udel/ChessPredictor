from __future__ import annotations
from Board import Board
from Player import Player
from ChessPieceGenerator import ChessPieceGenerator


class Game:
    """
    Game instance, represents a chess game being played
    """

    def __init__(self: Game, board: Board, player_1: Player, player_2: Player) -> None:
        """
        Initializes a Game instance, which takes in a board, and 2 players, and sets the proper fields to prepare for the game

        :param board: The Board instance
        :param player_1: The Player instance, player 1
        :param player_2: The Player instance, player 2
        """
        self.board: Board = board
        self.player_1: Player = player_1
        self.player_2: Player = player_2
        team_1_generator = ChessPieceGenerator(self.player_1.team)
        team_2_generator = ChessPieceGenerator(self.player_2.team)
        self.player_1.pieces = team_1_generator.generate_initial_pieces()
        self.player_2.pieces = team_2_generator.generate_initial_pieces()

    def end_game(self: Game) -> None:
        """
        Ends the game, clearing the board and clearing all player's owned pieces and captured pieces

        :return: None
        """
        self.board.clear()
        self.player_1.clear_pieces()
        self.player_2.clear_pieces()
