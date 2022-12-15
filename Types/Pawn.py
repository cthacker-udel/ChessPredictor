from __future__ import annotations

from ChessPiece import ChessPiece
from MoveSet import MoveSet


class Pawn(ChessPiece):
    """
    Represents a pawn piece on the chess board. https://www.chess.com/terms/chess-pawn
    """
    def __init__(self: Pawn, x: int, y: int) -> None:
        """
        Initializes a pawn instance, setting the x and y to its initial coordinates.

        :param x: The column where the pawn is being placed
        :param y: The row where the pawn is being placed
        """
        super()
        self.x = x
        self.y = y
        self.move_set = [MoveSet(0, 1), MoveSet(0, 2)]
        self.capture_moves = [MoveSet(1, 1), MoveSet(-1, -1)]
