from __future__ import annotations
from MoveSet import MoveSet
from MoveSet import InfiniteDirection
from ChessPiece import ChessPiece
from Player import Team


class Queen(ChessPiece):
    """
    The Queen Piece in chess. https://en.wikipedia.org/wiki/Queen_(chess)
    """
    def __init__(self: Queen, x: int, y: int, team: Team) -> None:
        """
        Initializes the Queen Piece instance

        :param x: The column where the queen piece is being placed upon its creation
        :param y: The row where the queen piece is being placed upon its creation
        :param team: The team the piece belongs to
        """
        super().__init__(x, y,
                         [MoveSet(0, 0, InfiniteDirection(True, True, True))],
                         [MoveSet(0, 0, InfiniteDirection(True, True, True))],
                         team)
        self.name = "Queen"
