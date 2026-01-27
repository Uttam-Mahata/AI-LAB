import heapq
from typing import List, Tuple, Optional, Set
from copy import deepcopy


class PuzzleState:
    """
    Represents a state in the 8-puzzle problem.
    
    Attributes:
        board: 3x3 grid representing the puzzle state
        empty_pos: Position of the empty cell (row, col)
        g_cost: Cost from start to current state
        h_cost: Heuristic cost from current state to goal
        f_cost: Total cost (g_cost + h_cost)
        parent: Parent state in the search tree
        move: Move that led to this state
    """
    
    BOARD_SIZE = 3  # Size of the puzzle grid (3x3)
    
    def __init__(self, board: List[List[int]], g_cost: int = 0, 
                 parent=None, move: str = "Initial"):
        """
        Initialize a puzzle state.
        
        Args:
            board: 3x3 grid representing the puzzle
            g_cost: Cost from start state
            parent: Parent state
            move: Move description
        """
        self.board = board
        self.g_cost = g_cost
        self.h_cost = 0
        self.f_cost = 0
        self.parent = parent
        self.move = move
        self.empty_pos = self._find_empty()
    
    def _find_empty(self) -> Tuple[int, int]:
        """Find the position of the empty cell (0)."""
        for i in range(self.BOARD_SIZE):
            for j in range(self.BOARD_SIZE):
                if self.board[i][j] == 0:
                    return (i, j)
        return (0, 0)
    
    def __lt__(self, other):
        """Compare states based on f_cost for priority queue."""
        return self.f_cost < other.f_cost
    
    def __eq__(self, other):
        """Check if two states are equal."""
        return self.board == other.board
    
    def __hash__(self):
        """Hash function for storing states in set."""
        return hash(str(self.board))
    
    def get_board_tuple(self) -> Tuple:
        """Get immutable representation of board for hashing."""
        return tuple(tuple(row) for row in self.board)
    
    def print_board(self):
        """Print the board in a readable format."""
        for row in self.board:
            print(" ".join(str(cell) if cell != 0 else "-" for cell in row))


class EightPuzzleSolver:
    """
    Solver for the 8-puzzle problem using A* search.
    
    Supports two heuristic functions:
    1. Misplaced tiles (h1)
    2. Manhattan distance (h2)
    """
    
    def __init__(self, initial_state: List[List[int]], goal_state: List[List[int]]):
        """
        Initialize the puzzle solver.
        
        Args:
            initial_state: Starting configuration
            goal_state: Target configuration
        """
        self.initial_state = PuzzleState(initial_state)
        self.goal_state = PuzzleState(goal_state)
        self.goal_positions = self._compute_goal_positions()
        self.nodes_expanded = 0
    
    def _compute_goal_positions(self) -> dict:
        """
        Precompute goal positions for each tile for Manhattan distance.
        
        Returns:
            Dictionary mapping tile value to (row, col) position in goal state
        """
        positions = {}
        for i in range(PuzzleState.BOARD_SIZE):
            for j in range(PuzzleState.BOARD_SIZE):
                tile = self.goal_state.board[i][j]
                if tile != 0:
                    positions[tile] = (i, j)
        return positions
    
    def get_successors(self, state: PuzzleState) -> List[PuzzleState]:
        """
        Generate all valid successor states from current state.
        
        Valid moves: Up, Down, Left, Right (moving the empty cell)
        
        Args:
            state: Current puzzle state
            
        Returns:
            List of successor states
        """
        successors = []
        row, col = state.empty_pos
        moves = [
            (-1, 0, "Up"),      # Move empty cell up
            (1, 0, "Down"),     # Move empty cell down
            (0, -1, "Left"),    # Move empty cell left
            (0, 1, "Right")     # Move empty cell right
        ]
        
        for dr, dc, move_name in moves:
            new_row, new_col = row + dr, col + dc
            
            if 0 <= new_row < PuzzleState.BOARD_SIZE and 0 <= new_col < PuzzleState.BOARD_SIZE:                # Create new board
                new_board = deepcopy(state.board)


                new_board[row][col], new_board[new_row][new_col] = \
                    new_board[new_row][new_col], new_board[row][col]
                
                new_state = PuzzleState(
                    new_board, 
                    state.g_cost + 1, 
                    state, 
                    move_name
                )
                successors.append(new_state)
        
        return successors
    
    def heuristic_misplaced_tiles(self, state: PuzzleState) -> int:
        """
        Calculate the number of misplaced tiles.
        
        Args:
            state: Current puzzle state
            
        Returns:
            Number of tiles not in their goal position
        """
        count = 0
        for i in range(PuzzleState.BOARD_SIZE):
            for j in range(PuzzleState.BOARD_SIZE):
                if state.board[i][j] != 0 and \
                   state.board[i][j] != self.goal_state.board[i][j]:
                    count += 1
        return count
    
    def heuristic_manhattan_distance(self, state: PuzzleState) -> int:
        """
        Calculate the Manhattan distance heuristic.
        
        Manhattan distance is the sum of horizontal and vertical distances
        of each tile from its goal position.
        
        Args:
            state: Current puzzle state
            
        Returns:
            Sum of Manhattan distances for all tiles
        """
        distance = 0
        for i in range(PuzzleState.BOARD_SIZE):
            for j in range(PuzzleState.BOARD_SIZE):
                tile = state.board[i][j]
                if tile != 0:
                    goal_row, goal_col = self.goal_positions[tile]
                    distance += abs(i - goal_row) + abs(j - goal_col)
        return distance
    
    def a_star_search(self, heuristic_type: str = "manhattan") -> Optional[PuzzleState]:
        """
        Solve the puzzle using A* search algorithm.
        
        Args:
            heuristic_type: Type of heuristic ("misplaced" or "manhattan")
            
        Returns:
            Goal state with path information, or None if no solution
        """
        if heuristic_type == "misplaced":
            heuristic_func = self.heuristic_misplaced_tiles
        else:
            heuristic_func = self.heuristic_manhattan_distance
        
        start = self.initial_state
        start.h_cost = heuristic_func(start)
        start.f_cost = start.g_cost + start.h_cost
        
        open_set = []
        heapq.heappush(open_set, start)
        
        closed_set = set()
        
        open_set_states = {start.get_board_tuple(): start}
        
        self.nodes_expanded = 0
        
        while open_set:
            current = heapq.heappop(open_set)
            current_tuple = current.get_board_tuple()
            
            if current_tuple in open_set_states:
                del open_set_states[current_tuple]
            
            if current.board == self.goal_state.board:
                return current
            
            closed_set.add(current_tuple)
            self.nodes_expanded += 1
            
            for successor in self.get_successors(current):
                successor_tuple = successor.get_board_tuple()
                
                # Skip if already visited
                if successor_tuple in closed_set:
                    continue
                
                successor.h_cost = heuristic_func(successor)
                successor.f_cost = successor.g_cost + successor.h_cost
                
                if successor_tuple in open_set_states:
                    existing = open_set_states[successor_tuple]
                    if successor.g_cost < existing.g_cost:


                        existing.g_cost = successor.g_cost
                        existing.f_cost = successor.f_cost
                        existing.parent = successor.parent
                        existing.move = successor.move
                else:
                    heapq.heappush(open_set, successor)
                    open_set_states[successor_tuple] = successor
        
        return None
    
    def get_solution_path(self, goal_state: PuzzleState) -> List[PuzzleState]:
        """
        Reconstruct the solution path from initial to goal state.
        
        Args:
            goal_state: The goal state reached by search
            
        Returns:
            List of states from initial to goal
        """
        path = []
        current = goal_state
        while current is not None:
            path.append(current)
            current = current.parent
        return list(reversed(path))
    
    def print_solution(self, solution_path: List[PuzzleState], heuristic_type: str):
        """
        Print the solution path in a readable format.
        
        Args:
            solution_path: List of states from initial to goal
            heuristic_type: Type of heuristic used
        """
        print(f"\n{'='*60}")
        print(f"Solution using A* with {heuristic_type.capitalize()} Heuristic")
        print(f"{'='*60}")
        print(f"Initial State:")
        solution_path[0].print_board()
        print(f"\nGoal State:")
        self.goal_state.print_board()
        print(f"\nNumber of moves: {len(solution_path) - 1}")
        print(f"Nodes expanded: {self.nodes_expanded}")
        print(f"\nSolution Steps:")
        print("-" * 60)
        
        for i, state in enumerate(solution_path):
            print(f"\nStep {i}: {state.move}")
            print(f"g={state.g_cost}, h={state.h_cost}, f={state.f_cost}")
            state.print_board()
        
        print("\n" + "="*60)


def main():
    """Main function to demonstrate the 8-puzzle solver."""
    
    initial_state = [
        [1, 2, 3],
        [8, 0, 4],
        [7, 6, 5]
    ]
    
    goal_state = [
        [2, 8, 1],
        [0, 4, 3],
        [7, 6, 5]
    ]
    
    print("\n" + "="*60)
    print("8-PUZZLE PROBLEM SOLVER")
    print("="*60)
    
    print("\n[1] Solving with A* using Misplaced Tiles Heuristic...")
    print("-" * 60)
    
    solver1 = EightPuzzleSolver(initial_state, goal_state)
    solution1 = solver1.a_star_search(heuristic_type="misplaced")
    
    if solution1:
        path1 = solver1.get_solution_path(solution1)
        solver1.print_solution(path1, "misplaced tiles")
    else:
        print("No solution found using Misplaced Tiles heuristic")
    
    print("\n[2] Solving with A* using Manhattan Distance Heuristic...")
    print("-" * 60)
    
    solver2 = EightPuzzleSolver(initial_state, goal_state)
    solution2 = solver2.a_star_search(heuristic_type="manhattan")
    
    if solution2:
        path2 = solver2.get_solution_path(solution2)
        solver2.print_solution(path2, "manhattan distance")
    else:
        print("No solution found using Manhattan Distance heuristic")
    
    print("\n" + "="*60)
    print("COMPARISON OF HEURISTICS")
    print("="*60)
    if solution1 and solution2:
        print(f"Misplaced Tiles:")
        print(f"  - Moves: {len(path1) - 1}")
        print(f"  - Nodes Expanded: {solver1.nodes_expanded}")
        print(f"\nManhattan Distance:")
        print(f"  - Moves: {len(path2) - 1}")
        print(f"  - Nodes Expanded: {solver2.nodes_expanded}")
        
        if solver2.nodes_expanded < solver1.nodes_expanded:
            print(f"\nManhattan Distance is more efficient!")
            print(f"It expanded {solver1.nodes_expanded - solver2.nodes_expanded} fewer nodes.")
        elif solver1.nodes_expanded < solver2.nodes_expanded:
            print(f"\nMisplaced Tiles is more efficient!")
            print(f"It expanded {solver2.nodes_expanded - solver1.nodes_expanded} fewer nodes.")
        else:
            print(f"\nBoth heuristics expanded the same number of nodes.")
    
    print("\n\n" + "="*60)
    print("Additional Test Case: Different Initial State")
    print("="*60)
    
    initial_state2 = [
        [1, 2, 3],
        [8, 4, 0],
        [7, 6, 5]
    ]
    
    solver3 = EightPuzzleSolver(initial_state2, goal_state)
    solution3 = solver3.a_star_search(heuristic_type="manhattan")
    
    if solution3:
        path3 = solver3.get_solution_path(solution3)
        solver3.print_solution(path3, "manhattan distance")
    else:
        print("No solution found")


if __name__ == "__main__":
    main()
