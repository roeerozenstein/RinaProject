import copy
import math

class AIPlayer:
    def __init__(self, symbol, max_depth=5):
        self.symbol = symbol
        self.opponent = 'X' if symbol == 'O' else 'O'
        self.max_depth = max_depth

    def get_move(self, board, deletes_left):
        best_score = -math.inf
        best_move = None
        # בדוק גם מהלכי הנחה וגם מחיקה
        for r in range(3):
            for c in range(3):
                sb = board.small_boards[r][c]
                # מותר לשחק רק בלוח הפעיל, אלא אם אין לוח פעיל (תור ראשון או לוח סגור)
                if board.active_board and (r, c) != board.active_board:
                    continue
                if sb.winner:
                    continue
                for i in range(3):
                    for j in range(3):
                        # מהלך הנחה
                        if sb.grid[i][j] == '':
                            new_board = copy.deepcopy(board)
                            new_deletes = deletes_left.copy()
                            new_board.small_boards[r][c].grid[i][j] = self.symbol
                            new_board.small_boards[r][c].check_winner()
                            new_board.active_board = (i, j)
                            if new_board.small_boards[i][j].winner:
                                new_board.active_board = None
                            new_board.check_winner()
                            score = self.minimax(new_board, new_deletes, self.max_depth - 1, False, -math.inf, math.inf)
                            if score > best_score:
                                best_score = score
                                best_move = ('place', r, c, i, j)
                        # מהלך מחיקה
                        elif sb.grid[i][j] == self.opponent and deletes_left[self.symbol] > 0:
                            if deletes_left[self.symbol] == 0:
                                continue
                            new_board = copy.deepcopy(board)
                            new_deletes = deletes_left.copy()
                            new_board.small_boards[r][c].grid[i][j] = ''
                            new_board.small_boards[r][c].check_winner()
                            new_board.active_board = (i, j)
                            if new_board.small_boards[i][j].winner:
                                new_board.active_board = None
                            new_board.check_winner()
                            new_deletes[self.symbol] -= 1
                            score = self.minimax(new_board, new_deletes, self.max_depth - 1, False, -math.inf, math.inf)
                            if score > best_score:
                                best_score = score
                                best_move = ('delete', r, c, i, j)
        return best_move

    def minimax(self, board, deletes_left, depth, maximizing, alpha, beta):
        if depth == 0 or board.winner:
            return self.evaluate(board, deletes_left)
        symbol = self.symbol if maximizing else self.opponent
        opponent = self.opponent if maximizing else self.symbol
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
                        # מהלך הנחה
                        if sb.grid[i][j] == '':
                            new_board = copy.deepcopy(board)
                            new_deletes = deletes_left.copy()
                            new_board.small_boards[r][c].grid[i][j] = symbol
                            new_board.small_boards[r][c].check_winner()
                            new_board.active_board = (i, j)
                            if new_board.small_boards[i][j].winner:
                                new_board.active_board = None
                            new_board.check_winner()
                            score = self.minimax(new_board, new_deletes, depth - 1, not maximizing, alpha, beta)
                            if maximizing:
                                best_score = max(best_score, score)
                                alpha = max(alpha, score)
                            else:
                                best_score = min(best_score, score)
                                beta = min(beta, score)
                            if beta <= alpha:
                                return best_score
                        # מהלך מחיקה
                        elif sb.grid[i][j] == opponent and deletes_left[symbol] > 0:
                            if deletes_left[symbol] == 0:
                                continue
                            new_board = copy.deepcopy(board)
                            new_deletes = deletes_left.copy()
                            new_board.small_boards[r][c].grid[i][j] = ''
                            new_board.small_boards[r][c].check_winner()
                            new_board.active_board = (i, j)
                            if new_board.small_boards[i][j].winner:
                                new_board.active_board = None
                            new_board.check_winner()
                            new_deletes[symbol] -= 1
                            score = self.minimax(new_board, new_deletes, depth - 1, not maximizing, alpha, beta)
                            if maximizing:
                                best_score = max(best_score, score)
                                alpha = max(alpha, score)
                            else:
                                best_score = min(best_score, score)
                                beta = min(beta, score)
                            if beta <= alpha:
                                return best_score
        return best_score

    def count_open_lines_small(self, sb, symbol):
        open_lines = 0
        # Rows
        for row in sb.grid:
            if all(cell == symbol or cell == '' for cell in row):
                open_lines += 1
        # Columns
        for c in range(3):
            col = [sb.grid[r][c] for r in range(3)]
            if all(cell == symbol or cell == '' for cell in col):
                open_lines += 1
        # Diagonals
        diag1 = [sb.grid[i][i] for i in range(3)]
        if all(cell == symbol or cell == '' for cell in diag1):
            open_lines += 1
        diag2 = [sb.grid[i][2 - i] for i in range(3)]
        if all(cell == symbol or cell == '' for cell in diag2):
            open_lines += 1
        return open_lines

    def count_open_lines_big(self, board, symbol):
        open_lines = 0
        # Prepare a 3x3 grid representing the big board (winner or None)
        grid = [[board.small_boards[r][c].winner for c in range(3)] for r in range(3)]
        # Rows
        for row in grid:
            if all(cell == symbol or cell is None for cell in row):
                open_lines += 1
        # Columns
        for c in range(3):
            col = [grid[r][c] for r in range(3)]
            if all(cell == symbol or cell is None for cell in col):
                open_lines += 1
        # Diagonals
        diag1 = [grid[i][i] for i in range(3)]
        if all(cell == symbol or cell is None for cell in diag1):
            open_lines += 1
        diag2 = [grid[i][2 - i] for i in range(3)]
        if all(cell == symbol or cell is None for cell in diag2):
            open_lines += 1
        return open_lines

    def evaluate(self, board, deletes_left):
        if board.winner == self.symbol:
            return 1000
        elif board.winner == self.opponent:
            return -1000

        score = 0
        # ניקוד על מחיקות שנותרו
        score += deletes_left[self.symbol] * 5
        # יתרון בלוח הגדול
        my_big = self.count_open_lines_big(board, self.symbol)
        opp_big = self.count_open_lines_big(board, self.opponent)
        score += 20 * (my_big - opp_big)
        # יתרון בלוחות הקטנים
        for r in range(3):
            for c in range(3):
                sb = board.small_boards[r][c]
                if sb.winner == self.symbol:
                    score += 10
                elif sb.winner == self.opponent:
                    score -= 10
                else:
                    my_lines = self.count_open_lines_small(sb, self.symbol)
                    opp_lines = self.count_open_lines_small(sb, self.opponent)
                    score += my_lines - opp_lines
        return score


