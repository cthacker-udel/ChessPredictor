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
        self.name = ''

    def set_team(self: ChessPiece, team: Team) -> ChessPiece:
        """
        Sets the ChessPiece's team and returns the modified instance

        :param team: The new team the ChessPiece will belong to
        :return:
        """
        self.team = team
        return self

    def generate_potential_moves(self: ChessPiece) -> List[List[int]]:
        """
        Generates all potential moves from a given chess piece, analyzing its move-set and returning all
        possible coordinates it can move to

        :return: All the possible moves the chess piece can make
        """
        #  check if move is infinite, if so, we generate a large amount of them
        infinite_moves = [x for x in filter(lambda move: move.infinite is not None, self.move_set)]
        potential_moves = []
        if len(infinite_moves) > 0:
            #  we have infinite moves, time to generate tons of potential moves we can make!
            for each_infinite_move in infinite_moves:
                if each_infinite_move.infinite_direction.x:
                    #  can move infinitely in the x
                    x_moving_left = self.x - 1
                    while x_moving_left >= 0:
                        potential_moves.append([x_moving_left, self.y])
                        x_moving_left -= 1
                    x_moving_right = self.x + 1
                    while x_moving_right < 8:
                        potential_moves.append([x_moving_right, self.y])
                        x_moving_right += 1
                elif each_infinite_move.infinite_direction.y:
                    #  can move infinitely in the y
                    y_moving_up = self.y - 1
                    while y_moving_up >= 0:
                        potential_moves.append([self.x,  y_moving_up])
                        y_moving_up -= 1
                    y_moving_down = self.y + 1
                    while y_moving_down < 8:
                        potential_moves.append([self.x, y_moving_down])
                        y_moving_down += 1
                elif each_infinite_move.infinite_direction.diagonal:
                    #  can move infinitely in the diagonal direction
                    diag_up_right_x = self.x + 1
                    diag_up_right_y = self.y - 1
                    while diag_up_right_y >= 0 and diag_up_right_x < 8:
                        potential_moves.append([diag_up_right_x, diag_up_right_y])
                        diag_up_right_x += 1
                        diag_up_right_y -= 1

                    diag_up_left_x = self.x - 1
                    diag_up_left_y = self.y - 1
                    while diag_up_left_x >= 0 and diag_up_left_y >= 0:
                        potential_moves.append([diag_up_left_x, diag_up_left_y])
                        diag_up_left_x -= 1
                        diag_up_left_y -= 1

                    diag_down_left_x = self.x - 1
                    diag_down_left_y = self.y + 1
                    while diag_down_left_x >= 0 and diag_down_left_y < 8:
                        potential_moves.append([diag_down_left_x, diag_down_left_y])
                        diag_down_left_x -= 1
                        diag_down_left_y += 1

                    diag_down_right_x = self.x + 1
                    diag_down_right_y = self.y + 1
                    while diag_down_right_x < 8 and diag_down_right_y < 8:
                        potential_moves.append([diag_down_right_x, diag_down_right_y])
                        diag_down_right_x += 1
                        diag_down_right_y += 1
            return potential_moves
        else:
            #  we have a fixed move-set, that means we will only generate k moves, one for each move in the move-set
            for each_move in self.move_set:
                modified_x = self.x + each_move.x
                modified_y = self.y + each_move.y
                potential_moves.append([modified_x, modified_y])
            return potential_moves

