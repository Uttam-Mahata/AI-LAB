# Assignment 2: AI Search Algorithms

This assignment explores classic artificial intelligence search problems using both uninformed and informed search techniques. It includes implementations of the **Water Jug Problem** and the **8-Puzzle Problem** in both Python and C.

## Table of Contents
- [Assignment Overview](#assignment-overview)
- [Problems & Algorithms](#problems--algorithms)
  - [1. Water Jug Problem](#1-water-jug-problem)
  - [2. 8-Puzzle Problem](#2-8-puzzle-problem)
- [Project Structure](#project-structure)
- [How to Run](#how-to-run)
  - [Python Version](#python-version)
  - [C Version](#c-version)
- [Heuristics Comparison (8-Puzzle)](#heuristics-comparison-8-puzzle)
- [Requirements](#requirements)

---

## Assignment Overview
The goal of this assignment is to understand and implement various search strategies to solve state-space problems. 
- **Uninformed Search**: BFS and DFS applied to the Water Jug problem.
- **Informed Search**: A* Search and Hill Climbing (with variants) applied to the 8-Puzzle problem.

## Problems & Algorithms

### 1. Water Jug Problem
**Problem**: Given two jugs with capacities $X$ and $Y$ liters, reach a target state $(a, b)$ using a sequence of valid operations.
- **Operations**: Fill a jug, Empty a jug, Pour from one jug to another.
- **Algorithms**:
  - **Breadth-First Search (BFS)**: Guaranteed to find the shortest path to the goal.
  - **Depth-First Search (DFS)**: Explores paths deeply; may not find the optimal solution.
  - **All Paths DFS**: Counts the total number of distinct paths to the goal within a depth limit.

### 2. 8-Puzzle Problem
**Problem**: A $3 \times 3$ board with 8 numbered tiles and one empty space. Reorder the tiles from an initial configuration to a goal state.
- **Algorithms**:
  - **A* Search**: Uses $f(n) = g(n) + h(n)$ to find the optimal path.
  - **Hill Climbing**: Greedy local search that moves to the neighbor with the best heuristic value.
  - **Hill Climbing with Sideways Moves**: Allows a limited number of moves to states with the same heuristic value to escape plateaus.
- **Heuristics**:
  - **Misplaced Tiles**: Number of tiles not in their goal position.
  - **Manhattan Distance**: Sum of vertical and horizontal distances of tiles from their goal positions.

---

## Project Structure
```
Assignment-2/
├── water_jug_problem.py    # Python: Water Jug implementation
├── eight_puzzle_problem.py   # Python: 8-Puzzle implementation (Hill Climbing)
├── run.py                  # Python: Main runner for both problems
├── water_jug_problem.c     # C: Water Jug implementation
├── eight_puzzle_problem.c    # C: 8-Puzzle implementation (A* Search)
├── run.c                   # C: Main runner for both problems
├── Makefile                # Build configuration for C
├── DOCUMENTATION.md        # Technical/Mathematical Documentation
└── ...                     # LaTeX files and outputs
```

---

## How to Run

### Python Version
The Python version provides a comprehensive demonstration of both problems.
```bash
python3 run.py
```
Or run individual problem solvers:
```bash
python3 water_jug_problem.py
python3 eight_puzzle_problem.py
```

### C Version
The C version is optimized for performance and implements A* for the 8-Puzzle.
```bash
# Compile the project
make

# Run the demonstration
./run_c

# Clean build files
make clean
```

---

## Heuristics Comparison (8-Puzzle)
The 8-Puzzle implementations compare the efficiency of different heuristics. Typically, **Manhattan Distance** is more informed than **Misplaced Tiles**, resulting in fewer nodes expanded to find the same optimal solution.

| Heuristic | Nodes Expanded | Solution Length |
|-----------|----------------|-----------------|
| Misplaced Tiles | Higher | Same (Optimal) |
| Manhattan Distance | Lower | Same (Optimal) |

---

## Requirements
- **Python**: Version 3.6+
- **C**: GCC compiler with `make` utility.
- **LaTeX**: (Optional) For compiling the mathematical documentation.

---
*Developed for AI Lab Coursework*
