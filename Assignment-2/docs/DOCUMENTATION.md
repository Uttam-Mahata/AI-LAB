# Assignment 2 Technical Documentation

This document provides technical and mathematical details for the algorithms implemented in Assignment 2.

## 1. Water Jug Problem

### 1.1 State Representation
A state is represented as a tuple $(j_1, j_2)$ where:
- $0 \leq j_1 \leq C_1$ (current water in Jug 1)
- $0 \leq j_2 \leq C_2$ (current water in Jug 2)
- $C_1, C_2$ are the maximum capacities.

### 1.2 Transition Rules
The state space is explored using the following operators:
1. **Fill**: $(j_1, j_2) \to (C_1, j_2)$ or $(j_1, C_2)$
2. **Empty**: $(j_1, j_2) \to (0, j_2)$ or $(j_1, 0)$
3. **Pour**:
   - $1 \to 2$: $(j_1, j_2) \to (j_1 - d, j_2 + d)$ where $d = \min(j_1, C_2 - j_2)$
   - $2 \to 1$: $(j_1, j_2) \to (j_1 + d, j_2 - d)$ where $d = \min(j_2, C_1 - j_1)$

### 1.3 Search Strategies
- **BFS (Breadth-First Search)**: Uses a FIFO queue to explore the shallowest unvisited nodes first. This guarantees finding the shortest sequence of operations.
- **DFS (Depth-First Search)**: Uses a LIFO stack. In the Water Jug problem, cycles are handled using a `visited` set to prevent infinite loops.

---

## 2. 8-Puzzle Problem

### 2.1 State Space
The 8-puzzle has $9! = 362,880$ possible configurations. However, only half ($181,440$) are reachable from any given state due to parity constraints on inversions.

### 2.2 Heuristic Functions
Two heuristics are implemented to estimate the cost to reach the goal:

#### A. Misplaced Tiles ($h_1$)
Counts the number of tiles that are not in their target position.
$$h_1(s) = \sum_{i=1}^{8} [pos(tile_i) \neq goal\_pos(tile_i)]$$

#### B. Manhattan Distance ($h_2$)
The sum of absolute differences of coordinates for each tile.
$$h_2(s) = \sum_{i=1}^{8} (|x_i - x_{goal,i}| + |y_i - y_{goal,i}|)$$
*Note: $h_2$ is more informed than $h_1$ because $h_2(n) \geq h_1(n)$ for all $n$.*

### 2.3 Algorithms

#### A* Search (Implemented in C)
Minimizes $f(n) = g(n) + h(n)$:
- $g(n)$: Actual cost from start to node $n$.
- $h(n)$: Estimated cost from $n$ to goal.
Since $h(n)$ is admissible (never overestimates), A* finds the optimal solution.

#### Hill Climbing (Implemented in Python)
A greedy local search that always moves to the successor with the lowest $h(n)$.
- **Simple Hill Climbing**: Terminates if no neighbor has a lower $h(n)$. Prone to local optima and plateaus.
- **Sideways Moves**: If the best neighbor has $h(neighbor) = h(current)$, the algorithm can take a limited number of "sideways" steps to navigate plateaus.

---

## 3. Implementation Details

### Data Structures
- **Python**: Uses `collections.deque` for BFS, lists as stacks for DFS, and `set` for visited states.
- **C**: Implements custom Priority Queues (Min-Heaps) for A* and Linked Lists for state management.

### Performance Comparison
Experimental results show that:
1. **BFS** is optimal for the Water Jug problem but memory-intensive.
2. **A* with Manhattan Distance** expands significantly fewer nodes than **A* with Misplaced Tiles** for the 8-puzzle.
3. **Hill Climbing** is extremely fast but frequently fails on complex 8-puzzle configurations without advanced techniques like random restarts or sideways moves.

---
*Refer to the LaTeX documentation `eight_puzzle_documentation.tex` for formal proofs and matrix notation.*
