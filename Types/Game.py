from __future__ import annotations

from typing import List

from Board import Board
from Player import Player, Team
from ChessPieceGenerator import ChessPieceGenerator
from Helpers import flip_coin, CoinFace
from GameTree import GameTree
from GameTreeNode import GameTreeNode


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

    def simulate_move(self: Game, from_x: int, from_y: int, to_x: int, to_y: int) -> Game:
        """
        Simulate a move from the player currently in session, assume the move is valid. Used for the MCTS

        :param from_x: The x coordinate the piece is being moved from
        :param from_y: The y coordinate the piece is being moved from
        :param to_x: The x coordinate to move to
        :param to_y: The y coordinate to move to
        :return: The modified instance
        """
        if self.board.is_capture(to_x, to_y, self.turn):
            #  is a capture move, then capture
            self.board.capture_piece(to_x, to_y)
            self.board.move_piece(from_x, from_y, to_x, to_y)
        else:
            #  not a capture, just move the piece
            self.board.move_piece(from_x, from_y, to_x, to_y)
        self.next_turn()
        return self

    def playout_game(self: Game) -> Team:
        """
        Randomly chooses moves as the user to play-out the game, until a winner is decided

        :return: The team that one, which will influence the node value
        """
        pass

    def monte_carlo(self: Game) -> Game:
        game_clone = self
        monte_carlo_tree = GameTree().set_root(GameTreeNode(game_clone))
        #  process whose turn it is, and then make a random guess for the move to make
        if game_clone.turn == Team.White:
            current_player = game_clone.player_1 if game_clone.player_1.team == Team.WHITE else game_clone.player_2
            all_valid_potential_moves: List[List[int]] = []
            for each_piece in current_player.pieces:
                all_valid_potential_moves.extend([
                    [each_piece.x, each_piece.y] + each_move
                    if self.board.validate_move(each_move[0], each_move[1], current_player.team)
                    else []
                    for each_move in each_piece.generate_potential_moves()
                ])
            child_game_instances = []
            for each_valid_move in all_valid_potential_moves:
                child_game_instances.append(
                    Game(self.board, self.player_1, self.player_2)
                    .simulate_move(
                        each_valid_move[0],
                        each_valid_move[1],
                        each_valid_move[2],
                        each_valid_move[3]
                    )
                )
            for each_simulated_game in child_game_instances:
                monte_carlo_tree.root.add_child(GameTreeNode(each_simulated_game))
            for each_simulated_game_child in monte_carlo_tree.root.children:
                # randomly play-out each node
                winning_team: Team = each_simulated_game_child.value.playout_game()
                if winning_team == Team.WHITE:
                    # increment the denominator
                    monte_carlo_tree.root.denominator += 1
                else:
                    monte_carlo_tree.root.numerator += 1