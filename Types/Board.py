from __future__ import annotations

from typing import List, Optional

from ChessPiece import ChessPiece

from Player import Player, Team


class Board:
    """
    The board class, which houses the actual board itself, and all methods relating to the board.
    """

    def __init__(self: Board, width: int, height: int) -> None:
        """
        Initializes the board instance, takes in a width and height argument to set the board dimensions

        :param width: The width of the board
        :param height: The height of the board
        """
        self.width: int = width
        self.height: int = height
        self.board: List[List[ChessPiece | None]] = [[None] * height]
        self.player_one: Optional[Player] = None
        self.player_two: Optional[Player] = None

    def set_player_one(self: Board, player: Player) -> Board:
        """
        Sets player one who is playing on this board

        :param player: The Player instance, represents a challenger
        :return: The modified board instance
        """
        self.player_one = player
        return self

    def set_player_two(self: Board, player: Player) -> Board:
        """
        Sets player two who is playing on this board

        :param player: The Player instance, represents a challenger
        :return: The modified board instance
        """
        self.player_two = player
        return self

    def place_piece(self: Board, chess_piece: ChessPiece, x: int, y: int) -> Board:
        """
        Places a piece on the chess board, used for moving pieces along the board, and the initialization of the
        board when the players start the game.

        :param chess_piece: The piece to place
        :param x: The coordinate for where the piece is moving to, stands for the column the piece is being placed at
        :param y: The coordinate for where the piece is moving to, stands for the row where the piece is being placed at
        :return: The board instance after being mutated
        """
        self.board[y][x] = chess_piece
        return self

    def remove_piece(self: Board, x: int, y: int) -> ChessPiece:
        """
        Removes a piece on the chess board, used for removing pieces from the board in the event they are either
        captured, or moving.

        :param x: The coordinate for where the piece is being removed from, stands for the column
        :param y: The coordinate for where the piece is being removed from, stands for the row
        :return: The removed chess piece
        """
        removed_piece = self.board[y][x]
        del self.board[y][x]
        return removed_piece

    def clear(self: Board) -> Board:
        """
        Clears the board of all pieces, used when the game ends

        :return: The modified Board instance
        """
        self.board = [[] * self.height]
        return self

    def grab_piece(self, x: int, y: int) -> ChessPiece | None:
        """
        Accesses and returns the piece at indexes x and y.

        :param x: The column where the piece is located
        :param y: The row where the piece is located
        :return: The ChessPiece or None if no piece exists there
        """
        return self.board[y][x]

    def does_piece_exist(self: Board, x: int, y: int) -> bool:
        """
        Checks if a piece is existent on that space, the space being the x and y coordinates supplied

        :param x: The column where we are checking if a piece is existent on
        :param y: The row where we are checking if a piece is existent on
        :return: Whether a piece is present on that row and column
        """
        return self.board[y][x] is not None

    def validate_move(self: Board, to_x: int, to_y: int, moving_team: Team) -> bool:
        """
        Validates the move being requested, and returns a boolean indicating if the move is valid

        :param moving_team: The team that is requesting the move
        :param to_x: The column where the piece is being moved to
        :param to_y: The row where the piece is being moved to
        :return: Whether the piece can be moved to that coordinate
        """
        to_piece = self.grab_piece(to_x, to_y)
        if to_piece is not None and to_piece.team == moving_team:  # Piece exists at coordinate and team is movers
            return False
        elif (to_x >= self.width or to_x < 0) or (to_y >= self.height or to_y < 0):  # Moving out of bounds
            return False
        return True

    def move_piece(self: Board, from_x: int, from_y: int, to_x: int, to_y: int, moving_team: Team) -> Board:
        """
        Moves a piece on the chess board, directly mutating the instance and returning it

        :param moving_team: The team that is requesting the move
        :param from_x: The column where the piece currently is
        :param from_y: The row where the piece currently is
        :param to_x: The column where the piece is moving to
        :param to_y: The row where the piece is moving to
        :return: The modified Board
        """
        if self.validate_move(to_x, to_y, moving_team):
            removed_piece = self.remove_piece(from_x, from_y)
            self.place_piece(removed_piece, to_x, to_y)
        return self
