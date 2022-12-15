from __future__ import annotations
from MoveSet import MoveSet
from MoveSet import InfiniteDirection
from ChessPiece import ChessPiece


class Queen(ChessPiece):
    """
    The Queen Piece in chess. https://en.wikipedia.org/wiki/Queen_(chess)
    """
    def __init__(self: Queen, x: int, y: int) -> None:
        """
        Initializes the Queen Piece instance

        :param x: The column where the queen piece is being placed upon its creation
        :param y: The row where the queen piece is being placed upon its creation
        """
        super()
        self.x = x
        self.y = y
        self.move_set = [MoveSet(0, 0, InfiniteDirection(True, True, True))]
        self.capture_moves = self.move_set
