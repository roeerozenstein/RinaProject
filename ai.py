import copy
import math

class AIPlayer:
    def __init__(self, symbol, max_depth=3):
        self.symbol = symbol
        self.opponent = 'X' if symbol == 'O' else 'O'
        self.max_depth = max_depth

    def get_move(self, board):  # board = BigBoard
        best_score = -math.inf
        best_move = None

        for r in range(3):
            for c in range(3):
                sb = board.small_boards[r][c]
                if board.active_board and (r, c) != board.active_board:
                    continue
                if sb.winner:
                    continue
                for i in range(3):
                    for j in range(3):
                        if sb.grid[i][j] == '':
                            # העתק מצב
                            new_board = copy.deepcopy(board)
                            new_board.small_boards[r][c].grid[i][j] = self.symbol
                            new_board.small_boards[r][c].check_winner()
                            new_board.active_board = (i, j)
                            if new_board.small_boards[i][j].winner:
                                new_board.active_board = None
                            new_board.check_winner()

                            score = self.minimax(new_board, self.max_depth - 1, False, -math.inf, math.inf)

                            if score > best_score:
                                best_score = score
                                best_move = (r, c, i, j)

        return best_move


    def minimax(self, board, depth, maximizing, alpha, beta):
        if depth == 0 or board.winner:
            return self.evaluate(board)

        symbol = self.symbol if maximizing else self.opponent
        best_score = -math.inf if maximizing else math.inf

        for r in range(3):
            for c in range(3):
                sb = board.small_boards[r][c]
                if board.active_board and (r, c) != board.active_board:
                    continue
                if sb.winner:
                    continue
                for i in range(3):
                    for j in range(3):
                        if sb.grid[i][j] == '':
                            new_board = copy.deepcopy(board)
                            new_board.small_boards[r][c].grid[i][j] = symbol
                            new_board.small_boards[r][c].check_winner()
                            new_board.active_board = (i, j)
                            if new_board.small_boards[i][j].winner:
                                new_board.active_board = None
                            new_board.check_winner()

                            score = self.minimax(new_board, depth - 1, not maximizing, alpha, beta)

                            if maximizing:
                                best_score = max(best_score, score)
                                alpha = max(alpha, score)
                            else:
                                best_score = min(best_score, score)
                                beta = min(beta, score)

                            if beta <= alpha:
                                return best_score
        return best_score


    def evaluate(self, board):
        if board.winner == self.symbol:
            return 1000
        elif board.winner == self.opponent:
            return -1000

        score = 0

        for r in range(3):
            for c in range(3):
                sb = board.small_boards[r][c]
                if sb.winner == self.symbol:
                    score += 10
                elif sb.winner == self.opponent:
                    score -= 10
        return score
