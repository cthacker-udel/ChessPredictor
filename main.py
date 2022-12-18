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
    print("Hello")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    play_chess()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
