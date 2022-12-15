from __future__ import annotations

from typing import List

from ChessPiece import ChessPiece


class Board:
    """
    The board class, which houses the actual board itself, and all methods relating to the board.
    """

    def __init__(self, width: int, height: int) -> None:
        """
        Initializes the board instance, takes in a width and height argument to set the board dimensions

        :param width: The width of the board
        :param height: The height of the board
        """
        self.width: int = width
        self.height: int = height
        self.board: List[List[ChessPiece]] = [[] * height]

    def place_piece(self, chess_piece: ChessPiece, x: int, y: int) -> Board:
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

    def remove_piece(self, x: int, y: int) -> ChessPiece:
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

    def clear(self) -> Board:
        """
        Clears the board of all pieces, used when the game ends

        :return: The modified Board instance
        """
        self.board = [[] * self.height]
        return self
