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
    """
    Helper class, designed to house functions that setup some functionality of the game
    """
    def __init__(self: ChessPieceGenerator, team: Team) -> None:
        """
        Initializes a ChessPieceGenerator class, which generates all starting pieces, or any piece in general

        :param team:
        """
        self.team = team
        self.modified_initial_placement: dict[Team, dict[str, List[List[int]]]] = {
            Team.WHITE: {
                "Bishop": [[0, 2], [0, 5]],
                "King": [[0, 3]],
                "Knight": [[0, 1], [0, 6]],
                "Pawn": [[1, 0], [1, 1], [1, 2], [1, 3], [1, 4], [1, 5], [1, 6], [1, 7]],
                "Queen": [[0, 4]],
                "Rook": [[0, 0], [0, 7]]
            },
            Team.BLACK: {
                "Bishop": [[7, 2], [7, 5]],
                "King": [[7, 3]],
                "Knight": [[7, 1], [7, 6]],
                "Pawn": [[6, 0], [6, 1], [6, 2], [6, 3], [6, 4], [6, 5], [6, 6], [6, 7]],
                "Queen": [[7, 4]],
                "Rook": [[7, 0], [7, 7]]
            }
        }

    def generate_initial_pieces(self: ChessPieceGenerator) -> List[ChessPiece]:
        """
        Generates an array of all the starting chess pieces, configured for each respective team that requests them

        :return: The array of generated chess pieces
        """
        #  One king, One Queen, Two Rooks, Two Bishops, Two Knights, Eight Pawns
        king_coords = self.modified_initial_placement[self.team]["King"]
        queen_coords = self.modified_initial_placement[self.team]["Queen"]
        rook_coords = self.modified_initial_placement[self.team]["Rook"]
        bishop_coords = self.modified_initial_placement[self.team]["Bishop"]
        knight_coords = self.modified_initial_placement[self.team]["Knight"]
        pawn_coords = self.modified_initial_placement[self.team]["Pawn"]
        king: List[ChessPiece] = [King(king_coords[0][1], king_coords[0][0], self.team)]
        queen: List[ChessPiece] = [Queen(queen_coords[0][1], queen_coords[0][0], self.team)]
        rooks: List[ChessPiece] = [Rook(rook_coords[0][1], rook_coords[0][0], self.team),
                                   Rook(rook_coords[1][1], rook_coords[1][0],
                                        self.team)]
        bishops: List[ChessPiece] = [Bishop(bishop_coords[0][1], bishop_coords[0][0], self.team),
                                     Bishop(bishop_coords[1][1],
                                            bishop_coords[1][0],
                                            self.team)]
        knights: List[ChessPiece] = [Knight(knight_coords[0][1], knight_coords[0][0], self.team),
                                     Knight(knight_coords[1][1],
                                            knight_coords[1][0],
                                            self.team)]
        pawns: List[ChessPiece] = [Pawn(pawn_coords[0][1], pawn_coords[0][0], self.team),
                                   Pawn(pawn_coords[1][1], pawn_coords[1][0], self.team),
                                   Pawn(pawn_coords[2][1], pawn_coords[2][0], self.team),
                                   Pawn(pawn_coords[3][1], pawn_coords[3][0], self.team),
                                   Pawn(pawn_coords[4][1], pawn_coords[4][0], self.team),
                                   Pawn(pawn_coords[5][1], pawn_coords[5][0], self.team),
                                   Pawn(pawn_coords[6][1], pawn_coords[6][0], self.team),
                                   Pawn(pawn_coords[7][1], pawn_coords[7][0], self.team)
                                   ]

        generated_chess_pieces: List[ChessPiece] = king + queen + rooks + bishops + knights + pawns
        return generated_chess_pieces
