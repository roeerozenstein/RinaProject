import pygame
from config import BLACK, GRAY
from config import SCREEN_WIDTH, SCREEN_HEIGHT

CELL_SIZE = 64
PADDING = 5

class SmallBoard:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.grid = [['' for _ in range(3)] for _ in range(3)]
        self.winner = None

    def check_winner(self):
        lines = []

        # שורות וטורים
        lines.extend(self.grid)  # שורות
        lines.extend([[self.grid[r][c] for r in range(3)] for c in range(3)])  # טורים

        # אלכסונים
        lines.append([self.grid[i][i] for i in range(3)])
        lines.append([self.grid[i][2 - i] for i in range(3)])

        for line in lines:
            if line[0] != '' and all(cell == line[0] for cell in line):
                self.winner = line[0]
                return self.winner
        return None

    def draw(self, surface, offset_x, offset_y):
        for i in range(4):
            pygame.draw.line(surface, GRAY,
                             (offset_x, offset_y + i * CELL_SIZE),
                             (offset_x + 3 * CELL_SIZE, offset_y + i * CELL_SIZE), 2)
            pygame.draw.line(surface, GRAY,
                             (offset_x + i * CELL_SIZE, offset_y),
                             (offset_x + i * CELL_SIZE, offset_y + 3 * CELL_SIZE), 2)
            
        if self.winner:
            # ציור סמל גדול במרכז הלוח
            color = (52, 152, 219) if self.winner == 'X' else (231, 76, 60)
            font = pygame.font.SysFont(None, 90)
            text = font.render(self.winner, True, color)
            text_rect = text.get_rect(center=(offset_x + 1.5 * CELL_SIZE, offset_y + 1.5 * CELL_SIZE))
            surface.blit(text, text_rect)
            return

        # ציור סמלים
        font = pygame.font.SysFont(None, 40)
        for r in range(3):
            for c in range(3):
                symbol = self.grid[r][c]
                if symbol != '':
                    color = (52, 152, 219) if symbol == 'X' else (231, 76, 60)
                    text = font.render(symbol, True, color)
                    x = offset_x + c * CELL_SIZE + CELL_SIZE // 3
                    y = offset_y + r * CELL_SIZE + CELL_SIZE // 4
                    surface.blit(text, (x, y))

    def handle_click(self, pos, offset_x, offset_y, current_player):
        x, y = pos
        if not (offset_x <= x <= offset_x + 3 * CELL_SIZE and offset_y <= y <= offset_y + 3 * CELL_SIZE):
            return False  # לא בתוך הלוח הזה

        col = (x - offset_x) // CELL_SIZE
        row = (y - offset_y) // CELL_SIZE

        if self.grid[row][col] == '':
            self.grid[row][col] = current_player
            self.check_winner()
            return True  # הצליח
        return False  # כבר תפוס

class BigBoard:
    def __init__(self):
        self.small_boards = [[SmallBoard(r, c) for c in range(3)] for r in range(3)]
        self.winner = None
        self.active_board = None  
        self.last_move = None  # (r, c, i, j)


    def check_winner(self):
        lines = []

        # שורות
        lines.extend([[self.small_boards[r][c].winner for c in range(3)] for r in range(3)])

        # טורים
        lines.extend([[self.small_boards[r][c].winner for r in range(3)] for c in range(3)])

        # אלכסונים
        lines.append([self.small_boards[i][i].winner for i in range(3)])
        lines.append([self.small_boards[i][2 - i].winner for i in range(3)])

        for line in lines:
            if line[0] and all(cell == line[0] for cell in line):
                self.winner = line[0]
                return self.winner

        return None

    def draw(self, surface, offset_x=0, offset_y=0):
        # Neon style colors
        NEON_RED = (255, 40, 40)
        NEON_BLUE = (0, 200, 255)
        DARK_BG = (20, 20, 40)
        GLOW_ALPHA = 90
        # Fill background (if this is the main board)
        if offset_x == 0 and offset_y == 0:
            surface.fill(DARK_BG)
        for r in range(3):
            for c in range(3):
                bx = c * 3 * CELL_SIZE + (c + 1) * PADDING + offset_x
                by = r * 3 * CELL_SIZE + (r + 1) * PADDING + offset_y
                # Draw neon glow for main board border only
                if offset_x == 0 and offset_y == 0:
                    glow_surf = pygame.Surface((3*CELL_SIZE+8, 3*CELL_SIZE+8), pygame.SRCALPHA)
                    for i in range(12, 0, -3):
                        pygame.draw.rect(glow_surf, (*NEON_BLUE, GLOW_ALPHA), (4-i, 4-i, 3*CELL_SIZE+8+2*i, 3*CELL_SIZE+8+2*i), border_radius=18)
                    surface.blit(glow_surf, (bx-4, by-4), special_flags=pygame.BLEND_RGBA_ADD)
                # Draw main border
                pygame.draw.rect(surface, NEON_BLUE, (bx, by, 3*CELL_SIZE, 3*CELL_SIZE), 4, border_radius=14)
                # Highlight active board(s)
                highlight_this = False
                if self.active_board is not None:
                    if (r, c) == self.active_board:
                        highlight_this = True
                else:
                    # highlight all available boards
                    if self.small_boards[r][c].winner is None and not self.is_board_full(r, c):
                        highlight_this = True
                if highlight_this:
                    active_glow = pygame.Surface((3*CELL_SIZE+16, 3*CELL_SIZE+16), pygame.SRCALPHA)
                    for i in range(18, 0, -3):
                        pygame.draw.rect(active_glow, (*NEON_BLUE, 120), (8-i, 8-i, 3*CELL_SIZE+16+2*i, 3*CELL_SIZE+16+2*i), border_radius=22)
                    surface.blit(active_glow, (bx-8, by-8), special_flags=pygame.BLEND_RGBA_ADD)
                    pygame.draw.rect(surface, NEON_BLUE, (bx-2, by-2, 3*CELL_SIZE+4, 3*CELL_SIZE+4), 6, border_radius=16)
                # Highlight last move (neon green, but only as a border)
                if self.last_move and (r, c) == (self.last_move[0], self.last_move[1]):
                    i, j = self.last_move[2], self.last_move[3]
                    cell_rect = (bx + j * CELL_SIZE, by + i * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                    pygame.draw.rect(surface, (102,255,102), cell_rect, 5, border_radius=8)
                # Draw the small board
                self.small_boards[r][c].draw(surface, bx, by)
                # Draw thin neon cell lines (inside small board)
                for i in range(1, 3):
                    # Vertical
                    pygame.draw.line(surface, NEON_BLUE, (bx + i*CELL_SIZE, by), (bx + i*CELL_SIZE, by + 3*CELL_SIZE), 2)
                    # Horizontal
                    pygame.draw.line(surface, NEON_BLUE, (bx, by + i*CELL_SIZE), (bx + 3*CELL_SIZE, by + i*CELL_SIZE), 2)
        # Draw thick neon lines between boards
        for i in range(1, 3):
            glow_line = pygame.Surface((surface.get_width(), 12), pygame.SRCALPHA)
            for k in range(10, 0, -2):
                pygame.draw.line(glow_line, (*NEON_BLUE, 60), (0, 6), (surface.get_width(), 6), 12-k)
            surface.blit(glow_line, (0, offset_y + i * (3 * CELL_SIZE + PADDING) - 6), special_flags=pygame.BLEND_RGBA_ADD)
            pygame.draw.line(surface, NEON_BLUE, (offset_x, offset_y + i * (3 * CELL_SIZE + PADDING)), (offset_x + 3 * 3 * CELL_SIZE + 4 * PADDING, offset_y + i * (3 * CELL_SIZE + PADDING)), 6)
            glow_line2 = pygame.Surface((12, surface.get_height()), pygame.SRCALPHA)
            for k in range(10, 0, -2):
                pygame.draw.line(glow_line2, (*NEON_BLUE, 60), (6, 0), (6, surface.get_height()), 12-k)
            surface.blit(glow_line2, (offset_x + i * (3 * CELL_SIZE + PADDING) - 6, 0), special_flags=pygame.BLEND_RGBA_ADD)
            pygame.draw.line(surface, NEON_BLUE, (offset_x + i * (3 * CELL_SIZE + PADDING), offset_y), (offset_x + i * (3 * CELL_SIZE + PADDING), offset_y + 3 * 3 * CELL_SIZE + 4 * PADDING), 6)

    def is_board_full(self, r, c):
        sb = self.small_boards[r][c]
        for row in sb.grid:
            for cell in row:
                if cell == '':
                    return False
        return True

    def handle_click(self, pos, current_player):
        if self.winner:
            return False
        # בדוק אם הלוח הפעיל תפוס (מלא או ניצח), ואם כן אפשר לשחק בכל לוח פתוח
        if self.active_board:
            r, c = self.active_board
            if self.small_boards[r][c].winner is not None or self.is_board_full(r, c):
                allowed_boards = None  # כל לוח פתוח
            else:
                allowed_boards = [self.active_board]
        else:
            allowed_boards = None  # כל לוח פתוח
        for r in range(3):
            for c in range(3):
                # אם יש לוח פעיל (והוא לא תפוס) – נוודא שרק בו אפשר לשחק
                if allowed_boards is not None and (r, c) not in allowed_boards:
                    continue
                offset_x = c * 3 * CELL_SIZE + (c + 1) * PADDING
                offset_y = r * 3 * CELL_SIZE + (r + 1) * PADDING
                success = self.small_boards[r][c].handle_click(pos, offset_x, offset_y, current_player)
                if success:
                    self.check_winner()
                    # קובע את הלוח הבא לפי התא שנבחר
                    cell_x = (pos[0] - offset_x) // CELL_SIZE
                    cell_y = (pos[1] - offset_y) // CELL_SIZE
                    next_board = (cell_y, cell_x)
                    # אם הלוח הבא כבר נגמר או מלא – נאפשר שחק בכל לוח פתוח
                    if self.small_boards[cell_y][cell_x].winner is not None or self.is_board_full(cell_y, cell_x):
                        self.active_board = None
                    else:
                        self.active_board = next_board
                    self.last_move = (r, c, cell_y, cell_x)
                    return True
        return False
    
    def handle_delete(self, pos, current_player):
        if self.winner:
            return False
        for r in range(3):
            for c in range(3):
                offset_x = c * 3 * CELL_SIZE + (c + 1) * PADDING
                offset_y = r * 3 * CELL_SIZE + (r + 1) * PADDING
                board = self.small_boards[r][c]
                if board.winner:
                    continue  # לא למחוק בלוח שנגמר
                cell_x = (pos[0] - offset_x) // CELL_SIZE
                cell_y = (pos[1] - offset_y) // CELL_SIZE
                if 0 <= cell_x < 3 and 0 <= cell_y < 3:
                    symbol = board.grid[cell_y][cell_x]
                    if symbol != '' and symbol != current_player:
                        board.grid[cell_y][cell_x] = ''
                        board.check_winner()  # אולי כבר לא ניצחון
                        self.active_board = (cell_y, cell_x)
                        if self.small_boards[cell_y][cell_x].winner is not None or self.is_board_full(cell_y, cell_x):
                            self.active_board = None
                        self.last_move = (r, c, cell_y, cell_x)
                        return True
        return False

