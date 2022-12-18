from __future__ import annotations

from typing import List, Optional, TYPE_CHECKING
from Types.Player import Team

if TYPE_CHECKING:
    from Types.ChessPiece import ChessPiece

    from Types.Player import Player


class Board:
    """
    The board class, which houses the actual board itself, and all methods relating to the board.
    """

    def __init__(self: Board, width: int = 8, height: int = 8) -> None:
        """
        Initializes the board instance, takes in a width and height argument to set the board dimensions

        :param width: The width of the board
        :param height: The height of the board
        """
        self.width: int = width
        self.height: int = height
        self.board: List[List[ChessPiece | None]] = []
        row = []
        for i in range(height):
            for j in range(width):
                row.append(None)
            self.board.append(row)
            row = []
        self.player_one: Optional[Player] = None
        self.player_two: Optional[Player] = None

    def set_player_one(self: Board, player: Player) -> Board:
        """
        Sets player one who is playing on this board

        :param player: The Player instance, represents a challenger
        :return: The modified board instance
        """
        self.player_one = player
        return self

    def set_player_two(self: Board, player: Player) -> Board:
        """
        Sets player two who is playing on this board

        :param player: The Player instance, represents a challenger
        :return: The modified board instance
        """
        self.player_two = player
        return self

    def place_piece(self: Board, chess_piece: ChessPiece, x: int, y: int) -> Board:
        """
        Places a piece on the chess board, used for moving pieces along the board, and the initialization of the
        board when the players start the game.

        :param chess_piece: The piece to place
        :param x: The coordinate for where the piece is moving to, stands for the column the piece is being placed at
        :param y: The coordinate for where the piece is moving to, stands for the row where the piece is being placed at
        :return: The board instance after being mutated
        """
        self.board[y][x] = chess_piece
        chess_piece.x = x
        chess_piece.y = y
        return self

    def remove_piece(self: Board, x: int, y: int) -> ChessPiece | None:
        """
        Removes a piece on the chess board, used for removing pieces from the board in the event they are either
        captured, or moving.

        :param x: The coordinate for where the piece is being removed from, stands for the column
        :param y: The coordinate for where the piece is being removed from, stands for the row
        :return: The removed chess piece
        """
        removed_piece = self.board[y][x]
        self.board[y][x] = None
        return removed_piece

    def clear(self: Board) -> Board:
        """
        Clears the board of all pieces, used when the game ends

        :return: The modified Board instance
        """
        self.board = [[] * self.height]
        return self

    def grab_piece(self, x: int, y: int) -> ChessPiece | None:
        """
        Accesses and returns the piece at indexes x and y.

        :param x: The column where the piece is located
        :param y: The row where the piece is located
        :return: The ChessPiece or None if no piece exists there
        """
        return self.board[y][x]

    def does_piece_exist(self: Board, x: int, y: int) -> bool:
        """
        Checks if a piece is existent on that space, the space being the x and y coordinates supplied

        :param x: The column where we are checking if a piece is existent on
        :param y: The row where we are checking if a piece is existent on
        :return: Whether a piece is present on that row and column
        """
        return self.board[y][x] is not None

    def validate_move(self: Board, to_x: int, to_y: int, moving_team: Team) -> bool:
        """
        Validates the move being requested, and returns a boolean indicating if the move is valid

        :param moving_team: The team that is requesting the move
        :param to_x: The column where the piece is being moved to
        :param to_y: The row where the piece is being moved to
        :return: Whether the piece can be moved to that coordinate
        """
        to_piece = self.grab_piece(to_x, to_y)
        if to_piece is not None and to_piece.team == moving_team:  # Piece exists at coordinate and team is movers
            return False
        elif (to_x >= self.width or to_x < 0) or (to_y >= self.height or to_y < 0):  # Moving out of bounds
            return False
        return True

    def is_capture(self: Board, to_x: int, to_y: int, moving_team: Team) -> bool:
        """
        Determines if the move is a capturing move, meaning that the player takes the opponent's piece at that spot
        and replaces that spot with the piece they are moving.

        :param to_x: The column where the user is requesting the move
        :param to_y: The row where the user is requesting the move
        :param moving_team: The team of the player that is moving the piece
        :return: Whether it is a capture move
        """
        moving_to_piece = self.grab_piece(to_x, to_y)
        return moving_to_piece is not None and moving_to_piece.team != moving_team

    def capture_piece(self: Board, to_x: int, to_y: int, moving_team: Team) -> ChessPiece:
        """
        Captures the piece at the coordinates `to_x` and `to_y`.

        :param to_x: The column where the user is requesting the move
        :param to_y: The row where the user is requesting the move
        :param moving_team: The team that is requesting the move
        :return: The capture piece
        """
        captured_piece: ChessPiece | None = self.remove_piece(to_x, to_y)  # The piece that was captured
        moving_player: Player = self.player_one if self.player_one.team == moving_team else self.player_two  # the
        # player that is moving their piece
        victim_player: Player = self.player_one if moving_player != self.player_one else self.player_two  # The player
        # that is being moved on
        victim_player.pieces.remove(captured_piece)  # removes the piece from the victim's piece array, because their
        # piece has been captured
        moving_player.captured_pieces.append(captured_piece)  # appends the piece to the captured pieces array of the
        # moving player
        return captured_piece

    def print_board(self: Board) -> None:
        """
        Prints the board for debugging or visual purposes

        :return: None, just prints the board
        """
        print('-------------------------------------------------------------')
        print(
            "Player One Pieces : {}  |  Player Two Pieces : {}\n Player One Captured Pieces : {}  |  Player Two "
            "Captured Pieces : {}".format(
                len(self.player_one.pieces), len(self.player_two.pieces), len(self.player_one.captured_pieces),
                len(self.player_two.captured_pieces)))
        for i in range(self.height):
            row = []
            for j in range(self.width):
                if self.board[i][j] is None:
                    row.append('({},{})_'.format(j, i))
                else:
                    row.append('({},{}){}{}'.format(self.board[i][j].x, self.board[i][j].y,
                                                    'W-' if self.board[i][j].team == Team.WHITE else 'B-',
                                                    self.board[i][j].name))
            print(row)

    def move_piece(self: Board, from_x: int, from_y: int, to_x: int, to_y: int, moving_team: Team) -> Board:
        """
        Moves a piece on the chess board, directly mutating the instance and returning it

        :param moving_team: The team that is requesting the move
        :param from_x: The column where the piece currently is
        :param from_y: The row where the piece currently is
        :param to_x: The column where the piece is moving to
        :param to_y: The row where the piece is moving to
        :return: The modified Board
        """
        removed_piece: ChessPiece | None = None
        moving_player = self.player_one if self.player_one.team == moving_team else self.player_two
        if self.validate_move(to_x, to_y, moving_team):
            if self.is_capture(to_x, to_y, moving_team):
                self.capture_piece(to_x, to_y, moving_team)
            removed_piece = self.remove_piece(from_x, from_y)
            self.place_piece(removed_piece, to_x, to_y)
            removed_piece_index = moving_player.pieces.index(removed_piece)
            moving_player.pieces.remove(removed_piece)
            moving_player.pieces.insert(removed_piece_index, removed_piece)
        return self

    def set_board(self: Board, player_1: Player, player_2: Player) -> Board:
        """
        Initializes the board, aka "setting" the board, given both players, sets their pieces in their respective spots

        :param player_1: Player 1
        :param player_2: Player 2
        :return: The Board instance
        """
        for piece_1, piece_2 in zip(player_1.pieces, player_2.pieces):
            self.board[piece_1.y][piece_1.x] = piece_1
            self.board[piece_2.y][piece_2.x] = piece_2
        return self
