from __future__ import annotations
from typing import TYPE_CHECKING

from Types.MoveSet import MoveSet
from Types.ChessPiece import ChessPiece

if TYPE_CHECKING:
    from Types.Player import Team


class Pawn(ChessPiece):
    """
    Represents a pawn piece on the chess board. https://www.chess.com/terms/chess-pawn
    """
    def __init__(self: Pawn, x: int, y: int, team: Team) -> None:
        """
        Initializes a pawn instance, setting the x and y to its initial coordinates.

        :param x: The column where the pawn is being placed
        :param y: The row where the pawn is being placed
        :param team: The team the piece belongs to
        """
        super().__init__(x, y, [MoveSet(0, 1), MoveSet(0, 2)], [MoveSet(1, 1), MoveSet(-1, -1)], team)
        self.name = "Pawn"
