# 8-Puzzle Problem Mathematical Documentation

This directory contains mathematical documentation for the 8-Puzzle Problem implementation using Hill Climbing algorithm.

## Files

- **`eight_puzzle_documentation.tex`** - LaTeX source file (329 lines)
- **`eight_puzzle_documentation.pdf`** - Compiled PDF document (7 pages, 188 KB)

## Document Contents

### 1. Introduction
- Formal definition of the 8-puzzle problem
- Mathematical notation for states, moves, and state space
- Problem formulation as a directed graph

### 2. Heuristic Functions
- **Manhattan Distance Heuristic**: $h_M(S) = \sum_{i=1}^{8} |x_i - x_i^*| + |y_i - y_i^*|$
- **Misplaced Tiles Heuristic**: $h_T(S) = |\{i : s_i \neq s_i^* \land s_i \neq 0\}|$
- Dominance relation proof: $h_M(S) \geq h_T(S)$

### 3. Hill Climbing Algorithm
- Algorithm pseudocode in formal algorithmic notation
- Basic Hill Climbing implementation
- Hill Climbing with Sideways Moves variant
- Time complexity: $O(b^d)$ worst case, $O(d)$ typical
- Space complexity: $O(d)$
- Discussion of limitations (local optima, plateaus, ridges)

### 4. Experimental Results
- Test cases with matrix notation
- Performance analysis
- Algorithm characteristics

### 5. Mathematical Properties
- State space size: 9! = 362,880 total configurations
- Parity constraints: only 181,440 reachable states
- Average branching factor: ~2.67

### 6. References
- Classic AI textbooks

## Compiling the LaTeX Document

To compile the LaTeX source file:

```bash
pdflatex eight_puzzle_documentation.tex
pdflatex eight_puzzle_documentation.tex  # Run twice for proper references
```

### Required LaTeX Packages
- `amsmath`, `amssymb`, `amsthm` - Mathematical typesetting
- `algorithm`, `algpseudocode` - Algorithm formatting
- `hyperref` - Hyperlinks in table of contents
- `geometry` - Page layout

## Features

✓ Professional mathematical notation  
✓ Formal definitions, theorems, and proofs  
✓ Algorithm pseudocode with proper formatting  
✓ Matrix notation for state representation  
✓ Complexity analysis with Big-O notation  
✓ Clickable table of contents  
✓ Numbered theorems and definitions  

## Document Structure

The document is organized into 6 main sections with subsections, spanning 7 pages. It includes:
- Formal definitions for states, moves, and heuristics
- Theorems with proofs for heuristic properties
- 2 Hill Climbing algorithm pseudocodes
- Mathematical equations and matrices
- Test case results
- References to authoritative sources

## Usage

This documentation serves as:
1. A formal mathematical reference for Hill Climbing implementation
2. Educational material for understanding the algorithm
3. A basis for academic reports or presentations
4. Reference material for algorithm analysis
