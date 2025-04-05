from Board import Board
from player import Player

def utility(board: Board, player: Player, opponent: Player) -> int:

    return board.count_pieces(player) - board.count_pieces(opponent)