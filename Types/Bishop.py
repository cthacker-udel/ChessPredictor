from __future__ import annotations
from ChessPiece import ChessPiece
from MoveSet import MoveSet
from MoveSet import InfiniteDirection
from Player import Team


class Bishop(ChessPiece):
    """
    Represents a Bishop piece on the chess board. https://en.wikipedia.org/wiki/Bishop_(chess)
    """
    def __init__(self: Bishop, x: int, y: int, team: Team) -> None:
        """
        Initializes a Bishop instance, placing it at the x and y coordinates supplied

        :param x: The initial x coordinate where the Bishop piece is being placed
        :param y: The initial y coordinate where the Bishop piece is being placed
        :param team: The team the piece belongs to
        """
        super().__init__(x, y,
                         [MoveSet(0, 0, InfiniteDirection(False, False, True))],
                         [MoveSet(0, 0, InfiniteDirection(False, False, True))],
                         team)
        self.name = "Bishop"

