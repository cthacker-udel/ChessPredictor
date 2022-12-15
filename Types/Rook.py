from __future__ import annotations
from MoveSet import MoveSet
from MoveSet import InfiniteDirection
from ChessPiece import ChessPiece
from Player import Team


class Rook(ChessPiece):
    """
    Represents a Rook piece on the chess board. https://en.wikipedia.org/wiki/Rook_(chess)
    """
    def __init__(self: Rook, x: int, y: int, team: Team) -> None:
        """
        Initializes a Rook instance, placing it at the initial x and y coordinates supplied

        :param x: The column where the rook is being placed initially
        :param y: The row where the rook is being placed initially
        :param team: The team the piece belongs to
        """
        super().__init__(x, y,
                         [MoveSet(0, 0, InfiniteDirection(True, False)), MoveSet(0, 0, InfiniteDirection(False, True))],
                         [MoveSet(0, 0, InfiniteDirection(True, False)), MoveSet(0, 0, InfiniteDirection(False, True))],
                         team)
        self.name = "Rook"
