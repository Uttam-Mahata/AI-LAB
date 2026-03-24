# Assignment 5 — Connect-4 with Mini-Max Algorithm

## Problem Statement

Connect-4 is a two-player strategy game played on a **6-row × 7-column** grid.
Players alternate dropping coloured discs into columns; discs fall to the lowest
available row. The first player to form a line of **four consecutive discs**
(horizontally, vertically, or diagonally) wins.

This implementation pits a **human player** against a **computer AI** powered by
the **Mini-Max algorithm with alpha-beta pruning**.

---

## Winning Strategies Implemented

| # | Strategy | Implementation |
|---|----------|----------------|
| a | **Middle Column Placement** | Heuristic awards +3 for each AI disc in column 3, giving the AI an inherent preference for the centre on its first move |
| b | **Trapping Opponents** | `score_window()` applies a −4 penalty whenever the opponent has 3 discs in a window with 1 empty cell, forcing the AI to block threats |
| c | **"7" Formation** | The depth-5 Mini-Max tree naturally discovers multi-directional threats that resemble the "7" pattern as part of optimal play |

---

## Algorithm: Mini-Max with Alpha-Beta Pruning

```
minimax(board, depth, α, β, maximising):
    if terminal(board) or depth == 0:
        return heuristic_score(board)

    if maximising (AI):
        for each valid column:
            simulate drop → recurse with maximising=False
            update α = max(α, score)
            if α ≥ β: break (β cut-off)

    else (human):
        for each valid column:
            simulate drop → recurse with maximising=True
            update β = min(β, score)
            if α ≥ β: break (α cut-off)
```

### Heuristic Function

Each board position is scored by examining every **window of 4 consecutive cells**
(horizontal, vertical, both diagonals):

| Window contents | Score |
|-----------------|-------|
| 4 AI discs | +100 |
| 3 AI discs + 1 empty | +5 |
| 2 AI discs + 2 empty | +2 |
| 3 opponent discs + 1 empty | −4 |
| Centre column AI disc | +3 per disc |

---

## Board Symbols

| Symbol | Meaning |
|--------|---------|
| `.` | Empty cell |
| `O` | Human disc |
| `X` | Computer (AI) disc |

---

## Usage

```bash
cd Assignment-5
python connect4.py
```

Enter a column number (0–6) when prompted. The AI responds immediately.
A game log is saved to `output.txt` after the session ends.

### Requirements

- Python 3.8+
- `numpy` (`pip install numpy`)

---

## File Structure

```
Assignment-5/
├── connect4.py   ← Full game + Mini-Max AI implementation
├── README.md     ← This file
└── output.txt    ← Auto-generated game session log
```
