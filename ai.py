import copy
import math

class AIPlayer:
    def __init__(self, symbol, max_depth=3):
        self.symbol = symbol
        self.opponent = 'X' if symbol == 'O' else 'O'
        self.max_depth = max_depth

    def get_move(self, board, deletes_left=None): #board = big board
        # אם הלוח הפעיל כבר נגמר – אפשר לשחק בכל לוח
        if board.active_board:
            r, c = board.active_board
            if board.small_boards[r][c].winner is not None:
                board.active_board = None

        self.deletes_left = deletes_left  # שמירה זמנית

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
                        cell = sb.grid[i][j]

                        if cell == '':
                            # מהלך רגיל – הנחת סמל
                            new_board = copy.deepcopy(board)
                            new_board.small_boards[r][c].grid[i][j] = self.symbol
                            new_board.small_boards[r][c].check_winner()
                            new_board.active_board = (i, j)
                            if new_board.small_boards[i][j].winner:
                                new_board.active_board = None
                            new_board.check_winner()
                            new_board.deletes_left = copy.deepcopy(board.deletes_left)

                            score = self.minimax(new_board, self.max_depth - 1, False, -math.inf, math.inf)

                            if score > best_score:
                                best_score = score
                                best_move = (r, c, i, j, 'place')

                        elif (
                            cell == self.opponent
                            and board.deletes_left
                            and board.deletes_left[self.symbol] > 0
                        ):
                            # מהלך מחיקה
                            new_board = copy.deepcopy(board)
                            new_board.small_boards[r][c].grid[i][j] = ''
                            new_board.deletes_left = copy.deepcopy(board.deletes_left)
                            new_board.deletes_left[self.symbol] -= 1
                            new_board.small_boards[r][c].check_winner()
                            new_board.check_winner()
                            new_board.active_board = None  # אחרי מחיקה – שחרר את הלוח

                            score = self.minimax(new_board, self.max_depth - 1, False, -math.inf, math.inf)

                            if score > best_score:
                                best_score = score
                                best_move = (r, c, i, j, 'delete')

        return best_move


    def minimax(self, board, depth, maximizing, alpha, beta):
        if depth == 0 or board.winner:
            return self.evaluate(board, getattr(board, 'deletes_left', None))


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


    def evaluate(self, board, deletes_left=None):

        if board.winner == self.symbol:
            return 10000
        elif board.winner == self.opponent:
            return -10000

        score = 0

        # 1. שליטה בלוחות הקטנים
        for r in range(3):
            for c in range(3):
                sb = board.small_boards[r][c]
                if sb.winner == self.symbol:
                    score += 300
                elif sb.winner == self.opponent:
                    score -= 300
                else:
                    # 2. התקדמות בלוחות הקטנים
                    score += self.evaluate_small_board(sb, self.symbol) * 2
                    score -= self.evaluate_small_board(sb, self.opponent)

        # 3. התקדמות בלוח הגדול (שניים ברצף)
        score += self.evaluate_big_lines(board, self.symbol)
        score -= self.evaluate_big_lines(board, self.opponent)

        # 4. שליטה באזורים חשובים
        score += self.control_key_areas(board, self.symbol)
        score -= self.control_key_areas(board, self.opponent)

        # 5. יתרון במחיקות שנותרו
        if deletes_left:
            my_deletes = deletes_left.get(self.symbol, 0)
            opp_deletes = deletes_left.get(self.opponent, 0)
            score += (my_deletes - opp_deletes) * 15


        return score
    

    def evaluate_small_board(self, sb, player):
        grid = sb.grid
        score = 0

        lines = []

        # שורות וטורים
        lines.extend(grid)
        lines.extend([[grid[r][c] for r in range(3)] for c in range(3)])

        # אלכסונים
        lines.append([grid[i][i] for i in range(3)])
        lines.append([grid[i][2 - i] for i in range(3)])

        for line in lines:
            if line.count(player) == 2 and line.count('') == 1:
                score += 10  # איום קרוב לניצחון
            elif line.count(player) == 1 and line.count('') == 2:
                score += 2  # פתיחה טובה

        return score


    def evaluate_big_lines(self, board, player):
        score = 0

        # נייצר "מפת שליטה" של הלוחות
        control = [[board.small_boards[r][c].winner for c in range(3)] for r in range(3)]

        lines = []
        lines.extend(control)  # שורות
        lines.extend([[control[r][c] for r in range(3)] for c in range(3)])  # טורים
        lines.append([control[i][i] for i in range(3)])  # אלכסון ראשי
        lines.append([control[i][2 - i] for i in range(3)])  # אלכסון משני

        for line in lines:
            if line.count(player) == 2 and line.count(None) == 1:
                score += 100  # איום ניצחון בלוח הגדול
            elif line.count(player) == 1 and line.count(None) == 2:
                score += 20

        return score

    
    def control_key_areas(self, board, player):
        score = 0

        # מרכז הלוח הגדול
        if board.small_boards[1][1].winner == player:
            score += 50

        # פינות
        for (r, c) in [(0, 0), (0, 2), (2, 0), (2, 2)]:
            if board.small_boards[r][c].winner == player:
                score += 30

        return score

