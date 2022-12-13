from MoveSet import MoveSet
from ChessPiece import ChessPiece


class King(ChessPiece):
    def __init__(self, x: int, y: int):
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
