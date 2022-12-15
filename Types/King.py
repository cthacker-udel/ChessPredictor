from __future__ import annotations
from MoveSet import MoveSet
from ChessPiece import ChessPiece
from Player import Team
from typing import List


class King(ChessPiece):
    """
    The King chess piece. https://en.wikipedia.org/wiki/King_(chess)
    """
    def __init__(self: King, x: int, y: int, team: Team) -> None:
        """
        Initializes a King instance, placing it at the x and y coordinates supplied

        :param x: The column where the King will be placed initially
        :param y: The row where the King will be placed initially
        :param team: The team the piece belongs to
        """
        super().__init__(x, y, [
            MoveSet(1, 0),
            MoveSet(1, 1),
            MoveSet(1, -1),
            MoveSet(0, 1),
            MoveSet(0, -1),
            MoveSet(-1, -1),
            MoveSet(-1, 0),
            MoveSet(-1, 1)
        ], [
            MoveSet(1, 0),
            MoveSet(1, 1),
            MoveSet(1, -1),
            MoveSet(0, 1),
            MoveSet(0, -1),
            MoveSet(-1, -1),
            MoveSet(-1, 0),
            MoveSet(-1, 1)
        ], team)
        self.name = "King"
