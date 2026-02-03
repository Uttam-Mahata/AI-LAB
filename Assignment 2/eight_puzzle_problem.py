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
    
    def hill_climbing_search(self, heuristic_type: str = "manhattan", max_iterations: int = 10000) -> Optional[PuzzleState]:
        """
        Solve the puzzle using Hill Climbing algorithm.
        
        Hill Climbing is a local search algorithm that:
        1. Starts from initial state
        2. Evaluates all neighbors
        3. Moves to the best neighbor (with lowest heuristic cost)
        4. Repeats until no neighbor is better (local optimum) or goal is reached
        
        Args:
            heuristic_type: Type of heuristic ("misplaced" or "manhattan")
            max_iterations: Maximum number of iterations to prevent infinite loops
            
        Returns:
            Goal state with path information, or None if stuck at local optimum
        """
        if heuristic_type == "misplaced":
            heuristic_func = self.heuristic_misplaced_tiles
        else:
            heuristic_func = self.heuristic_manhattan_distance
        
        current = self.initial_state
        current.h_cost = heuristic_func(current)
        
        self.nodes_expanded = 0
        visited_states = set()
        
        for iteration in range(max_iterations):
            # Check if goal reached
            if current.board == self.goal_state.board:
                return current
            
            # Mark current state as visited
            visited_states.add(current.get_board_tuple())
            
            # Get all successors
            successors = self.get_successors(current)
            self.nodes_expanded += 1
            
            # Calculate heuristic for all successors
            best_successor = None
            best_heuristic = float('inf')
            
            for successor in successors:
                # Skip already visited states to avoid cycles
                if successor.get_board_tuple() in visited_states:
                    continue
                    
                successor.h_cost = heuristic_func(successor)
                
                if successor.h_cost < best_heuristic:
                    best_heuristic = successor.h_cost
                    best_successor = successor
            
            # If no better successor found, we're stuck at local optimum
            if best_successor is None or best_heuristic >= current.h_cost:
                return None  # Stuck at local optimum
            
            # Move to best successor
            current = best_successor
        
        return None  # Max iterations reached

    def hill_climbing_with_sideways_moves(self, heuristic_type: str = "manhattan", max_iterations: int = 10000, max_sideways: int = 100) -> Optional[PuzzleState]:
        """
        Hill Climbing with sideways moves to escape plateaus.
        
        Allows moving to neighbors with the same heuristic value for a limited number of times.
        
        Args:
            heuristic_type: Type of heuristic ("misplaced" or "manhattan")
            max_iterations: Maximum number of iterations
            max_sideways: Maximum number of consecutive sideways moves allowed
            
        Returns:
            Goal state with path information, or None if stuck at local optimum
        """
        if heuristic_type == "misplaced":
            heuristic_func = self.heuristic_misplaced_tiles
        else:
            heuristic_func = self.heuristic_manhattan_distance
        
        current = self.initial_state
        current.h_cost = heuristic_func(current)
        
        self.nodes_expanded = 0
        visited_states = set()
        sideways_count = 0
        
        for iteration in range(max_iterations):
            # Check if goal reached
            if current.board == self.goal_state.board:
                return current
            
            # Mark current state as visited
            visited_states.add(current.get_board_tuple())
            
            # Get all successors
            successors = self.get_successors(current)
            self.nodes_expanded += 1
            
            # Calculate heuristic for all successors
            best_successor = None
            best_heuristic = float('inf')
            
            for successor in successors:
                # Skip already visited states to avoid cycles
                if successor.get_board_tuple() in visited_states:
                    continue
                    
                successor.h_cost = heuristic_func(successor)
                
                if successor.h_cost < best_heuristic:
                    best_heuristic = successor.h_cost
                    best_successor = successor
            
            # Check if we can move
            if best_successor is None:
                return None  # No unvisited neighbors
            
            # If better successor found, move to it
            if best_heuristic < current.h_cost:
                current = best_successor
                sideways_count = 0  # Reset sideways counter
            # Allow sideways moves (same heuristic value)
            elif best_heuristic == current.h_cost and sideways_count < max_sideways:
                current = best_successor
                sideways_count += 1
            else:
                return None  # Stuck at local optimum or exceeded sideways limit
        
        return None  # Max iterations reached

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
    """Main function to demonstrate the 8-puzzle solver with Hill Climbing."""
    
    # Redirect output to file as well
    import sys
    from io import StringIO
    
    output_buffer = StringIO()
    
    def print_to_both(*args, **kwargs):
        """Print to both console and file buffer."""
        print(*args, **kwargs)
        print(*args, **kwargs, file=output_buffer)
    
    print_to_both("\n" + "="*70)
    print_to_both("8-PUZZLE PROBLEM SOLVER USING HILL CLIMBING APPROACH")
    print_to_both("="*70)
    
    print_to_both("\nProblem Description:")
    print_to_both("Hill Climbing is a local search algorithm that:")
    print_to_both("1. Starts from the initial state")
    print_to_both("2. Evaluates all neighboring states")
    print_to_both("3. Moves to the neighbor with the best (lowest) heuristic value")
    print_to_both("4. Repeats until goal is reached or no better neighbor exists")
    print_to_both("\nLimitation: Hill Climbing can get stuck at local optima.")
    print_to_both("Solution: Use Hill Climbing with Sideways Moves or Random Restarts.")
    
    # Define goal state for all tests
    goal_state = [
        [1, 2, 3],
        [8, 0, 4],
        [7, 6, 5]
    ]
    
    # Test Case 1: Simple case (1 move away) - Should work
    print_to_both("\n" + "="*70)
    print_to_both("TEST CASE 1: Simple Problem (1 move from goal)")
    print_to_both("="*70)
    
    initial_state1 = [
        [1, 2, 3],
        [8, 4, 0],
        [7, 6, 5]
    ]
    
    print_to_both("\nInitial State:")
    for row in initial_state1:
        print_to_both("  " + " ".join(str(x) if x != 0 else "-" for x in row))
    
    print_to_both("\nGoal State:")
    for row in goal_state:
        print_to_both("  " + " ".join(str(x) if x != 0 else "-" for x in row))
    
    print_to_both("\n[1] Solving with Hill Climbing (Manhattan Distance)...")
    print_to_both("-" * 70)
    
    solver1 = EightPuzzleSolver(initial_state1, goal_state)
    solution1 = solver1.hill_climbing_search(heuristic_type="manhattan")
    
    if solution1:
        path1 = solver1.get_solution_path(solution1)
        print_to_both(f"\n✓ SUCCESS! Hill Climbing found a solution.")
        print_to_both(f"  - Number of moves: {len(path1) - 1}")
        print_to_both(f"  - Nodes expanded: {solver1.nodes_expanded}")
        print_to_both(f"\nSolution Steps:")
        
        for i, state in enumerate(path1):
            print_to_both(f"\nStep {i}: {state.move}")
            print_to_both(f"  Heuristic cost (h): {state.h_cost}")
            for row in state.board:
                print_to_both("    " + " ".join(str(x) if x != 0 else "-" for x in row))
    else:
        print_to_both(f"\n❌ Hill Climbing got stuck at a local optimum!")
    
    # Test Case 2: Medium complexity (few moves away)
    print_to_both("\n" + "="*70)
    print_to_both("TEST CASE 2: Medium Complexity Problem")
    print_to_both("="*70)
    
    initial_state2 = [
        [1, 2, 3],
        [0, 8, 4],
        [7, 6, 5]
    ]
    
    print_to_both("\nInitial State:")
    for row in initial_state2:
        print_to_both("  " + " ".join(str(x) if x != 0 else "-" for x in row))
    
    print_to_both("\nGoal State:")
    for row in goal_state:
        print_to_both("  " + " ".join(str(x) if x != 0 else "-" for x in row))
    
    print_to_both("\n[2] Solving with Hill Climbing (Manhattan Distance)...")
    print_to_both("-" * 70)
    
    solver2 = EightPuzzleSolver(initial_state2, goal_state)
    solution2 = solver2.hill_climbing_search(heuristic_type="manhattan")
    
    if solution2:
        path2 = solver2.get_solution_path(solution2)
        print_to_both(f"\n✓ SUCCESS! Hill Climbing found a solution.")
        print_to_both(f"  - Number of moves: {len(path2) - 1}")
        print_to_both(f"  - Nodes expanded: {solver2.nodes_expanded}")
        print_to_both(f"\nSolution Steps:")
        
        for i, state in enumerate(path2):
            print_to_both(f"\nStep {i}: {state.move}")
            print_to_both(f"  Heuristic cost (h): {state.h_cost}")
            for row in state.board:
                print_to_both("    " + " ".join(str(x) if x != 0 else "-" for x in row))
    else:
        print_to_both(f"\n❌ Hill Climbing got stuck at a local optimum!")
        
        # Try with sideways moves
        print_to_both(f"\n[2b] Retrying with Hill Climbing + Sideways Moves...")
        print_to_both("-" * 70)
        
        solver2b = EightPuzzleSolver(initial_state2, goal_state)
        solution2b = solver2b.hill_climbing_with_sideways_moves(heuristic_type="manhattan")
        
        if solution2b:
            path2b = solver2b.get_solution_path(solution2b)
            print_to_both(f"\n✓ SUCCESS with sideways moves!")
            print_to_both(f"  - Number of moves: {len(path2b) - 1}")
            print_to_both(f"  - Nodes expanded: {solver2b.nodes_expanded}")
        else:
            print_to_both(f"\n❌ Still stuck at local optimum even with sideways moves.")
    
    # Test Case 3: Complex problem - likely to fail with basic Hill Climbing
    print_to_both("\n" + "="*70)
    print_to_both("TEST CASE 3: Complex Problem (Demonstrates Limitation)")
    print_to_both("="*70)
    
    initial_state3 = [
        [1, 2, 3],
        [8, 6, 4],
        [7, 0, 5]
    ]
    
    print_to_both("\nInitial State:")
    for row in initial_state3:
        print_to_both("  " + " ".join(str(x) if x != 0 else "-" for x in row))
    
    print_to_both("\nGoal State:")
    for row in goal_state:
        print_to_both("  " + " ".join(str(x) if x != 0 else "-" for x in row))
    
    print_to_both("\n[3] Solving with Hill Climbing (Manhattan Distance)...")
    print_to_both("-" * 70)
    
    solver3 = EightPuzzleSolver(initial_state3, goal_state)
    solution3 = solver3.hill_climbing_search(heuristic_type="manhattan")
    
    if solution3:
        path3 = solver3.get_solution_path(solution3)
        print_to_both(f"\n✓ SUCCESS! Hill Climbing found a solution.")
        print_to_both(f"  - Number of moves: {len(path3) - 1}")
        print_to_both(f"  - Nodes expanded: {solver3.nodes_expanded}")
    else:
        print_to_both(f"\n❌ Hill Climbing got stuck at a local optimum!")
        print_to_both("This demonstrates the main limitation of Hill Climbing.")
        
        # Try with sideways moves
        print_to_both(f"\n[3b] Retrying with Hill Climbing + Sideways Moves...")
        print_to_both("-" * 70)
        
        solver3b = EightPuzzleSolver(initial_state3, goal_state)
        solution3b = solver3b.hill_climbing_with_sideways_moves(heuristic_type="manhattan")
        
        if solution3b:
            path3b = solver3b.get_solution_path(solution3b)
            print_to_both(f"\n✓ SUCCESS with sideways moves!")
            print_to_both(f"  - Number of moves: {len(path3b) - 1}")
            print_to_both(f"  - Nodes expanded: {solver3b.nodes_expanded}")
        else:
            print_to_both(f"\n❌ Still stuck at local optimum even with sideways moves.")
    
    # Comparison with A* for reference
    print_to_both("\n" + "="*70)
    print_to_both("COMPARISON: Hill Climbing vs A* Search")
    print_to_both("="*70)
    
    print_to_both("\nFor TEST CASE 3, let's compare with A* Search:")
    print_to_both("-" * 70)
    
    solver_astar = EightPuzzleSolver(initial_state3, goal_state)
    solution_astar = solver_astar.a_star_search(heuristic_type="manhattan")
    
    if solution_astar:
        path_astar = solver_astar.get_solution_path(solution_astar)
        print_to_both(f"\nA* Search Results:")
        print_to_both(f"  - Moves: {len(path_astar) - 1}")
        print_to_both(f"  - Nodes Expanded: {solver_astar.nodes_expanded}")
        print_to_both(f"  - Status: ✓ Found optimal solution")
    
    # Summary
    print_to_both("\n" + "="*70)
    print_to_both("ALGORITHM COMPARISON SUMMARY")
    print_to_both("="*70)
    print_to_both("\n┌──────────────────────────────┬────────────┬─────────────────┐")
    print_to_both("│ Algorithm                    │ Test Case  │ Result          │")
    print_to_both("├──────────────────────────────┼────────────┼─────────────────┤")
    
    if solution1:
        moves1 = len(path1)-1
        move_word1 = "move" if moves1 == 1 else "moves"
        print_to_both(f"│ Hill Climbing (Manhattan)    │     1      │ ✓ Success ({moves1} {move_word1}) │")
    else:
        print_to_both("│ Hill Climbing (Manhattan)    │     1      │ ❌ Failed       │")
    
    if solution2:
        moves2 = len(path2)-1
        move_word2 = "move" if moves2 == 1 else "moves"
        print_to_both(f"│ Hill Climbing (Manhattan)    │     2      │ ✓ Success ({moves2} {move_word2}) │")
    else:
        print_to_both("│ Hill Climbing (Manhattan)    │     2      │ ❌ Failed       │")
    
    if solution3:
        moves3 = len(path3)-1
        move_word3 = "move" if moves3 == 1 else "moves"
        print_to_both(f"│ Hill Climbing (Manhattan)    │     3      │ ✓ Success ({moves3} {move_word3}) │")
    else:
        print_to_both("│ Hill Climbing (Manhattan)    │     3      │ ❌ Failed       │")
    
    moves_astar = len(path_astar)-1
    move_word_astar = "move" if moves_astar == 1 else "moves"
    print_to_both(f"│ A* Search (Manhattan)        │     3      │ ✓ Success ({moves_astar} {move_word_astar}) │")
    print_to_both("└──────────────────────────────┴────────────┴─────────────────┘")
    
    print_to_both("\n" + "="*70)
    print_to_both("KEY OBSERVATIONS")
    print_to_both("="*70)
    print_to_both("\n✓ Advantages of Hill Climbing:")
    print_to_both("  • Very fast for simple problems (fewer nodes expanded)")
    print_to_both("  • Low memory requirements")
    print_to_both("  • Simple to implement and understand")
    
    print_to_both("\n❌ Limitations of Hill Climbing:")
    print_to_both("  • Can get stuck at local optima")
    print_to_both("  • May fail to find a solution even when one exists")
    print_to_both("  • Not guaranteed to find the optimal solution")
    
    print_to_both("\n💡 Improvements:")
    print_to_both("  • Hill Climbing with Sideways Moves: Helps escape plateaus")
    print_to_both("  • Random Restart: Try multiple starting points")
    print_to_both("  • Simulated Annealing: Allow occasional uphill moves")
    
    print_to_both("\n✓ Advantages of A* Search:")
    print_to_both("  • Guaranteed to find optimal solution (if exists)")
    print_to_both("  • Complete: Always finds solution if one exists")
    print_to_both("  • Uses admissible heuristics effectively")
    
    print_to_both("\n" + "="*70)
    print_to_both("END OF 8-PUZZLE PROBLEM DEMONSTRATION")
    print_to_both("="*70)
    print_to_both()
    
    # Save output to file
    output_file = "eight_puzzle_hill_climbing_output.txt"
    with open(output_file, 'w') as f:
        f.write(output_buffer.getvalue())
    
    print(f"\n✓ Output saved to: {output_file}")


if __name__ == "__main__":
    main()
