import pygame
import sys
import copy
import random
from ultimate_tic_tac_toe import check_tris, game_tie, minimax, update_board, compute_min_sub_board_coordinates, get_sub_board_from_coordinates, update_macro_board, compute_valid_coordinates

# --- Pygame Setup ---
pygame.init()

SIZE = 600
CELL_SIZE = SIZE // 9
SUB_SIZE = SIZE // 3
LINE_COLOR = (0, 0, 0)
BG_COLOR = (255, 255, 255)
X_COLOR = (200, 0, 0)
O_COLOR = (0, 0, 200)
HIGHLIGHT_COLOR = (200, 200, 0)
FONT = pygame.font.SysFont(None, 36)
LIGHT_BLUE = (173, 216, 230)
BIG_FONT = pygame.font.SysFont(None, 72)
LAST_MOVE_COLOR = (255, 140, 0)  # Orange
LAST_MOVE_FONT = pygame.font.SysFont(None, 60)

screen = pygame.display.set_mode((SIZE, SIZE))
pygame.display.set_caption('Ultimate Tic-Tac-Toe: Human vs AI')

# --- Game State ---
macro_board = [['' for _ in range(3)] for _ in range(3)]
board = [['' for _ in range(9)] for _ in range(9)]
current_player = 'X'  # Human is X, AI is O
active_sub = None  # (row, col) of active sub-board, or None if any
last_move = None  # (row, col) of the last move

def draw_board():
    screen.fill(BG_COLOR)
    # Draw sub-board highlights
    if active_sub:
        x, y = active_sub
        pygame.draw.rect(screen, HIGHLIGHT_COLOR, (y*SUB_SIZE, x*SUB_SIZE, SUB_SIZE, SUB_SIZE))
    # Draw sub-boards
    for sub_i in range(3):
        for sub_j in range(3):
            mark = macro_board[sub_i][sub_j]
            sub_x, sub_y = sub_j*SUB_SIZE, sub_i*SUB_SIZE
            if mark:
                # Fill sub-board with light blue
                pygame.draw.rect(screen, LIGHT_BLUE, (sub_x, sub_y, SUB_SIZE, SUB_SIZE))
                # Draw winner in the center
                if mark in ['X', 'O']:
                    text = BIG_FONT.render(mark, True, X_COLOR if mark == 'X' else O_COLOR)
                else:
                    text = BIG_FONT.render('.', True, (100,100,100))
                rect = text.get_rect(center=(sub_x+SUB_SIZE//2, sub_y+SUB_SIZE//2))
                screen.blit(text, rect)
    # Draw grid
    for i in range(10):
        lw = 4 if i % 3 == 0 else 1
        pygame.draw.line(screen, LINE_COLOR, (0, i*CELL_SIZE), (SIZE, i*CELL_SIZE), lw)
        pygame.draw.line(screen, LINE_COLOR, (i*CELL_SIZE, 0), (i*CELL_SIZE, SIZE), lw)
    # Draw X/O only in unfinished sub-boards
    for i in range(9):
        for j in range(9):
            sub_i, sub_j = i//3, j//3
            if not macro_board[sub_i][sub_j] and board[i][j]:
                if last_move == (i, j):
                    color = LAST_MOVE_COLOR
                    font = LAST_MOVE_FONT
                else:
                    color = X_COLOR if board[i][j] == 'X' else O_COLOR
                    font = FONT
                text = font.render(board[i][j], True, color)
                rect = text.get_rect(center=(j*CELL_SIZE+CELL_SIZE//2, i*CELL_SIZE+CELL_SIZE//2))
                screen.blit(text, rect)
    pygame.display.flip()

def get_active_sub(valid_moves):
    x_set = set([coord[0]//3 for coord in valid_moves])
    y_set = set([coord[1]//3 for coord in valid_moves])
    if len(x_set) == 1 and len(y_set) == 1:
        return (list(x_set)[0], list(y_set)[0])
    return None

def get_valid_moves():
    valid = compute_valid_coordinates(board)
    if active_sub:
        # If the sub-board is finished, allow any valid move
        if macro_board[active_sub[0]][active_sub[1]]:
            return valid
        min_x, min_y = active_sub[0]*3, active_sub[1]*3
        valid = [c for c in valid if min_x <= c[0] < min_x+3 and min_y <= c[1] < min_y+3]
    return valid

def ai_move():
    global active_sub
    valid_moves = get_valid_moves()
    print('AI valid_moves:', valid_moves)
    if not valid_moves:
        print('No valid moves for AI')
        return None  # No valid moves, likely a tie
    move = None
    if active_sub and not macro_board[active_sub[0]][active_sub[1]]:
        min_x, min_y = active_sub[0]*3, active_sub[1]*3
        sub_board = get_sub_board_from_coordinates(board, min_x, min_y)
        move = minimax(True, copy.deepcopy(sub_board))
        print('AI minimax (sub_board) move:', move)
        if isinstance(move, list) and len(move) == 2:
            move = [move[0]+min_x, move[1]+min_y]
    else:
        move = minimax(True, copy.deepcopy(board))
        print('AI minimax (full board) move:', move)
    # Ensure the move is valid and well-formed
    if not (isinstance(move, list) and len(move) == 2 and all(isinstance(x, int) for x in move)):
        print('AI move from minimax is invalid, picking random')
        move = random.choice(valid_moves)
    if move not in valid_moves:
        print('AI move not in valid_moves, picking random')
        move = random.choice(valid_moves)
    print('AI final move:', move)
    update_board('O', move, board)
    update_macro_board('O', move, macro_board, board)
    return move

def check_game_end():
    for player in ['X', 'O']:
        if check_tris(player, macro_board):
            return player
    if game_tie(macro_board):
        return 'Tie'
    return None

def main():
    global current_player, active_sub, last_move
    running = True
    winner = None
    while running:
        draw_board()
        if winner:
            msg = f"Winner: {winner}" if winner != 'Tie' else "It's a tie!"
            text = FONT.render(msg, True, (0,150,0))
            rect = text.get_rect(center=(SIZE//2, SIZE//2))
            screen.blit(text, rect)
            pygame.display.flip()
            pygame.time.wait(3000)
            running = False
            continue
        if current_player == 'X':
            # Human turn
            valid_moves = get_valid_moves()
            print('USER valid_moves:', valid_moves)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    row, col = y//CELL_SIZE, x//CELL_SIZE
                    if [row, col] in valid_moves:
                        update_board('X', [row, col], board)
                        update_macro_board('X', [row, col], macro_board, board)
                        last_move = (row, col)
                        print('USER final move:', [row, col])
                        # Set next active sub-board
                        active_sub = (row%3, col%3)
                        if macro_board[active_sub[0]][active_sub[1]]:
                            active_sub = None
                        current_player = 'O'
                        winner = check_game_end()
        else:
            # AI turn
            pygame.time.wait(500)
            move = ai_move()
            if move is None:
                winner = check_game_end()
                continue
            last_move = tuple(move)
            active_sub = (move[0]%3, move[1]%3)
            if macro_board[active_sub[0]][active_sub[1]]:
                active_sub = None
            current_player = 'X'
            winner = check_game_end()
    pygame.quit()

if __name__ == '__main__':
    main() 