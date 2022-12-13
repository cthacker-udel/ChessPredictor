from MoveSet import MoveSet
from ChessPiece import ChessPiece


class Knight(ChessPiece):
    """
    Represents a knight piece on the chess board
    """
    def __init__(self, x: int, y: int):
        super()
        self.x = x
        self.y = y
        self.move_set = [
            MoveSet(-1, 2),
            MoveSet(1, 2),
            MoveSet(2, 1),
            MoveSet(2, -1),
            MoveSet(-2, 1),
            MoveSet(-2, -1),
            MoveSet(1, -2),
            MoveSet(-1, -2)
        ]
        self.capture_moves = self.move_set
