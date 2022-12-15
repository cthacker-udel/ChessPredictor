from __future__ import annotations
from MoveSet import MoveSet
from MoveSet import InfiniteDirection
from ChessPiece import ChessPiece


class Rook(ChessPiece):
    """
    Represents a Rook piece on the chess board. https://en.wikipedia.org/wiki/Rook_(chess)
    """
    def __init__(self: Rook, x: int, y: int) -> None:
        """
        Initializes a Rook instance, placing it at the initial x and y coordinates supplied

        :param x: The column where the rook is being placed initially
        :param y: The row where the rook is being placed initially
        """
        super()
        self.x = x
        self.y = y
        self.move_set = [MoveSet(0, 0, InfiniteDirection(True, False)), MoveSet(0, 0, InfiniteDirection(False, True))]
        self.capture_moves = self.move_set
