from __future__ import annotations
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from Types.MoveSet import MoveSet
    from Types.Player import Team
    from Types.Board import Board


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

    def generate_potential_moves(self: ChessPiece, board: Board) -> List[List[int]]:
        """
        Generates all potential moves from a given chess piece, analyzing its move-set and returning all
        possible coordinates it can move to

        MAJOR TODO: MAKE SURE THE PIECE CANNOT JUMP OVER PIECES, HAPPENED WITH THE QUEEN JUMPING OVER PAWNS

        :return: All the possible moves the chess piece can make
        """
        #  check if move is infinite, if so, we generate a large amount of them
        #  While cycling through coordinates, check if piece is on spot, if it is, then break out of the loop

        infinite_moves = [x for x in filter(lambda move: move.infinite_direction is not None, self.move_set)]
        potential_moves = []
        if len(infinite_moves) > 0:
            #  we have infinite moves, time to generate tons of potential moves we can make!
            for each_infinite_move in infinite_moves:
                if each_infinite_move.infinite_direction.x:
                    #  can move infinitely in the x
                    x_moving_left = self.x - 1
                    while x_moving_left >= 0:
                        if board.grab_piece(x_moving_left, self.y) is not None:
                            if board.grab_piece(x_moving_left, self.y).team != self.team:
                                potential_moves.append([x_moving_left, self.y])
                            break
                        potential_moves.append([x_moving_left, self.y])
                        x_moving_left -= 1
                    x_moving_right = self.x + 1
                    while x_moving_right < 8:
                        if board.grab_piece(x_moving_right, self.y) is not None:
                            if board.grab_piece(x_moving_right, self.y).team != self.team:
                                potential_moves.append([x_moving_right, self.y])
                            break
                        potential_moves.append([x_moving_right, self.y])
                        x_moving_right += 1
                elif each_infinite_move.infinite_direction.y:
                    #  can move infinitely in the y
                    y_moving_up = self.y - 1
                    while y_moving_up >= 0:
                        if board.grab_piece(self.x, y_moving_up) is not None:
                            if board.grab_piece(self.x, y_moving_up).team != self.team:
                                potential_moves.append([self.x, y_moving_up])
                            break
                        potential_moves.append([self.x,  y_moving_up])
                        y_moving_up -= 1
                    y_moving_down = self.y + 1
                    while y_moving_down < 8:
                        if board.grab_piece(self.x, y_moving_down) is not None:
                            if board.grab_piece(self.x, y_moving_down).team != self.team:
                                potential_moves.append([self.x, y_moving_down])
                            break
                        potential_moves.append([self.x, y_moving_down])
                        y_moving_down += 1
                elif each_infinite_move.infinite_direction.diagonal:
                    #  can move infinitely in the diagonal direction
                    diag_up_right_x = self.x + 1
                    diag_up_right_y = self.y - 1
                    while diag_up_right_y >= 0 and diag_up_right_x < 8:
                        if board.grab_piece(diag_up_right_x, diag_up_right_y) is not None:
                            if board.grab_piece(diag_up_right_x, diag_up_right_y).team != self.team:
                                potential_moves.append([diag_up_right_x, diag_up_right_y])
                            break
                        potential_moves.append([diag_up_right_x, diag_up_right_y])
                        diag_up_right_x += 1
                        diag_up_right_y -= 1

                    diag_up_left_x = self.x - 1
                    diag_up_left_y = self.y - 1
                    while diag_up_left_x >= 0 and diag_up_left_y >= 0:
                        if board.grab_piece(diag_up_left_x, diag_up_left_y) is not None:
                            if board.grab_piece(diag_up_left_x, diag_up_left_y).team != self.team:
                                potential_moves.append([diag_up_left_x, diag_up_left_y])
                            break
                        potential_moves.append([diag_up_left_x, diag_up_left_y])
                        diag_up_left_x -= 1
                        diag_up_left_y -= 1

                    diag_down_left_x = self.x - 1
                    diag_down_left_y = self.y + 1
                    while diag_down_left_x >= 0 and diag_down_left_y < 8:
                        if board.grab_piece(diag_down_left_x, diag_down_left_y) is not None:
                            if board.grab_piece(diag_down_left_x, diag_down_left_y).team != self.team:
                                potential_moves.append([diag_down_left_x, diag_down_left_y])
                            break
                        potential_moves.append([diag_down_left_x, diag_down_left_y])
                        diag_down_left_x -= 1
                        diag_down_left_y += 1

                    diag_down_right_x = self.x + 1
                    diag_down_right_y = self.y + 1
                    while diag_down_right_x < 8 and diag_down_right_y < 8:
                        if board.grab_piece(diag_down_right_x, diag_down_right_y) is not None:
                            if board.grab_piece(diag_down_right_x, diag_down_right_y).team != self.team:
                                potential_moves.append([diag_down_right_x, diag_down_right_y])
                            break
                        potential_moves.append([diag_down_right_x, diag_down_right_y])
                        diag_down_right_x += 1
                        diag_down_right_y += 1
            return potential_moves
        else:
            #  we have a fixed move-set, that means we will only generate k moves, one for each move in the move-set
            for each_move in self.move_set:
                modified_x = self.x + each_move.x
                modified_y = self.y + each_move.y
                if (modified_x >= 8 or modified_x < 0 or modified_y >= 8 or modified_y < 0) or board.grab_piece(modified_x, modified_y) is not None and board.grab_piece(modified_x, modified_y).team == self.team:
                    continue
                potential_moves.append([modified_x, modified_y])
            potential_moves = list(filter(lambda x: (x[0] < 8 and x[1] < 8) and (x[0] >= 0 and x[1] >= 0), potential_moves))
            return potential_moves

