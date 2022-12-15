from __future__ import annotations
from typing import List, Optional
from MoveSet import MoveSet
from Player import Team


class ChessPiece:
    """
    Represents a ChessPiece, contains fields x, y, and move_set.

    :var: x - The x coordinate
    :var: y - The y coordinate
    :var: move_set - The moveset of the piece

    """
    def __init__(self: ChessPiece, x: int, y: int, move_set: List[MoveSet], capture_moves: List[MoveSet], team: Team):
        """
        Initializes a new instance of the ChessPiece, which holds all the necessities for a chess piece, such as the
        x and y coordinates, the move_set, capture_moves, and the team

        :param x: The column where the piece is being placed
        :param y: The row where the piece is being placed
        :param move_set: The move set of the piece
        :param capture_moves: The capture moves of the piece
        :param team: The team of the piece
        """
        self.x = x
        self.y = y
        self.move_set = move_set
        self.capture_moves = capture_moves
        self.team = team

    def set_team(self: ChessPiece, team: Team) -> ChessPiece:
        """
        Sets the ChessPiece's team and returns the modified instance

        :param team: The new team the ChessPiece will belong to
        :return:
        """
        self.team = team
        return self
