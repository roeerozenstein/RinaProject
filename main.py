import pygame
from config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
from board import BigBoard
from ai import AIPlayer
ai = AIPlayer('O')



pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Advanced Tic Tac Toe")
clock = pygame.time.Clock()

big_board = BigBoard()
current_player = 'X'
deletes_left = {'X': 3, 'O': 3}


def main():
    global current_player
    running = True
    while running:
        screen.fill((255, 255, 255))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()

                if event.button == 1:  # לחיצה רגילה - משחק רגיל
                    played = big_board.handle_click(pos, current_player)
                    if played:
                        current_player = 'O' if current_player == 'X' else 'X'

                elif event.button == 3:  # כפתור ימני - ניסיון למחוק סמל
                    if deletes_left[current_player] > 0:
                        deleted = big_board.handle_delete(pos, current_player)
                        if deleted:
                            deletes_left[current_player] -= 1
                            current_player = 'O' if current_player == 'X' else 'X'

            elif event.type == pygame.USEREVENT and current_player == 'O_WAITING':
                move = ai.get_move(big_board)
                if move:
                    r, c, i, j = move
                    sb = big_board.small_boards[r][c]
                    if sb.grid[i][j] == '':
                        sb.grid[i][j] = 'O'
                        sb.check_winner()
                        big_board.check_winner()
                        big_board.active_board = (i, j)
                        if big_board.small_boards[i][j].winner:
                            big_board.active_board = None
                        current_player = 'X'
                        pygame.time.set_timer(pygame.USEREVENT, 0)  # בטל את הטיימר
       
        if current_player == 'O' and not big_board.winner:
            pygame.time.set_timer(pygame.USEREVENT, 300)  # הפעל אירוע מותאם אישית לאחר 300ms
            current_player = 'O_WAITING'  # מצב ביניים: מחכים לסוכן

  
        
        big_board.draw(screen)
        
        font = pygame.font.SysFont(None, 30)
        text_x = font.render(f"X deletes left: {deletes_left['X']}", True, (0, 0, 255))
        text_o = font.render(f"O deletes left: {deletes_left['O']}", True, (255, 0, 0))
        screen.blit(text_x, (10, 10))
        screen.blit(text_o, (10, 40))

        
        if big_board.winner:
            font = pygame.font.SysFont(None, 60)
            text = font.render(f"{big_board.winner} wins!", True, (255, 0, 0))
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(text, text_rect)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
