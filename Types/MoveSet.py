from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass
class InfiniteDirection:
    """
    Represents the details of the infinite direction movement

    :var: x - Whether it can move in the x direction infinitely
    :var: y - Whether it can move in the y direction infinitely
    :var: diagonal - Whether it can move in the diagonal direction infinitely
    """
    x: Optional[bool] = False
    y: Optional[bool] = False
    diagonal: Optional[bool] = False


@dataclass
class MoveSet:
    """
    Represents the details of the move set of a chess piece

    :var: x - The x step the piece can take
    :var: y - The y step the piece can take
    :var: infinite_direction - The infinite direction the piece can move in
    """
    x: int
    y: int
    infinite_direction: Optional[InfiniteDirection] = None
