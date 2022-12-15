from __future__ import annotations

from MoveSet import MoveSet
from ChessPiece import ChessPiece
from Player import Team


class Knight(ChessPiece):
    """
    Represents a knight piece on the chess board. https://en.wikipedia.org/wiki/Knight_(chess)
    """
    def __init__(self: Knight, x: int, y: int, team: Team) -> None:
        """
        Initializes a Knight instance on the chess board, placing the knight at the x and y coordinates supplied

        :param x: The column where the knight will be place
        :param y: The row where the knight will be placed
        :param team: The team the piece belongs to
        """
        super().__init__(x, y, [
            MoveSet(-1, 2),
            MoveSet(1, 2),
            MoveSet(2, 1),
            MoveSet(2, -1),
            MoveSet(-2, 1),
            MoveSet(-2, -1),
            MoveSet(1, -2),
            MoveSet(-1, -2)
        ], [
            MoveSet(-1, 2),
            MoveSet(1, 2),
            MoveSet(2, 1),
            MoveSet(2, -1),
            MoveSet(-2, 1),
            MoveSet(-2, -1),
            MoveSet(1, -2),
            MoveSet(-1, -2)
        ], team)
        self.name = "Knight"
