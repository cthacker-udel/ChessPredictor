from __future__ import annotations
from typing import TYPE_CHECKING
from Types.MoveSet import MoveSet
from Types.MoveSet import InfiniteDirection
from Types.ChessPiece import ChessPiece

if TYPE_CHECKING:
    from Types.Player import Team


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
                         [MoveSet(0, 0, InfiniteDirection(False, False, True))],
                         [MoveSet(0, 0, InfiniteDirection(False, False, True))],
                         team)
        self.name = "Queen"
