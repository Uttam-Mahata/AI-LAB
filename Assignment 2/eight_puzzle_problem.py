from typing import List, Tuple, Optional
from copy import deepcopy


class PuzzleState:
    BOARD_SIZE = 3
    
    def __init__(self, board: List[List[int]], parent=None, move: str = "Initial"):
        self.board = board
        self.h_cost = 0
        self.parent = parent
        self.move = move
        self.empty_pos = self._find_empty()
    
    def _find_empty(self) -> Tuple[int, int]:
        for i in range(self.BOARD_SIZE):
            for j in range(self.BOARD_SIZE):
                if self.board[i][j] == 0:
                    return (i, j)
        return (0, 0)
    
    def __eq__(self, other):
        return self.board == other.board
    
    def __hash__(self):
        return hash(str(self.board))
    
    def get_board_tuple(self) -> Tuple:
        return tuple(tuple(row) for row in self.board)
    
    def print_board(self):
        for row in self.board:
            print(" ".join(str(cell) if cell != 0 else "-" for cell in row))


class EightPuzzleSolver:
    
    def __init__(self, initial_state: List[List[int]], goal_state: List[List[int]]):
        self.initial_state = PuzzleState(initial_state)
        self.goal_state = PuzzleState(goal_state)
        self.goal_positions = self._compute_goal_positions()
        self.nodes_expanded = 0
    
    def _compute_goal_positions(self) -> dict:
        positions = {}
        for i in range(PuzzleState.BOARD_SIZE):
            for j in range(PuzzleState.BOARD_SIZE):
                tile = self.goal_state.board[i][j]
                if tile != 0:
                    positions[tile] = (i, j)
        return positions
    
    def get_successors(self, state: PuzzleState) -> List[PuzzleState]:
        successors = []
        row, col = state.empty_pos
        moves = [(-1, 0, "Up"), (1, 0, "Down"), (0, -1, "Left"), (0, 1, "Right")]
        
        for dr, dc, move_name in moves:
            new_row, new_col = row + dr, col + dc
            
            if 0 <= new_row < PuzzleState.BOARD_SIZE and 0 <= new_col < PuzzleState.BOARD_SIZE:
                new_board = deepcopy(state.board)
                new_board[row][col], new_board[new_row][new_col] = \
                    new_board[new_row][new_col], new_board[row][col]
                
                new_state = PuzzleState(new_board, state, move_name)
                successors.append(new_state)
        
        return successors
    
    def heuristic_misplaced_tiles(self, state: PuzzleState) -> int:
        count = 0
        for i in range(PuzzleState.BOARD_SIZE):
            for j in range(PuzzleState.BOARD_SIZE):
                if state.board[i][j] != 0 and \
                   state.board[i][j] != self.goal_state.board[i][j]:
                    count += 1
        return count
    
    def heuristic_manhattan_distance(self, state: PuzzleState) -> int:
        distance = 0
        for i in range(PuzzleState.BOARD_SIZE):
            for j in range(PuzzleState.BOARD_SIZE):
                tile = state.board[i][j]
                if tile != 0:
                    goal_row, goal_col = self.goal_positions[tile]
                    distance += abs(i - goal_row) + abs(j - goal_col)
        return distance
    
    def hill_climbing_search(self, heuristic_type: str = "manhattan", max_iterations: int = 10000) -> Optional[PuzzleState]:
        if heuristic_type == "misplaced":
            heuristic_func = self.heuristic_misplaced_tiles
        else:
            heuristic_func = self.heuristic_manhattan_distance
        
        current = self.initial_state
        current.h_cost = heuristic_func(current)
        
        self.nodes_expanded = 0
        visited_states = set()
        
        for iteration in range(max_iterations):
            if current.board == self.goal_state.board:
                return current
            
            visited_states.add(current.get_board_tuple())
            successors = self.get_successors(current)
            self.nodes_expanded += 1
            
            best_successor = None
            best_heuristic = float('inf')
            
            for successor in successors:
                if successor.get_board_tuple() in visited_states:
                    continue
                    
                successor.h_cost = heuristic_func(successor)
                
                if successor.h_cost < best_heuristic:
                    best_heuristic = successor.h_cost
                    best_successor = successor
            
            if best_successor is None or best_heuristic >= current.h_cost:
                return None
            
            current = best_successor
        
        return None

    def hill_climbing_with_sideways_moves(self, heuristic_type: str = "manhattan", max_iterations: int = 10000, max_sideways: int = 100) -> Optional[PuzzleState]:
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
            if current.board == self.goal_state.board:
                return current
            
            visited_states.add(current.get_board_tuple())
            successors = self.get_successors(current)
            self.nodes_expanded += 1
            
            best_successor = None
            best_heuristic = float('inf')
            
            for successor in successors:
                if successor.get_board_tuple() in visited_states:
                    continue
                    
                successor.h_cost = heuristic_func(successor)
                
                if successor.h_cost < best_heuristic:
                    best_heuristic = successor.h_cost
                    best_successor = successor
            
            if best_successor is None:
                return None
            
            if best_heuristic < current.h_cost:
                current = best_successor
                sideways_count = 0
            elif best_heuristic == current.h_cost and sideways_count < max_sideways:
                current = best_successor
                sideways_count += 1
            else:
                return None
        
        return None


    def get_solution_path(self, goal_state: PuzzleState) -> List[PuzzleState]:
        path = []
        current = goal_state
        while current is not None:
            path.append(current)
            current = current.parent
        return list(reversed(path))


def main():
    from io import StringIO
    
    output_buffer = StringIO()
    
    def print_to_both(*args, **kwargs):
        print(*args, **kwargs)
        print(*args, **kwargs, file=output_buffer)
    
    print_to_both("\n" + "="*70)
    print_to_both("8-PUZZLE PROBLEM SOLVER - HILL CLIMBING")
    print_to_both("="*70)
    
    goal_state = [[1, 2, 3], [8, 0, 4], [7, 6, 5]]
    
    # Test Case 1
    print_to_both("\n" + "="*70)
    print_to_both("TEST CASE 1: Simple Problem")
    print_to_both("="*70)
    
    initial_state1 = [[1, 2, 3], [8, 4, 0], [7, 6, 5]]
    
    print_to_both("\nInitial State:")
    for row in initial_state1:
        print_to_both("  " + " ".join(str(x) if x != 0 else "-" for x in row))
    
    print_to_both("\nGoal State:")
    for row in goal_state:
        print_to_both("  " + " ".join(str(x) if x != 0 else "-" for x in row))
    
    solver1 = EightPuzzleSolver(initial_state1, goal_state)
    solution1 = solver1.hill_climbing_search(heuristic_type="manhattan")
    
    if solution1:
        path1 = solver1.get_solution_path(solution1)
        print_to_both(f"\n✓ Success! Moves: {len(path1) - 1}, Nodes: {solver1.nodes_expanded}")
        print_to_both("\nSolution Steps:")
        
        for i, state in enumerate(path1):
            print_to_both(f"\nStep {i}: {state.move} (h={state.h_cost})")
            for row in state.board:
                print_to_both("    " + " ".join(str(x) if x != 0 else "-" for x in row))
    else:
        print_to_both("\n❌ Stuck at local optimum")
    
    # Test Case 2
    print_to_both("\n" + "="*70)
    print_to_both("TEST CASE 2: Medium Complexity")
    print_to_both("="*70)
    
    initial_state2 = [[1, 2, 3], [0, 8, 4], [7, 6, 5]]
    
    print_to_both("\nInitial State:")
    for row in initial_state2:
        print_to_both("  " + " ".join(str(x) if x != 0 else "-" for x in row))
    
    solver2 = EightPuzzleSolver(initial_state2, goal_state)
    solution2 = solver2.hill_climbing_search(heuristic_type="manhattan")
    
    if solution2:
        path2 = solver2.get_solution_path(solution2)
        print_to_both(f"\n✓ Success! Moves: {len(path2) - 1}, Nodes: {solver2.nodes_expanded}")
    else:
        print_to_both("\n❌ Stuck at local optimum")
        
        print_to_both("\nRetrying with sideways moves...")
        solver2b = EightPuzzleSolver(initial_state2, goal_state)
        solution2b = solver2b.hill_climbing_with_sideways_moves(heuristic_type="manhattan")
        
        if solution2b:
            path2b = solver2b.get_solution_path(solution2b)
            print_to_both(f"✓ Success with sideways! Moves: {len(path2b) - 1}, Nodes: {solver2b.nodes_expanded}")
        else:
            print_to_both("❌ Still stuck")
    
    # Test Case 3
    print_to_both("\n" + "="*70)
    print_to_both("TEST CASE 3: Complex Problem")
    print_to_both("="*70)
    
    initial_state3 = [[1, 2, 3], [8, 6, 4], [7, 0, 5]]
    
    print_to_both("\nInitial State:")
    for row in initial_state3:
        print_to_both("  " + " ".join(str(x) if x != 0 else "-" for x in row))
    
    solver3 = EightPuzzleSolver(initial_state3, goal_state)
    solution3 = solver3.hill_climbing_search(heuristic_type="manhattan")
    
    if solution3:
        path3 = solver3.get_solution_path(solution3)
        print_to_both(f"\n✓ Success! Moves: {len(path3) - 1}, Nodes: {solver3.nodes_expanded}")
    else:
        print_to_both("\n❌ Stuck at local optimum")
        
        print_to_both("\nRetrying with sideways moves...")
        solver3b = EightPuzzleSolver(initial_state3, goal_state)
        solution3b = solver3b.hill_climbing_with_sideways_moves(heuristic_type="manhattan")
        
        if solution3b:
            path3b = solver3b.get_solution_path(solution3b)
            print_to_both(f"✓ Success with sideways! Moves: {len(path3b) - 1}, Nodes: {solver3b.nodes_expanded}")
        else:
            print_to_both("❌ Still stuck")
    
    print_to_both("\n" + "="*70)
    print_to_both("Summary:")
    print_to_both("Hill Climbing is fast but can get stuck at local optima.")
    print_to_both("Sideways moves can help escape plateaus.")
    print_to_both("="*70)
    print_to_both()
    
    output_file = "eight_puzzle_hill_climbing_output.txt"
    with open(output_file, 'w') as f:
        f.write(output_buffer.getvalue())
    
    print(f"\n✓ Output saved to: {output_file}")


if __name__ == "__main__":
    main()
