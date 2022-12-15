from __future__ import annotations
from ChessPiece import ChessPiece
from MoveSet import MoveSet
from MoveSet import InfiniteDirection


class Bishop(ChessPiece):
    """
    Represents a Bishop piece on the chess board. https://en.wikipedia.org/wiki/Bishop_(chess)
    """
    def __init__(self: Bishop, x: int, y: int) -> None:
        """
        Initializes a Bishop instance, placing it at the x and y coordinates supplied

        :param x: The initial x coordinate where the Bishop piece is being placed
        :param y: The initial y coordinate where the Bishop piece is being placed
        """
        super()
        self.x = x
        self.y = y
        self.move_set = [MoveSet(0, 0, InfiniteDirection(True, True, True))]
        self.capture_moves = self.move_set
