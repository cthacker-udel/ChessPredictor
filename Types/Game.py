from __future__ import annotations

import random
from typing import List

from Board import Board
from Player import Player, Team
from ChessPieceGenerator import ChessPieceGenerator
from Helpers import flip_coin, CoinFace
from GameTree import GameTree
from GameTreeNode import GameTreeNode
from King import King
from ChessPiece import ChessPiece


def is_in_kings_space(king: King, piece: ChessPiece) -> List[bool, List[int]]:
    """
    Checks if the piece supplied to the function is occupying any space the king can potentially move to

    :param king: The king instance
    :param piece: The piece to move
    :return: Whether the piece passed in occupies any of the king's potential moving spaces
    """
    is_left = piece.x == king.x - 1
    is_right = piece.x == king.x + 1
    is_top = piece.y == king.y - 1
    is_bottom = piece.y == king.y + 1
    is_top_left = piece.x == king.x - 1 and piece.y == king.y - 1
    is_top_right = piece.x == king.x + 1 and piece.y == king.y - 1
    is_bottom_left = piece.x == king.x - 1 and piece.y == king.y + 1
    is_bottom_right = piece.x == king.x + 1 and piece.y == king.y + 1
    if is_left or is_right or is_top or is_bottom or is_top_left or is_top_right or is_bottom_left or is_bottom_right:
        return [True, [piece.x, piece.y]]
    return [False, []]


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

        :return: The player that won
        """
        # we check if either player is in checkmate, if not, we make a random move from the list of available moves
        # the player can make
        current_player = None
        while not self.is_checkmate():
            current_player = self.player_1 if self.turn == Team.WHITE and self.player_1.team == Team.WHITE else self.player_2
            all_valid_potential_moves: List[List[int]] = []
            for each_piece in current_player.pieces:
                all_valid_potential_moves.extend([
                    [each_piece.x, each_piece.y] + each_move
                    if self.board.validate_move(each_move[0], each_move[1], current_player.team)
                    else []
                    for each_move in each_piece.generate_potential_moves()
                ])
            random_move_choice = random.choice(all_valid_potential_moves)
            self.simulate_move(random_move_choice[0], random_move_choice[1], random_move_choice[2], random_move_choice[3])
            self.next_turn()
        return current_player.team

    def is_checkmate(self: Game) -> bool:  # O(N) + O(MK + MJ) --> O(N + MK + MJ)
        """
        - **O(N + MK + MJ)**

        - N being the # of pieces the current_player has
        - M being the # of pieces the opposing player has
        - K being the # of potential moves from each piece
        - J being the # of valid moves from the generated potential moves

        We take each piece the current player owns, and check if any one of their pieces covers all
        potential spots the king can move to. The issue arises with these cases: What happens if the king has
        pawns/pieces either above or below them that can't move therefore we don't need to be checking that area. What
        happens when the king can possibly move to get out of a situation (that's covered with the X's) But the thing is
        though, is that the other player cannot move a piece at all, can only move the king, so what we have to do is
        say what spaces are already occupied around the king, mark those as X as well, since we can't move there.
        That's the solution.

        :return: Whether the opposing player is in checkmate
        """

        # Assign N the # of pieces the current_player has, and M the # of the pieces the opposing_player has,
        # the runtime analyses provided below reference those variables

        curr_player = self.player_1 if self.turn == Team.WHITE and self.player_1.team == Team.WHITE else self.player_2
        # set opposing player
        opposing_player = self.player_2 if curr_player == self.player_1 else self.player_1
        # find king from player
        found_king: King | None = None
        for each_piece in curr_player.pieces:  # O(n)
            if each_piece.name == "King":
                #  piece is a king
                found_king = each_piece
                break
        # found the king, now we map out all potential moves from the player, marking their movements on a board
        # if the king is surrounded, then the player has checkmate.
        mock_board: List[List[ChessPiece | str | None]] = [
            [None if i != found_king.y and j != found_king.x else found_king for i in range(self.board.width) for j in
             range(self.board.height)]]
        # check if any pieces surround the king, then mark that as X
        for each_piece in opposing_player.pieces:  # O(m)
            if found_king is not None:
                is_in_king_space: List[bool, List[int]] = is_in_kings_space(found_king, each_piece)
                if is_in_king_space[0]:
                    mock_board[is_in_king_space[1][1]][is_in_king_space[1][0]] = 'O'
        #  analyze all pieces movements, marking all areas they can strike with an 'X'
        for each_piece in opposing_player.pieces:  # O(M*(K + J)) --> O(MK + MJ)
            all_potential_moves: List[List[int]] = each_piece.generate_potential_moves()  # K potential moves
            all_valid_moves: List[List[int]] = []
            for each_potential_move in all_potential_moves:
                if self.board.validate_move(each_potential_move[0], each_potential_move[1], opposing_player.team):
                    all_valid_moves.append(
                        each_potential_move
                    )
            for each_valid_move in all_valid_moves:  # J valid moves
                # mark the coordinate with an 'X', unless it's the king's spot
                if each_valid_move[1] != found_king.y and each_valid_move[0] != found_king.x:
                    if mock_board[each_valid_move[1]][each_valid_move[0]] != 'O':
                        mock_board[each_valid_move[1]][each_valid_move[0]] = 'X'
            left, right, top, bottom, top_left, top_right, bottom_left, bottom_right = False, False, False, False, False, False, False, False
            left_coord = [found_king.x - 1, found_king.y]
            right_coord = [found_king.x + 1, found_king.y]
            top_coord = [found_king.x, found_king.y - 1]
            bottom_coord = [found_king.x, found_king.y + 1]
            top_left_coord = [found_king.x - 1, found_king.y - 1]
            top_right_coord = [found_king.x + 1, found_king.y - 1]
            bottom_left_coord = [found_king.x - 1, found_king.y + 1]
            bottom_right_coord = [found_king.x + 1, found_king.y + 1]

            if found_king.x > 0:
                left = mock_board[left_coord[1]][left_coord[0]] in ['XO']
            if found_king.x < self.board.width:
                right = mock_board[right_coord[1]][right_coord[0]] in ['XO']
            if found_king.y > 0:
                top = mock_board[top_coord[1]][top_coord[0]] in ['XO']
            if found_king.y < self.board.height:
                bottom = mock_board[bottom_coord[1]][bottom_coord[0]] in ['XO']
            if found_king.y > 0 and found_king.x > 0:
                top_left = mock_board[top_left_coord[1]][top_left_coord[0]] in ['XO']
            if found_king.y < self.board.height and found_king.x < self.board.width:
                top_right = mock_board[top_right_coord[1]][top_right_coord[0]] in ['XO']
            if found_king.y < self.board.height and found_king.x > 0:
                bottom_left = mock_board[bottom_left_coord[1]][bottom_left_coord[0]]
            if found_king.y < self.board.height and found_king.x < self.board.width:
                bottom_right = mock_board[bottom_right_coord[1]][bottom_right_coord[0]] in ['XO']

            if left and right and top and bottom and top_left and top_right and bottom_left and bottom_right:
                return True
            #  clear all X's surrounding king
            if mock_board[left_coord[1]][left_coord[0]] == 'X':
                mock_board[left_coord[1]][left_coord[0]] = None
            if mock_board[right_coord[1]][right_coord[0]] == 'X':
                mock_board[right_coord[1]][right_coord[0]] = None
            if mock_board[top_coord[1]][top_coord[0]] == 'X':
                mock_board[top_coord[1]][top_coord[0]] = None
            if mock_board[bottom_coord[1]][bottom_coord[0]] == 'X':
                mock_board[bottom_coord[1]][bottom_coord[0]] = None
            if mock_board[top_left_coord[1]][top_left_coord[0]] == 'X':
                mock_board[top_left_coord[1]][top_left_coord[0]] = None
            if mock_board[top_right_coord[1]][top_right_coord[0]] == 'X':
                mock_board[top_right_coord[1]][top_right_coord[0]] = None
            if mock_board[bottom_left_coord[1]][bottom_left_coord[0]] == 'X':
                mock_board[bottom_left_coord[1]][bottom_left_coord[0]] = None
            if mock_board[bottom_right_coord[1]][bottom_right_coord[0]] == 'X':
                mock_board[bottom_right_coord[1]][bottom_right_coord[0]] = None

        return False

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
