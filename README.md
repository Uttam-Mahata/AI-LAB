# AI Lab - Course Assignments

This repository contains AI Lab course assignments, including implementations of classic AI problems and machine learning applications.

## Repository Structure

- **Assignment 1**: News Classification using LSTM and GRU
- **Assignment 2**: Water Jug Problem using Search Algorithms
- **Additional Problems**: Eight Puzzle Problem (bonus implementation)

## Assignments

### Assignment 1: News Classification

Implementation of text classification using deep learning techniques (LSTM and GRU) on the AG News dataset.

**Location**: `Assignment 1/`

**Key Features**:
- LSTM and GRU text classifiers
- Multiple embedding strategies (GloVe frozen, GloVe fine-tuned, Random)
- Hyperparameter tuning
- Model evaluation and comparison

**File**: `ag_news_classification.ipynb`

[View Assignment 1 README](Assignment%201/README.md)

---

### Assignment 2: Water Jug Problem

Classic AI problem solving using search algorithms (DFS and BFS) to measure a specific amount of water.

**Location**: `Assignment 2/`

**Key Features**:
- Depth First Search (DFS) implementation
- Breadth First Search (BFS) implementation
- Path counting and optimization
- Configurable jug capacities and goal states

**File**: `water_jug_problem.py`

**Usage**:
```bash
cd "Assignment 2"
python3 water_jug_problem.py
```

[View Assignment 2 README](Assignment%202/README.md)

---

## Additional Implementation: 8-Puzzle Problem

**Note**: This is an additional problem implementation (not part of the main assignments).

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

## Quick Start

### Run Individual Assignments

**Assignment 1 (News Classification)**:
```bash
# Open the notebook in Jupyter or Google Colab
cd "Assignment 1"
jupyter notebook ag_news_classification.ipynb
```

**Assignment 2 (Water Jug Problem)**:
```bash
cd "Assignment 2"
python3 water_jug_problem.py
```

### Run All Demonstrations

Run the demonstration script to see both Water Jug and 8-Puzzle problems in action:

```bash
python3 demo.py
```

Or run the 8-Puzzle problem individually:

```bash
python3 eight_puzzle_problem.py
```

## Requirements

### Assignment 1
- Python 3.6+
- Jupyter Notebook
- TensorFlow/PyTorch
- NumPy, Pandas, Matplotlib
- GloVe embeddings (downloaded within notebook)

### Assignment 2 & 8-Puzzle
- Python 3.6 or higher
- No external dependencies (uses only Python standard library)

---

## Key Concepts Demonstrated

### Search Strategies
1. **Uninformed Search (Assignment 2):**
   - DFS: Stack-based, memory efficient but may not find optimal solution
   - BFS: Queue-based, guarantees shortest path, higher memory usage

2. **Informed Search (8-Puzzle):**
   - A*: Uses heuristics to guide search toward goal
   - Optimality depends on admissible heuristic (never overestimates)

3. **Deep Learning (Assignment 1):**
   - LSTM: Long Short-Term Memory for sequence modeling
   - GRU: Gated Recurrent Unit for text classification
   - Word embeddings for text representation

### Performance Comparison

**Water Jug Problem (Assignment 2)**:
- **DFS:** Finds a solution but may not be optimal (9 steps)
- **BFS:** Finds the shortest solution (7 steps)
- **Path Count:** Identifies all possible paths to goal (14 paths)

**8-Puzzle Problem (Additional)**:
- **Misplaced Tiles:** Simple to compute, expands 29 nodes
- **Manhattan Distance:** More informed, expands only 15 nodes (48% fewer!)
- Both find optimal solution (9 moves)

---

## Learning Outcomes

### Assignment 1: News Classification
1. Text preprocessing and tokenization
2. Word embeddings (GloVe) and their applications
3. LSTM and GRU architectures for sequence modeling
4. Hyperparameter tuning strategies
5. Model evaluation and comparison

### Assignment 2: Water Jug Problem
1. Understanding uninformed search algorithms (DFS, BFS)
2. State space representation and exploration
3. Path finding and optimization
4. Algorithm complexity comparison
5. Python programming with data structures (stacks, queues, sets)

### 8-Puzzle Problem (Additional)
1. Understanding informed search with A* algorithm
2. Heuristic design (admissibility and informativeness)
3. Comparing different heuristics
4. Priority queue implementation with heapq
5. State space search optimization

---

## Course Information

This is an educational project for AI Lab coursework, demonstrating:
- Classical AI search algorithms
- Deep learning for natural language processing
- Problem-solving techniques in artificial intelligence

---

## Repository Files

- `Assignment 1/` - News Classification assignment
  - `ag_news_classification.ipynb` - Jupyter notebook
  - `README.md` - Assignment 1 documentation
- `Assignment 2/` - Water Jug Problem assignment
  - `water_jug_problem.py` - Python implementation
  - `README.md` - Assignment 2 documentation
- `eight_puzzle_problem.py` - Additional 8-Puzzle implementation
- `demo.py` - Demonstration script for Water Jug and 8-Puzzle problems
- `README.md` - This file (main documentation)
