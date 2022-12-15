from __future__ import annotations
from Player import Team
from ChessPiece import ChessPiece
from typing import List
from King import King
from Bishop import Bishop
from Knight import Knight
from Pawn import Pawn
from Queen import Queen
from Rook import Rook


class ChessPieceGenerator:

    def __init__(self: ChessPieceGenerator, team: Team) -> None:
        """
        Initializes a ChessPieceGenerator class, which generates all starting pieces, or any piece in general

        :param team:
        """
        self.team = team
        self.modified_initial_placement = {
            Team.WHITE: {},
            Team.BLACK: {}
        }

    def generate_initial_pieces(self: ChessPieceGenerator) -> List[ChessPiece]:
        #  One king, One Queen, Two Rooks, Two Bishops, Two Knights, Eight Pawns
        generated_chess_pieces: List[ChessPiece] = []
        generated_chess_pieces.append(King())
