# Ultimate Tic-Tac-Toe

A visually enhanced, feature-rich implementation of Ultimate Tic-Tac-Toe with an AI opponent, built using Python and Pygame.

## Features

- **Ultimate Tic-Tac-Toe**: Play the advanced version of Tic-Tac-Toe on a 3x3 grid of 3x3 boards.
- **AI Opponent**: Challenge a computer player powered by a minimax-based algorithm.
- **Modern UI**: Neon-style graphics, animated start screen, and interactive buttons.
- **Special Moves**: Each player can delete up to 3 of their opponent's marks per game (right-click).
- **Restart & Score Tracking**: Easily restart games and track remaining deletes for each player.

## How the AI Works

The AI opponent in this project is implemented using the **Minimax algorithm** with alpha-beta pruning, tailored for the complexity of Ultimate Tic-Tac-Toe.

### Key Features:

- **Minimax Search**: The AI simulates possible future moves up to a certain depth (configurable, default is 4), evaluating the best possible outcome for itself while assuming the opponent also plays optimally.
- **Alpha-Beta Pruning**: This optimization reduces the number of game states the AI needs to evaluate, making the search faster without sacrificing accuracy.
- **Dual Actions**: The AI considers both placing its own mark and deleting an opponent's mark (if deletes are available), choosing the action that maximizes its advantage.
- **Board Evaluation**: At each leaf node or when the search depth is reached, the AI evaluates the board:
  - +1000 if the AI has won the big board.
  - -1000 if the opponent has won.
  - +10 for each small board won by the AI, -10 for each won by the opponent.
- **Active Board Logic**: The AI respects the rules of Ultimate Tic-Tac-Toe, only considering moves in the active small board unless it is full or won.

### AI Class Structure

- `AIPlayer.get_move(board, deletes_left)`: Returns the best move (either a placement or a delete) by simulating all possible actions and evaluating their outcomes.
- `AIPlayer.minimax(board, deletes_left, depth, maximizing, alpha, beta)`: Recursively explores the game tree, alternating between maximizing (AI's turn) and minimizing (opponent's turn) the evaluation score.
- `AIPlayer.evaluate(board)`: Scores the board state for the AI.

This approach allows the AI to play strategically, balancing between winning small boards, blocking the opponent, and using deletes effectively.

## Requirements

- Python 3.7+
- [Pygame](https://www.pygame.org/) (`pip install pygame`)

## How to Run

1. **Install dependencies** (if not already installed):
   ```bash
   pip install pygame
   ```

2. **Run the game**:
   ```bash
   python main.py
   ```

3. **Gameplay**:
   - **Left-click** to place your mark.
   - **Right-click** to delete an opponent's mark (if you have deletes left).
   - Click **RESTART** to start a new game.

## Files

- `main.py` — Main game loop and UI.
- `board.py` — Game logic for boards and moves.
- `ai.py` — AI player logic.
- `config.py` — Screen and color settings.
- `X_O.png` — Game background image.
- `ULTIMAT TIC-TAC-TOE.pptx` — Project presentation.

## Credits

Developed by Dorin Tzuberi, Roee Rozenstein, Shahar Profeta, Shai Saraf. 

---

