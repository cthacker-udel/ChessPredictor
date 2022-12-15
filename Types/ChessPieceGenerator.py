from __future__ import annotations
from Player import Team
from ChessPiece import ChessPiece
from typing import List


class ChessPieceGenerator:

    def __init__(self: ChessPieceGenerator, team: Team) -> None:
        """
        Initializes a ChessPieceGenerator class, which generates all starting pieces, or any piece in general

        :param team:
        """
        self.team = team

    def generate_initial_pieces(self: ChessPieceGenerator) -> List[ChessPiece]:
        #  One king, One Queen, Two Rooks, Two Bishops, Two Knights, Eight Pawns
        generated_chess_pieces: List[ChessPiece] = []

