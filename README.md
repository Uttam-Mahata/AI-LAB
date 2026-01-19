# AI Lab - Search Algorithms Implementation

This repository contains implementations of classic AI search problems using various search algorithms.

## Problems Implemented

### 1. Water Jug Problem

**Problem Description:**
Given two jugs with capacities of 3 liters and 4 liters, and no markings for measurement, find a sequence of operations to measure exactly 2 liters in the 4-liter jug.

**Permissible Operations:**
- Fill a jug to its full capacity
- Empty a jug completely
- Pour water from one jug to another until either the source is empty or the destination is full

**Algorithms Used:**
- **Depth First Search (DFS):** Explores paths deeply before backtracking
- **Breadth First Search (BFS):** Explores all paths at the current depth before moving deeper

**Features:**
- Solves the water jug problem with configurable jug capacities
- Supports variable initial and goal states
- Counts total number of paths to reach the goal state
- Compares DFS and BFS solutions

**Usage:**
```bash
python3 water_jug_problem.py
```

**Example Output:**
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

---

### 2. 8-Puzzle Problem

**Problem Description:**
A 3×3 grid contains eight numbered tiles (1-8) and one empty space. The goal is to rearrange the tiles from an initial configuration to a goal configuration by sliding tiles into the empty space.

**Initial State:**
```
2 8 1
- 4 3
7 6 5
```

**Goal State:**
```
1 2 3
8 - 4
7 6 5
```

**Algorithm Used:**
- **A* Search:** Best-first search using f(n) = g(n) + h(n)
  - g(n): Cost from start to current node
  - h(n): Heuristic estimate from current to goal

**Heuristic Functions:**

1. **Misplaced Tiles Heuristic (h1):**
   - Counts the number of tiles not in their goal position
   - Admissible: Never overestimates the cost
   - Example: If 5 tiles are misplaced, h1 = 5

2. **Manhattan Distance Heuristic (h2):**
   - Sum of horizontal and vertical distances of each tile from its goal position
   - More informed than misplaced tiles
   - Example: Tile at (0,0) with goal at (1,2) contributes |0-1| + |0-2| = 3

**Features:**
- Implements A* search with two different heuristics
- Compares efficiency of both heuristics
- Shows complete solution path with intermediate states
- Displays nodes expanded for performance comparison

**Usage:**
```bash
python3 eight_puzzle_problem.py
```

**Example Output:**
```
Solution using A* with Manhattan distance Heuristic
Number of moves: 9
Nodes expanded: 15

Solution Steps:
Step 0: Initial
2 8 1
- 4 3
7 6 5

Step 1: Up
- 8 1
2 4 3
7 6 5
...
```

---

## Performance Comparison

### Water Jug Problem
- **DFS:** Finds a solution but may not be optimal (9 steps in example)
- **BFS:** Finds the shortest solution (7 steps in example)
- **Path Count:** Identifies all possible paths to goal (14 paths found)

### 8-Puzzle Problem
- **Misplaced Tiles:** Simple to compute, expands 29 nodes
- **Manhattan Distance:** More informed, expands only 15 nodes (48% fewer!)
- Both find optimal solution (9 moves)

---

## Key Concepts Demonstrated

### Search Strategies
1. **Uninformed Search:**
   - DFS: Stack-based, memory efficient but may not find optimal solution
   - BFS: Queue-based, guarantees shortest path, higher memory usage

2. **Informed Search:**
   - A*: Uses heuristics to guide search toward goal
   - Optimality depends on admissible heuristic (never overestimates)

### Heuristic Design
- **Admissibility:** h(n) ≤ actual cost to goal (guarantees optimal solution)
- **Informativeness:** Better heuristics expand fewer nodes
- **Computational Cost:** Trade-off between heuristic calculation time and node expansion

### State Space Representation
- **Water Jug:** State = (jug1_amount, jug2_amount)
- **8-Puzzle:** State = 3×3 grid configuration
- Both use hash sets to track visited states and avoid cycles

---

## Requirements

- Python 3.6 or higher
- No external dependencies (uses only Python standard library)

---

## Implementation Details

### Water Jug Problem (`water_jug_problem.py`)
- **Class:** `WaterJugProblem`
- **Methods:**
  - `get_successors()`: Generates all valid next states
  - `dfs()`: Depth-first search implementation
  - `bfs()`: Breadth-first search implementation
  - `count_all_paths_dfs()`: Counts all paths to goal
  - `print_solution()`: Formats and displays solution

### 8-Puzzle Problem (`eight_puzzle_problem.py`)
- **Classes:**
  - `PuzzleState`: Represents a puzzle configuration
  - `EightPuzzleSolver`: Implements A* search
- **Methods:**
  - `get_successors()`: Generates valid moves
  - `heuristic_misplaced_tiles()`: Counts misplaced tiles
  - `heuristic_manhattan_distance()`: Calculates Manhattan distance
  - `a_star_search()`: A* algorithm implementation
  - `print_solution()`: Displays solution path

---

## Learning Outcomes

1. **Understanding Search Algorithms:** Practical implementation of DFS, BFS, and A*
2. **Heuristic Design:** Comparing different heuristic functions
3. **State Space Search:** Representing and exploring problem states
4. **Algorithm Analysis:** Comparing time and space complexity through node expansion counts
5. **Python Programming:** Object-oriented design, data structures (heaps, queues, sets)

---

## Extensions and Modifications

Both implementations support:
- **Variable initial and goal states**
- **Different jug capacities (water jug)**
- **Multiple test cases**
- **Performance metrics (nodes expanded, path length)**

You can modify the problems by changing the parameters in the `main()` function of each file.

---

## License

This is an educational project for AI Lab coursework.

---

## Author

Implemented as part of AI Lab assignment demonstrating classical AI search algorithms.
