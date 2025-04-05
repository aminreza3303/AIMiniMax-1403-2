import copy
from player import Player
from Board import Board
from Action import doAction
from utility import *

class AI:
    MIN_VALUE = -1000000
    MAX_VALUE = 1000000

    def choose_action(self, board, player, opponent, max_depth):
        best_action = self.do_minimax(
            copy.deepcopy(board),
            copy.copy(player),
            copy.copy(opponent),
            max_depth,
        )
        return best_action

    def deepCopy(self, player, opponent, board) -> tuple[Player, Player, Board]:
        player_copy = copy.deepcopy(player)
        opponent_copy = copy.deepcopy(opponent)
        next_board = copy.deepcopy(board)
        return player_copy, opponent_copy, next_board

    def succesor(self, board: Board, player: Player, opponent: Player, reverse=False):
        if (reverse):
            actions = opponent.getValidActions(board)
        else:
            actions = player.getValidActions(board)

        result = []
        for action in actions:
            player_copy, opponent_copy, next_board = self.deepCopy(player, opponent, board)
            if (reverse):
                doAction(action, opponent_copy, next_board)
            else:
                doAction(action, player_copy, next_board)
            result.append([next_board, player_copy, opponent_copy, action])
            """" next board , player, opponent , action"""
        return result
    def do_minimax(self, board: Board, player: Player, opponent: Player, depth):

        value, state = self.max(board, player, opponent, depth)
        return state[3]

    def max(self, board, player, opponent, depth):
        if depth == 0 or player.terminal_test(board):
            return utility(board, player, opponent), [board, player, opponent, None]

        max_value = self.MIN_VALUE
        best_state = None

        successors = self.succesor(board, player, opponent)
        if not successors:
            return utility(board, player, opponent), [board, player, opponent, None]

        for next_board, next_player, next_opponent, action in successors:
            value, _ = self.min(next_board, next_player, next_opponent, depth - 1)
            if value > max_value:
                max_value = value
                best_state = [next_board, next_player, next_opponent, action]

        return max_value, best_state

    def min(self, board, player, opponent, depth):
        if depth == 0 or opponent.terminal_test(board):
            return utility(board, player, opponent), [board, player, opponent, None]

        min_value = self.MAX_VALUE
        best_state = None

        successors = self.succesor(board, player, opponent, reverse=True)
        if not successors:
            return utility(board, player, opponent), [board, player, opponent, None]

        for next_board, next_player, next_opponent, action in successors:
            value, _ = self.max(next_board, next_player, next_opponent, depth - 1)
            if value < min_value:
                min_value = value
                best_state = [next_board, next_player, next_opponent, action]

        return min_value, best_state