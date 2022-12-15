from __future__ import annotations

from typing import List

from Board import Board
from Player import Player, Team
from ChessPieceGenerator import ChessPieceGenerator
from Helpers import flip_coin, CoinFace


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
        self.turn: Team | None = Team.BLACK if flip_coin() == CoinFace.HEADS else Team.WHITE

    def end_game(self: Game) -> None:
        """
        Ends the game, clearing the board and clearing all player's owned pieces and captured pieces

        :return: None
        """
        self.board.clear()
        self.player_1.clear_pieces()
        self.player_2.clear_pieces()

    def next_turn(self: Game) -> Game:
        self.turn = Team.BLACK if self.turn == Team.WHITE else Team.WHITE
        return self


    def simulate_step(self: Game) -> Game:
        game_clone = self
        #  process whose turn it is, and then make a random guess for the move to make
        if game_clone.turn == Team.White:
            available_moves = []
            current_player = game_clone.player_1 if game_clone.player_1.team == Team.WHITE else game_clone.player_2
            all_valid_potential_moves: List[List[int]] = []
            for each_piece in current_player.pieces:
                all_valid_potential_moves.extend([
                    each_move if self.board.validate_move(each_move[0], each_move[1], current_player.team) else []
                    for each_move in each_piece.generate_potential_moves()
                ])
            #  generated all children of the current state
