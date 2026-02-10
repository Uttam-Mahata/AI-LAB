# Assignment 2: Water Jug Problem

## Overview
This assignment implements the classic Water Jug Problem using various search algorithms. The problem involves measuring a specific amount of water using two jugs of different capacities with only basic operations: fill, empty, and pour.

## Problem Description
Given two jugs with capacities of 3 liters and 4 liters, and no markings for measurement, find a sequence of operations to measure exactly 2 liters in the 4-liter jug.

## Permissible Operations
1. Fill a jug to its full capacity
2. Empty a jug completely
3. Pour water from one jug to another until either the source is empty or the destination is full

## Algorithms Implemented
1. **Depth First Search (DFS)**: Explores paths deeply before backtracking
2. **Breadth First Search (BFS)**: Explores all paths at the current depth before moving deeper

## Features
- Solves the water jug problem with configurable jug capacities
- Supports variable initial and goal states
- Counts total number of paths to reach the goal state
- Compares DFS and BFS solutions
- Shows step-by-step solution path

## File
- `water_jug_problem.py` - Python implementation of the Water Jug Problem solver

## How to Run
```bash
python3 water_jug_problem.py
```

## Example Output
```
Problem 1: 3L and 4L jugs, Goal: (0, 2)
Solution using BFS:
Steps to reach goal:
Step 0: Initial State - Jug1: 0, Jug2: 0
Step 1: Fill Jug1 - Jug1: 3, Jug2: 0
Step 2: Pour Jug1->Jug2 - Jug1: 0, Jug2: 3
...
Total steps: 7
```

## Performance Comparison
- **DFS**: Finds a solution but may not be optimal (9 steps in example)
- **BFS**: Finds the shortest solution (7 steps in example)
- **Path Count**: Identifies all possible paths to goal (14 paths found)

## Requirements
- Python 3.6 or higher
- No external dependencies (uses only Python standard library)

## Implementation Details
- **Class**: `WaterJugProblem`
- **Methods**:
  - `get_successors()`: Generates all valid next states
  - `dfs()`: Depth-first search implementation
  - `bfs()`: Breadth-first search implementation
  - `count_all_paths_dfs()`: Counts all paths to goal
  - `print_solution()`: Formats and displays solution

## Extensions
The implementation supports:
- Variable initial and goal states
- Different jug capacities
- Multiple test cases
- Performance metrics (path length, total paths)

## Learning Outcomes
- Understanding uninformed search algorithms (DFS, BFS)
- State space representation and exploration
- Path finding and optimization
- Algorithm complexity comparison
- Python programming with data structures (stacks, queues, sets)

---
*Part of AI Lab coursework*
