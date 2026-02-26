# Assignment 3: Pathfinding and Search Algorithms

This directory contains implementations of various search algorithms, primarily focusing on **A* (A-Star) Search** for grid pathfinding and **AO* Search** for graph-based problem solving.

## Contents

- `grid_solver_v1.py`: The primary implementation of the A* algorithm on a 2D grid.
- `search_graph.py`: Implementation of the AO* search algorithm for AND-OR graphs.
- `grid_solver.py`: A version of the A* solver with additional corner-cutting prevention logic.
- `search_grid.py`: An alternative A* implementation focusing on standard Euclidean distance and visualization.
- `grid2.py`: A specialized A* solver that allows toggling strict corner rules for diagonal movement.

---

## A* Grid Solver (`grid_solver_v1.py`)

The `grid_solver_v1.py` script implements the A* search algorithm to find the shortest path between a start and goal coordinate on a grid that contains obstacles.

### Features
- **Heuristic**: Uses Euclidean distance ($ \sqrt{dx^2 + dy^2} $) to estimate the cost to the goal.
- **Movement**: Supports 8-directional movement (Cardinal + Diagonal).
  - Cardinal move cost: `1.0`
  - Diagonal move cost: `√2 ≈ 1.414`
- **Visualization**: Prints a text-based representation of the grid showing the start (S), goal (E), obstacles (#), and the calculated path (*).
- **Persistence**: Automatically writes the path details and visualization to `output.txt`.

### How to Run

Ensure you have Python 3 installed. Run the script directly from the terminal:

```bash
python grid_solver_v1.py
```

### Grid Layout
The default grid is a 4x8 matrix where `0` represents free space and `1` represents obstacles:
```text
S * . . # # # #
. . * * . # # #
# # . # * * . .
# . . . . . * E
```

---

## AO* Search (`search_graph.py`)

The `search_graph.py` script implements the **AO* Algorithm**, which is used for searching AND-OR graphs. Unlike A*, AO* is designed to solve problems that can be decomposed into sub-problems.

### How to Run
```bash
python search_graph.py
```

### Features
- **Heuristic Updates**: Dynamically updates node heuristics based on child node costs.
- **Solution Graph**: Tracks the optimal path through the AND-OR structure.
- **Backtracking**: Propagates cost changes back up the graph to find the global minimum.

---

## Output
When running the grid solvers, the results (path coordinates, total movement cost, and grid visualization) are saved to `output.txt` for easy reference.
