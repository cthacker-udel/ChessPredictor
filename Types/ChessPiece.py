from dataclasses import dataclass
from typing import List, Optional
from MoveSet import MoveSet


@dataclass
class ChessPiece:
    """
    Represents a ChessPiece, contains fields x, y, and move_set.

    :var: x - The x coordinate
    :var: y - The y coordinate
    :var: move_set - The moveset of the piece

    """
    x: int  # the x coordinate of the piece
    y: int  # the y coordinate of the piece
    move_set: List[MoveSet]  # the move set of the piece
    capture_moves: Optional[List[MoveSet]]  # the moves used to capture pieces (Pawns, for example)
