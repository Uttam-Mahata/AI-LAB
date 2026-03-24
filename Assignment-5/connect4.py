"""
Connect-4 Game with Mini-Max Algorithm (Alpha-Beta Pruning)
============================================================
A two-player game where a human plays against a computer AI.
The AI uses the Mini-Max algorithm with alpha-beta pruning to
determine the optimal move at each step.

Board: 6 rows x 7 columns
Win condition: 4 discs in a row (horizontal, vertical, diagonal)
"""

import numpy as np
import random
import sys
import math

ROWS   = 6
COLS   = 7
EMPTY  = 0
PLAYER = 1   # Human  →  O
AI     = 2   # Computer → X
DEPTH  = 5   # Mini-Max search depth


class Connect4:
    """
    Encapsulates the Connect-4 game board, game logic, and AI.

    The board is a 2-D numpy array (ROWS x COLS).
    Row 0 is the TOP; row ROWS-1 is the BOTTOM.
    Gravity is simulated by always placing a disc in the lowest
    empty row of the chosen column.
    """

    def __init__(self):
        self.board  = np.zeros((ROWS, COLS), dtype=int)
        self.log    = []   

    def tee(self, *args, **kwargs):
        """Print to console AND accumulate for output.txt."""
        line = " ".join(str(a) for a in args)
        print(line, **kwargs)
        self.log.append(line)

    def is_valid_column(self, col: int) -> bool:
        """Return True if column still has at least one empty cell."""
        return self.board[0][col] == EMPTY

    def get_next_open_row(self, col: int) -> int:
        """Return the lowest empty row index in the given column."""
        for r in range(ROWS - 1, -1, -1):
            if self.board[r][col] == EMPTY:
                return r
        raise ValueError(f"Column {col} is full.")

    def drop_piece(self, board: np.ndarray, row: int, col: int, piece: int):
        """Place a disc on the given board array (in-place)."""
        board[row][col] = piece

    def is_board_full(self) -> bool:
        return all(not self.is_valid_column(c) for c in range(COLS))

    def winning_move(self, board: np.ndarray, piece: int) -> bool:
        """
        Return True if `piece` has four in a row anywhere on `board`.
        Checks horizontal, vertical, and both diagonals.
        """
        # Horizontal
        for r in range(ROWS):
            for c in range(COLS - 3):
                if all(board[r][c + i] == piece for i in range(4)):
                    return True
        # Vertical
        for r in range(ROWS - 3):
            for c in range(COLS):
                if all(board[r + i][c] == piece for i in range(4)):
                    return True
        # Diagonal (positive slope)
        for r in range(ROWS - 3):
            for c in range(COLS - 3):
                if all(board[r + i][c + i] == piece for i in range(4)):
                    return True
        # Diagonal (negative slope)
        for r in range(3, ROWS):
            for c in range(COLS - 3):
                if all(board[r - i][c + i] == piece for i in range(4)):
                    return True
        return False

    def score_window(self, window: list, piece: int) -> int:
        """
        Score a window of 4 cells for the given piece.

        Scoring reflects assignment strategies:
          +100  four in a row  (win)
          +5    three + one empty
          +2    two  + two empty
          -4    opponent three + one empty (block urgency)
        """
        opp = PLAYER if piece == AI else AI

        count     = window.count(piece)
        empty     = window.count(EMPTY)
        opp_count = window.count(opp)

        if count == 4:
            return 100
        elif count == 3 and empty == 1:
            return 5
        elif count == 2 and empty == 2:
            return 2
        elif opp_count == 3 and empty == 1:
            return -4
        return 0

    def score_position(self, board: np.ndarray, piece: int) -> int:
        """
        Evaluate the full board for the given piece.

        Strategy a — centre column preference (+3 per own disc in col 3)
        Strategy b — implicit via -4 penalty for opponent three-in-a-row
        """
        score = 0

        center_col = list(board[:, COLS // 2])
        score += center_col.count(piece) * 3

        # Horizontal windows
        for r in range(ROWS):
            row_arr = list(board[r, :])
            for c in range(COLS - 3):
                score += self.score_window(row_arr[c:c + 4], piece)

        # Vertical windows
        for c in range(COLS):
            col_arr = list(board[:, c])
            for r in range(ROWS - 3):
                score += self.score_window(col_arr[r:r + 4], piece)

        # Diagonal
        for r in range(ROWS - 3):
            for c in range(COLS - 3):
                window = [board[r + i][c + i] for i in range(4)]
                score += self.score_window(window, piece)

        # Diagonal
        for r in range(3, ROWS):
            for c in range(COLS - 3):
                window = [board[r - i][c + i] for i in range(4)]
                score += self.score_window(window, piece)

        return score

    def minimax(
        self,
        board: np.ndarray,
        depth: int,
        alpha: float,
        beta: float,
        maximizing_player: bool
    ):
        """
        Mini-Max algorithm with alpha-beta pruning.

        Parameters
        ----------
        board              : current board state (numpy array)
        depth              : remaining search depth
        alpha              : best score for maximiser (−∞ initially)
        beta               : best score for minimiser (+∞ initially)
        maximizing_player  : True = AI's turn, False = human's turn

        Returns
        -------
        (best_col, score)  : column index and its heuristic value
        """
        valid_cols = [c for c in range(COLS) if board[0][c] == EMPTY]

        ai_wins     = self.winning_move(board, AI)
        player_wins = self.winning_move(board, PLAYER)
        is_full     = len(valid_cols) == 0

        # Terminal states
        if ai_wins:
            return None, 100_000_000
        if player_wins:
            return None, -100_000_000
        if is_full or depth == 0:
            return None, self.score_position(board, AI)

        if maximizing_player:
            value    = -math.inf
            best_col = random.choice(valid_cols)

            for col in valid_cols:
                row    = self._get_open_row(board, col)
                b_copy = board.copy()
                b_copy[row][col] = AI

                _, new_score = self.minimax(b_copy, depth - 1, alpha, beta, False)

                if new_score > value:
                    value    = new_score
                    best_col = col

                alpha = max(alpha, value)
                if alpha >= beta:          # Beta cut-off
                    break

            return best_col, value

        else:  # Minimising player (human)
            value    = math.inf
            best_col = random.choice(valid_cols)

            for col in valid_cols:
                row    = self._get_open_row(board, col)
                b_copy = board.copy()
                b_copy[row][col] = PLAYER

                _, new_score = self.minimax(b_copy, depth - 1, alpha, beta, True)

                if new_score < value:
                    value    = new_score
                    best_col = col

                beta = min(beta, value)
                if alpha >= beta:          # Alpha cut-off
                    break

            return best_col, value

    def _get_open_row(self, board: np.ndarray, col: int) -> int:
        """Helper: find lowest empty row in `board` for a given column."""
        for r in range(ROWS - 1, -1, -1):
            if board[r][col] == EMPTY:
                return r
        raise ValueError(f"Column {col} is full.")

    def get_best_move(self) -> int:
        """Ask Mini-Max for the best column for the AI."""
        col, _ = self.minimax(self.board.copy(), DEPTH, -math.inf, math.inf, True)
        return col

    def print_board(self):
        """Render the board to console (and log) with ASCII art."""
        symbols = {EMPTY: ".", PLAYER: "O", AI: "X"}

        header = " " + "   ".join(str(c) for c in range(COLS))
        divider = "+" + "---+" * COLS

        self.tee("\n" + divider)
        for r in range(ROWS):
            row_str = "|"
            for c in range(COLS):
                row_str += f" {symbols[self.board[r][c]]} |"
            self.tee(row_str)
            self.tee(divider)
        self.tee(header)
        self.tee("")

    def play(self):
        """Run the interactive game loop (human vs AI)."""
        sep = "=" * 55
        banner = (
            "\n" + sep + "\n" +
            "      CONNECT-4  |  Mini-Max AI  (depth=" + str(DEPTH) + ")\n" +
            sep + "\n" +
            "  You   = O    |    Computer = X\n" +
            "  Enter a column number (0-6) to drop your disc.\n" +
            sep
        )
        self.tee(banner)
        self.print_board()

        game_over = False
        turn      = PLAYER   # Human goes first

        while not game_over:
            if turn == PLAYER:
                col = None
                while col is None:
                    try:
                        raw = input("Your turn — choose column (0-6): ").strip()
                        self.log.append(f"Your turn — choose column (0-6): {raw}")
                        c = int(raw)
                        if c < 0 or c >= COLS:
                            print("  [!] Column must be between 0 and 6.")
                        elif not self.is_valid_column(c):
                            print("  [!] That column is full. Pick another.")
                        else:
                            col = c
                    except ValueError:
                        print("  [!] Please enter a valid integer.")

                row = self.get_next_open_row(col)
                self.drop_piece(self.board, row, col, PLAYER)
                self.tee(f"\n  >> You placed O in column {col}.")

                if self.winning_move(self.board, PLAYER):
                    self.print_board()
                    self.tee("=" * 55)
                    self.tee("  CONGRATULATIONS! You win!")
                    self.tee("=" * 55)
                    game_over = True
                elif self.is_board_full():
                    self.print_board()
                    self.tee("=" * 55)
                    self.tee("  It's a DRAW!")
                    self.tee("=" * 55)
                    game_over = True
                else:
                    self.print_board()
                    turn = AI

            else:
                self.tee("\n  Computer is thinking...")
                col = self.get_best_move()
                row = self.get_next_open_row(col)
                self.drop_piece(self.board, row, col, AI)
                self.tee(f"  >> Computer placed X in column {col}.")

                if self.winning_move(self.board, AI):
                    self.print_board()
                    self.tee("=" * 55)
                    self.tee("  Computer wins! Better luck next time.")
                    self.tee("=" * 55)
                    game_over = True
                elif self.is_board_full():
                    self.print_board()
                    self.tee("=" * 55)
                    self.tee("  It's a DRAW!")
                    self.tee("=" * 55)
                    game_over = True
                else:
                    self.print_board()
                    turn = PLAYER

        # Write session log to output.txt
        output_path = "output.txt"
        with open(output_path, "w") as f:
            f.write("\n".join(self.log))
        print(f"\n  [Game log saved to {output_path}]")


if __name__ == "__main__":
    game = Connect4()
    game.play()
