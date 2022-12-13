from ChessPiece import ChessPiece
from MoveSet import MoveSet
from MoveSet import InfiniteDirection


class Bishop(ChessPiece):
    """
    Represents a Bishop piece on the chess board
    """
    def __init__(self, x: int, y: int):
        super()
        self.x = x
        self.y = y
        self.move_set = [MoveSet(0, 0, InfiniteDirection(True, True, True))]
        self.capture_moves = self.move_set
