from ChessPiece import ChessPiece
from MoveSet import MoveSet


class Pawn(ChessPiece):
    """
    Represents a pawn piece on the chess board
    """
    def __init__(self, x: int, y: int):
        super()
        self.x = x
        self.y = y
        self.move_set = [MoveSet(0, 1), MoveSet(0, 2)]
        self.capture_moves = [MoveSet(1, 1), MoveSet(-1, -1)]
