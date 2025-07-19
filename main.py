import pygame
from config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
from board import BigBoard, CELL_SIZE, PADDING
from ai import AIPlayer
ai = AIPlayer('O', max_depth = 4)


def reset_game():
    global big_board, current_player, deletes_left, ai
    big_board = BigBoard()
    current_player = 'X'
    deletes_left = {'X': 3, 'O': 3}
    ai = AIPlayer('O', max_depth=4)

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Ultimate Tic Tac Toe")
clock = pygame.time.Clock()

reset_game()


def show_start_screen():
    import math, random
    t = 0
    # טען את תמונת הרקע X_O.png
    try:
        bg_img = pygame.image.load('X_O.jpg').convert_alpha()
        bg_img = pygame.transform.smoothscale(bg_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
    except Exception as e:
        bg_img = None
    # לא צריך איקסים/עיגולים ברקע
    waiting = True
    while waiting:
        # הצג את התמונה על כל המסך
        if bg_img:
            img_surf = bg_img.copy()
            img_surf.set_alpha(180)
            screen.blit(img_surf, (0, 0))
        else:
            screen.fill((30, 34, 45))
        # כותרת עם צל קטן ומהבהב איטי מאוד
        # בחר גופן מגניב (Luckiest Guy, Impact, Comic Sans MS, Arial)
        for font_name in ['luckiestguy', 'impact', 'comicsansms', 'arial']:
            try:
                title_font = pygame.font.SysFont(font_name, 62, bold=True)
                button_font = pygame.font.SysFont(font_name, 28, bold=True)
                break
            except:
                continue
        # אפקט מהבהב איטי פי 5
        phase = (t/5) % 3
        if phase < 1:
            title_color = (52, 152, 219)  # כחול
        elif phase < 2:
            title_color = (102, 204, 255)  # תכלת
        else:
            title_color = (231, 76, 60)  # אדום
        title = title_font.render('Ultimate Tic Tac Toe', True, title_color)
        # צל קטן
        shadow = title_font.render('Ultimate Tic Tac Toe', True, (10,10,10))
        title_y = SCREEN_HEIGHT//2 - 60
        for dx,dy in [(-2,0),(2,0),(0,-2),(0,2),(0,0)]:
            if dx!=0 or dy!=0:
                screen.blit(shadow, (SCREEN_WIDTH//2 - title.get_width()//2 + dx, title_y + dy))
            else:
                screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, title_y))
        # כפתור START מודרני
        button_text = button_font.render('START', True, (255,255,255))
        button_w, button_h = 160, 50
        button_x, button_y = (SCREEN_WIDTH - button_w)//2, title_y + 80
        button_rect = pygame.Rect(button_x, button_y, button_w, button_h)
        mouse_pos = pygame.mouse.get_pos()
        if button_rect.collidepoint(mouse_pos):
            button_color = (102, 204, 255)  # כחול בהיר ב-hover
        else:
            button_color = (44, 62, 80)
        pygame.draw.rect(screen, button_color, button_rect, border_radius=16)
        pygame.draw.rect(screen, (52,152,219), button_rect, 3, border_radius=16)
        screen.blit(button_text, (button_x + (button_w - button_text.get_width()) // 2, button_y + (button_h - button_text.get_height()) // 2))
        pygame.display.flip()
        t += 0.04
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    waiting = False
show_start_screen()


def main():
    global current_player
    running = True
    while running:
        # רקע עדין
        screen.fill((230, 235, 245))

        # פס עליון לניקוד + כפתור RESTART
        TOP_BAR_HEIGHT = 50
        pygame.draw.rect(screen, (44, 62, 80), (0, 0, SCREEN_WIDTH, TOP_BAR_HEIGHT), border_radius=0)
        # ניקוד
        font = pygame.font.SysFont('arial', 24, bold=True)
        text_x = font.render(f"X deletes left: {deletes_left['X']}", True, (52, 152, 219))
        text_o = font.render(f"O deletes left: {deletes_left['O']}", True, (231, 76, 60))
        screen.blit(text_x, (30, 10))
        screen.blit(text_o, (30 + text_x.get_width() + 30, 10))
        # כפתור RESTART עם אפקט hover
        button_font = pygame.font.SysFont('arial', 22, bold=True)
        button_text = button_font.render("RESTART", True, (255,255,255))
        button_w, button_h = 110, 32
        button_x, button_y = SCREEN_WIDTH - button_w - 20, 9
        button_rect = pygame.Rect(button_x, button_y, button_w, button_h)
        shadow_rect = button_rect.move(2, 2)
        pygame.draw.rect(screen, (30, 30, 30), shadow_rect, border_radius=8)
        mouse_pos = pygame.mouse.get_pos()
        if button_rect.collidepoint(mouse_pos):
            button_color = (0, 120, 255)  # כחול ניאון ב-hover
            # אפקט זוהר תואם לגודל הכפתור
            glow_surf = pygame.Surface((button_w, button_h), pygame.SRCALPHA)
            for i in range(8, 0, -2):
                pygame.draw.rect(glow_surf, (0, 200, 255, 60), (i, i, button_w-2*i, button_h-2*i), border_radius=8)
            screen.blit(glow_surf, (button_x, button_y), special_flags=pygame.BLEND_RGBA_ADD)
        else:
            button_color = (0, 60, 120)  # כחול עמוק רגיל
        pygame.draw.rect(screen, button_color, button_rect, border_radius=8)
        # מסגרת תכלת זוהרת
        border_color = (0, 255, 255)
        pygame.draw.rect(screen, border_color, button_rect, 3, border_radius=8)
        screen.blit(button_text, (button_x + (button_w - button_text.get_width()) // 2, button_y + (button_h - button_text.get_height()) // 2))
        # (הסרתי את כפתור SHOW TIE MESSAGE וכל הלוגיקה שלו)

        # מסגרת דקה מתחת לפס
        pygame.draw.line(screen, (189, 195, 199), (0, TOP_BAR_HEIGHT), (SCREEN_WIDTH, TOP_BAR_HEIGHT), 3)

        # הלוח עצמו - ממורכז אנכית מתחת לפס
        board_offset_y = TOP_BAR_HEIGHT + 10
        big_board.draw(screen, offset_y=board_offset_y)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                # בדוק אם נלחץ כפתור RESTART
                if button_rect.collidepoint(pos):
                    reset_game()
                    continue
                board_offset_y = TOP_BAR_HEIGHT + 20
                adj_pos = (pos[0], pos[1] - board_offset_y)
                if event.button == 1:  # לחיצה רגילה - משחק רגיל
                    played = big_board.handle_click(adj_pos, current_player)
                    if played:
                        # עדכן מהלך אחרון
                        for r in range(3):
                            for c in range(3):
                                offset_x = c * 3 * CELL_SIZE + (c + 1) * PADDING
                                offset_y = r * 3 * CELL_SIZE + (r + 1) * PADDING
                                cell_x = (adj_pos[0] - offset_x) // CELL_SIZE
                                cell_y = (adj_pos[1] - offset_y) // CELL_SIZE
                                if 0 <= cell_x < 3 and 0 <= cell_y < 3:
                                    if big_board.small_boards[r][c].grid[cell_y][cell_x] == current_player:
                                        big_board.last_move = (r, c, cell_y, cell_x)
                        current_player = 'O' if current_player == 'X' else 'X'

                elif event.button == 3:  # כפתור ימני - ניסיון למחוק סמל
                    if deletes_left[current_player] > 0:
                        deleted = big_board.handle_delete(adj_pos, current_player)
                        if deleted:
                            # עדכן מהלך אחרון
                            for r in range(3):
                                for c in range(3):
                                    offset_x = c * 3 * CELL_SIZE + (c + 1) * PADDING
                                    offset_y = r * 3 * CELL_SIZE + (r + 1) * PADDING
                                    cell_x = (adj_pos[0] - offset_x) // CELL_SIZE
                                    cell_y = (adj_pos[1] - offset_y) // CELL_SIZE
                                    if 0 <= cell_x < 3 and 0 <= cell_y < 3:
                                        big_board.last_move = (r, c, cell_y, cell_x)
                            deletes_left[current_player] -= 1
                            current_player = 'O' if current_player == 'X' else 'X'

            elif event.type == pygame.USEREVENT and current_player == 'O_WAITING':
                move = ai.get_move(big_board, deletes_left)
                if move:
                    action, r, c, i, j = move
                    sb = big_board.small_boards[r][c]
                    if action == 'place' and sb.grid[i][j] == '':
                        sb.grid[i][j] = 'O'
                        sb.check_winner()
                        big_board.check_winner()
                        big_board.active_board = (i, j)
                        if big_board.small_boards[i][j].winner:
                            big_board.active_board = None
                        big_board.last_move = (r, c, i, j)
                        current_player = 'X'
                        pygame.time.set_timer(pygame.USEREVENT, 0)
                    elif action == 'delete' and sb.grid[i][j] == 'X' and deletes_left['O'] > 0:
                        sb.grid[i][j] = ''
                        sb.check_winner()
                        big_board.check_winner()
                        big_board.active_board = (i, j)
                        if big_board.small_boards[i][j].winner:
                            big_board.active_board = None
                        big_board.last_move = (r, c, i, j)
                        deletes_left['O'] -= 1
                        current_player = 'X'
                        pygame.time.set_timer(pygame.USEREVENT, 0)
                else:
                    # אין מהלך חוקי - עבור ל-X או סיים משחק
                    current_player = 'X'
                    pygame.time.set_timer(pygame.USEREVENT, 0)
       
        if current_player == 'O' and not big_board.winner:
            pygame.time.set_timer(pygame.USEREVENT, 300)  # הפעל אירוע מותאם אישית לאחר 300ms
            current_player = 'O_WAITING'  # מצב ביניים: מחכים לסוכן

  
        
        # הודעת סיום משחק יפה
        if big_board.winner or not big_board.has_any_available_board():
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((44, 62, 80, 180))
            screen.blit(overlay, (0, 0))
            font = pygame.font.SysFont('arial', 64, bold=True)
            if big_board.winner:
                msg = f"{big_board.winner} wins!"
                color = (231, 76, 60) if big_board.winner == 'O' else (52, 152, 219)
                # צל
                text = font.render(msg, True, (30, 30, 30))
                text_rect = text.get_rect(center=(SCREEN_WIDTH // 2 + 4, SCREEN_HEIGHT // 2 + 4))
                screen.blit(text, text_rect)
                # טקסט צבעוני
                text = font.render(msg, True, color)
                text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
                screen.blit(text, text_rect)
            else:
                small_font = pygame.font.SysFont('arial', 44, bold=True)
                msg1 = "It's a tie!"
                msg2 = "Nobody wins this round"
                color = (241, 196, 15)
                # צל
                text1 = small_font.render(msg1, True, (30, 30, 30))
                text2 = small_font.render(msg2, True, (30, 30, 30))
                text1_rect = text1.get_rect(center=(SCREEN_WIDTH // 2 + 4, SCREEN_HEIGHT // 2 - 24 + 4))
                text2_rect = text2.get_rect(center=(SCREEN_WIDTH // 2 + 4, SCREEN_HEIGHT // 2 + 24 + 4))
                screen.blit(text1, text1_rect)
                screen.blit(text2, text2_rect)
                # טקסט צבעוני
                text1 = small_font.render(msg1, True, color)
                text2 = small_font.render(msg2, True, color)
                text1_rect = text1.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 24))
                text2_rect = text2.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 24))
                screen.blit(text1, text1_rect)
                screen.blit(text2, text2_rect)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()