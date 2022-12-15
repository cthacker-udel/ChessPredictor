from dataclasses import dataclass
from enum import Enum
from ChessPiece import ChessPiece
from typing import List, Optional


class Team(Enum):
    """
    Represents the possible teams the player can belong to, in chess it's two, either white or black
    """
    WHITE = 0  # The White Team
    BLACK = 1  # The Black Team


@dataclass
class Player:
    """
    The Player class, which represents a player of one of the two teams in chess
    """
    team: Team  # The team the player belongs to, either white or black
    captured_pieces: List[ChessPiece]  # The chess pieces the user has captured
    pieces: List[ChessPiece]  # The ChessPieces the player owns
    name: Optional[str]  # The name of the player (customization option)
