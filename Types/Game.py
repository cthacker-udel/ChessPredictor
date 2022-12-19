from __future__ import annotations

import random
from copy import deepcopy
from typing import List, TYPE_CHECKING
from Types.ChessPieceGenerator import ChessPieceGenerator
from Types.Helpers import flip_coin, CoinFace
from Types.Player import Team, Player
from Types.GameTree import GameTree
from Types.GameTreeNode import GameTreeNode
import time

if TYPE_CHECKING:
    from Types.Board import Board
    from Types.Player import Player
    from Types.King import King
    from Types.ChessPiece import ChessPiece


class Game:
    """
    Game instance, represents a chess game being played
    """

    def __init__(self: Game, board: Board, player_1: Player, player_2: Player, turn: Team = None) -> None:
        """
        Initializes a Game instance, which takes in a board, and 2 players, and sets the proper fields to prepare for the game

        :param board: The Board instance
        :param player_1: The Player instance, player 1
        :param player_2: The Player instance, player 2
        """
        self.board: Board = deepcopy(board)

        if not turn:
            self.board.player_one = deepcopy(player_1)
            self.board.player_two = deepcopy(player_2)

            self.player_1: Player = self.board.player_one
            self.player_2: Player = self.board.player_two
            team_1_generator = ChessPieceGenerator(self.player_1.team)
            team_2_generator = ChessPieceGenerator(self.player_2.team)
            self.player_1.pieces = team_1_generator.generate_initial_pieces()
            self.player_2.pieces = team_2_generator.generate_initial_pieces()
            self.board.player_one = self.player_1
            self.board.player_two = self.player_2
            self.board.set_board(self.board.player_one, self.board.player_two)
            self.turn: Team | None = Team.BLACK if flip_coin() == CoinFace.HEADS else Team.WHITE
        else:
            self.turn = turn
            self.board.player_one = deepcopy(player_1)
            self.board.player_two = deepcopy(player_2)
            self.player_1 = self.board.player_one
            self.player_2 = self.board.player_two

            self.board.player_one.pieces = []
            self.board.player_two.pieces = []
            self.player_1.pieces = []
            self.player_2.pieces = []
            for i in range(self.board.height):
                for j in range(self.board.width):
                    if self.board.board[i][j] is not None and self.board.board[i][j].team == self.board.player_one.team:
                        self.player_1.pieces.append(self.board.board[i][j])
                    elif self.board.board[i][j] is not None and self.board.board[i][j].team == self.board.player_two.team:
                        self.player_2.pieces.append(self.board.board[i][j])
            self.board.player_one.pieces = self.player_1.pieces[:]
            self.board.player_two.pieces = self.player_2.pieces[:]

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

    def simulate_move(self: Game, from_x: int, from_y: int, to_x: int, to_y: int, team: Team) -> Game:
        """
        Simulate a move from the player currently in session, assume the move is valid. Used for the MCTS

        :param from_x: The x coordinate the piece is being moved from
        :param from_y: The y coordinate the piece is being moved from
        :param to_x: The x coordinate to move to
        :param to_y: The y coordinate to move to
        :param team: The team executing the move
        :return: The modified instance
        """
        self.board.move_piece(from_x, from_y, to_x, to_y, team)
        self.next_turn()
        return self

    def playout_game(self: Game) -> Team:
        """
        Randomly chooses moves as the user to play-out the game, until a winner is decided

        :return: The player that won
        """
        # we check if either player is in checkmate, if not, we make a random move from the list of available moves
        # the player can make
        current_player: Player | None = None
        total_moves: int = 0
        while not self.is_checkmate():
            current_player: Player = self.player_1 if self.turn == Team.WHITE and self.player_1.team == Team.WHITE else self.player_2
            all_valid_potential_moves: List[List[int]] = []
            for each_piece in current_player.pieces:
                all_valid_potential_moves.extend([
                    [each_piece.x, each_piece.y] + each_move
                    if self.board.validate_move(each_move[0], each_move[1], current_player.team)
                    else []
                    for each_move in each_piece.generate_potential_moves(self.board)
                ])
            all_valid_potential_moves = list(filter(lambda x: len(x) > 0, all_valid_potential_moves))
            all_valid_capture_moves = list(filter(lambda x: self.board.is_capture(x[2], x[3], current_player.team), all_valid_potential_moves))
            random_move_choice: List[int] | None = None
            #  print("# potential {}  |  # of capture {}".format(len(all_valid_potential_moves), len(all_valid_capture_moves)))
            if len(all_valid_potential_moves) == 0 and len(all_valid_capture_moves) == 0:
                self.board.print_board()
                for each_piece in current_player.pieces:
                    all_valid_potential_moves.extend([
                        [each_piece.x, each_piece.y] + each_move
                        if self.board.validate_move(each_move[0], each_move[1], current_player.team)
                        else []
                        for each_move in each_piece.generate_potential_moves(self.board)
                    ])
            if len(all_valid_capture_moves) > 0:
                random_move_choice = random.choice(all_valid_capture_moves)
            else:
                random_move_choice = random.choice(all_valid_potential_moves)

            self.simulate_move(random_move_choice[0], random_move_choice[1], random_move_choice[2],
                               random_move_choice[3], current_player.team)
            #  self.board.print_board()
            total_moves += 1
            #  print("Total Moves {}".format(total_moves))
        return current_player.team

    def is_in_kings_space(self: Game, king: King, piece: ChessPiece) -> List[bool, List[int]]:
        """
        Checks if the piece supplied to the function is occupying any space the king can potentially move to

        :param king: The king instance
        :param piece: The piece to move
        :return: Whether the piece passed in occupies any of the king's potential moving spaces
        """
        is_left = piece.x == king.x - 1 and piece.y == king.y
        is_right = piece.x == king.x + 1 and piece.y == king.y
        is_top = piece.y == king.y - 1 and piece.x == king.x
        is_bottom = piece.y == king.y + 1 and piece.x == king.x
        is_top_left = piece.x == king.x - 1 and piece.y == king.y - 1
        is_top_right = piece.x == king.x + 1 and piece.y == king.y - 1
        is_bottom_left = piece.x == king.x - 1 and piece.y == king.y + 1
        is_bottom_right = piece.x == king.x + 1 and piece.y == king.y + 1
        if is_left or is_right or is_top or is_bottom or is_top_left or is_top_right or is_bottom_left or is_bottom_right:
            return [True, [piece.x, piece.y]]
        return [False, []]

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

        def valid_coord(coord: List[int]) -> bool:
            """
            Validates a coordinate passed into it, in the format [x, y]

            :param coord: The coordinate being passed in
            :return: Whether the coordinate is valid
            """
            return coord[1] < 8 and coord[1] >= 0 and coord[0] < 8 and coord[0] >= 0

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

        if found_king == None:
            return True
        # found the king, now we map out all potential moves from the player, marking their movements on a board
        # if the king is surrounded, then the player has checkmate.
        mock_board = []
        for i in range(self.board.height):
            row = []
            for j in range(self.board.width):
                if self.board.board[i][j] == found_king:
                    row.append(found_king)
                else:
                    row.append(None)
            mock_board.append(row)
        # check if any pieces surround the king, then mark that as X
        #  self.board.print_board()
        for each_piece in opposing_player.pieces:  # O(m)
            if found_king is not None:
                is_in_king_space: List[bool, List[int]] = self.is_in_kings_space(found_king, each_piece)
                if is_in_king_space[0]:
                    mock_board[is_in_king_space[1][1]][is_in_king_space[1][0]] = 'O'
        #  analyze all pieces movements, marking all areas they can strike with an 'X'
        for each_piece in opposing_player.pieces:  # O(M*(K + J)) --> O(MK + MJ)
            all_potential_moves: List[List[int]] = each_piece.generate_potential_moves(self.board)  # K potential moves
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

            if found_king.x > 0 and valid_coord(left_coord):
                left = mock_board[left_coord[1]][left_coord[0]] in ['XO']
            if found_king.x < self.board.width and valid_coord(right_coord):
                right = mock_board[right_coord[1]][right_coord[0]] in ['XO']
            if found_king.y > 0 and valid_coord(top_coord):
                top = mock_board[top_coord[1]][top_coord[0]] in ['XO']
            if found_king.y < self.board.height and valid_coord(bottom_coord):
                bottom = mock_board[bottom_coord[1]][bottom_coord[0]] in ['XO']
            if found_king.y > 0 and found_king.x > 0 and valid_coord(top_left_coord):
                top_left = mock_board[top_left_coord[1]][top_left_coord[0]] in ['XO']
            if found_king.y < self.board.height and found_king.x < self.board.width and valid_coord(top_right_coord):
                top_right = mock_board[top_right_coord[1]][top_right_coord[0]] in ['XO']
            if found_king.y < self.board.height and found_king.x > 0 and valid_coord(bottom_left_coord):
                bottom_left = mock_board[bottom_left_coord[1]][bottom_left_coord[0]]
            if found_king.y < self.board.height and found_king.x < self.board.width and valid_coord(bottom_right_coord):
                bottom_right = mock_board[bottom_right_coord[1]][bottom_right_coord[0]] in ['XO']

            if left and right and top and bottom and top_left and top_right and bottom_left and bottom_right:
                return True
            #  clear all X's surrounding king
            if valid_coord(left_coord) and mock_board[left_coord[1]][left_coord[0]] == 'X':
                mock_board[left_coord[1]][left_coord[0]] = None
            if valid_coord(right_coord) and mock_board[right_coord[1]][right_coord[0]] == 'X':
                mock_board[right_coord[1]][right_coord[0]] = None
            if valid_coord(top_coord) and mock_board[top_coord[1]][top_coord[0]] == 'X':
                mock_board[top_coord[1]][top_coord[0]] = None
            if valid_coord(bottom_coord) and mock_board[bottom_coord[1]][bottom_coord[0]] == 'X':
                mock_board[bottom_coord[1]][bottom_coord[0]] = None
            if valid_coord(top_left_coord) and mock_board[top_left_coord[1]][top_left_coord[0]] == 'X':
                mock_board[top_left_coord[1]][top_left_coord[0]] = None
            if valid_coord(top_right_coord) and mock_board[top_right_coord[1]][top_right_coord[0]] == 'X':
                mock_board[top_right_coord[1]][top_right_coord[0]] = None
            if valid_coord(bottom_left_coord) and mock_board[bottom_left_coord[1]][bottom_left_coord[0]] == 'X':
                mock_board[bottom_left_coord[1]][bottom_left_coord[0]] = None
            if valid_coord(bottom_right_coord) and mock_board[bottom_right_coord[1]][bottom_right_coord[0]] == 'X':
                mock_board[bottom_right_coord[1]][bottom_right_coord[0]] = None

        return False

    def monte_carlo(self: Game, game: Game | None = None, depth: int = 0) -> Game | GameTreeNode:
        """
        Monte-Carlo Tree Search Algorithm, which constructs child nodes consisting of children of the current game instance
        and plays out those games and reports the result back to the callee, which then causes all the children nodes
        to contain values, which the higher the numerator, the more change white has to win with that move of the child
        node, the higher the denominator, the more change black has to win with that move of the child node. Then,
        we pick the maximum node among all the child nodes according to our results (If we are playing as white,
        then we pick the node with the highest numerator,  if we are black, then we pick the result with the highest
        denominator. The move is then assigned to the callee and we further process the next course of action given
        that move.

        :param game: The game instance, which is used to spawn the child nodes
        :param depth: The depth limit, which can be configured dependent on how many moves the user wants to simulate
        until playout of each child node C commences
        :return: The most optimal move among all the potential moves the user can make
        """
        if game is not None:
            if game.is_checkmate():
                node = GameTreeNode(game)
                node.denominator = 0 if game.turn == Team.WHITE else 1
                node.numerator = 0 if game.turn == Team.BLACK else 1
                return node
            game_clone = game
        else:
            game_clone = self

        if depth == 1:
            play_out_result = game.playout_game()
            node = GameTreeNode(game)
            node.numerator = 0 if play_out_result == Team.BLACK else 1
            node.denominator = 0 if play_out_result == Team.WHITE else 1
            return node
        monte_carlo_tree = GameTree().set_root(GameTreeNode(game_clone))
        #  process whose turn it is, and then make a random guess for the move to make
        current_player = game_clone.player_1 if game_clone.player_1.team == Team.WHITE else game_clone.player_2
        all_valid_potential_moves: List[List[int]] = []
        for each_piece in current_player.pieces:
            all_valid_potential_moves.extend([
                [each_piece.x, each_piece.y] + each_move
                if game_clone.board.validate_move(each_move[0], each_move[1], current_player.team)
                else []
                for each_move in each_piece.generate_potential_moves(game_clone.board)
            ])
        all_valid_potential_moves = list(filter(lambda x: len(x) > 0, all_valid_potential_moves))
        child_game_instances = []
        for each_valid_move in all_valid_potential_moves:
            child_game_instances.append(
                Game(game_clone.board, Player(game_clone.player_1), Player(game_clone.player_2), game_clone.turn)
                .simulate_move(
                    each_valid_move[0],
                    each_valid_move[1],
                    each_valid_move[2],
                    each_valid_move[3],
                    current_player.team
                )
            )
        for each_simulated_game in child_game_instances:
            monte_carlo_tree.root.add_child(GameTreeNode(each_simulated_game))
        for each_simulated_game_child in monte_carlo_tree.root.children:
            # randomly play-out each node
            simulation_result = game_clone.monte_carlo(each_simulated_game_child.value, depth + 1)
            monte_carlo_tree.root.denominator += simulation_result.denominator
            monte_carlo_tree.root.numerator += simulation_result.numerator
        max_denominator = 0
        max_node = None
        for each_node in monte_carlo_tree.root.children:
            if each_node.denominator > max_denominator:
                max_node = each_node
                max_denominator = each_node.denominator
        return max_node
