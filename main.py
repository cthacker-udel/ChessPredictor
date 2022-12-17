from Types.Board import Board
from Types.Player import Player, Team
from Types.Game import Game


def print_hi(name):
    board: Board = Board()
    player_1 = Player()
    player_1.team = Team.WHITE
    player_2 = Player()
    player_2.team = Team.BLACK
    game: Game = Game(board, player_1, player_2)
    result_game = game.monte_carlo()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
