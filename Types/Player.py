from __future__ import annotations
from enum import Enum
from ChessPiece import ChessPiece
from typing import List, Optional


class Team(Enum):
    """
    Represents the possible teams the player can belong to, in chess it's two, either white or black
    """
    WHITE = 0  # The White Team
    BLACK = 1  # The Black Team


class Player:
    """
    The Player class, which represents a player of one of the two teams in chess
    """

    def __init__(self: Player) -> None:
        """
        Initializes a player instance, with all fields defaulted
        """
        self.team: Team | None = None
        self.captured_pieces: List[ChessPiece] = []
        self.pieces: List[ChessPiece] = []
        self.name: Optional[str] = ''

    def clear_pieces(self: Player) -> None:
        """
        Clears the player's owned pieces and captured pieces
        """
        self.pieces = []
        self.captured_pieces = []
