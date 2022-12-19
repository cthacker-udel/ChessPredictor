from __future__ import annotations

from Types.Board import Board
from Types.Player import Player, Team
from Types.Game import Game


def play_chess():
    board: Board = Board()
    player_1 = Player()
    player_1.team = Team.WHITE
    player_2 = Player()
    player_2.team = Team.BLACK
    game: Game = Game(board, player_1, player_2)
    result_game: Game | None = game
    while not result_game.is_checkmate():
        result_game = game.monte_carlo().value
    print('WHITE' if result_game.turn == Team.WHITE else 'BLACK')


if __name__ == '__main__':
    play_chess()
