from __future__ import annotations
from MoveSet import MoveSet
from ChessPiece import ChessPiece


class King(ChessPiece):
    """
    The King chess piece. https://en.wikipedia.org/wiki/King_(chess)
    """
    def __init__(self: King, x: int, y: int) -> None:
        """
        Initializes a King instance, placing it at the x and y coordinates supplied

        :param x: The column where the King will be placed initially
        :param y: The row where the King will be placed initially
        """
        super()
        self.x = x
        self.y = y
        self.move_set = [
            MoveSet(1, 0),
            MoveSet(1, 1),
            MoveSet(1, -1),
            MoveSet(0, 1),
            MoveSet(0, -1),
            MoveSet(-1, -1),
            MoveSet(-1, 0),
            MoveSet(-1, 1)
        ]
        self.capture_moves = self.move_set
