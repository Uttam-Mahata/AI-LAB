
import sys

import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'Assignment 2'))

from water_jug_problem import WaterJugProblem
from eight_puzzle_problem import EightPuzzleSolver


def demo_water_jug():
    """Demonstration of the Water Jug Problem."""
    print("\n" + "="*70)
    print(" WATER JUG PROBLEM DEMONSTRATION ".center(70))
    print("="*70)
    
    print("\nProblem Setup:")
    print("  - Jug 1 Capacity: 3 liters")
    print("  - Jug 2 Capacity: 4 liters")
    print("  - Goal: Get exactly 2 liters in Jug 2")
    print("  - Initial State: Both jugs empty (0, 0)")
    
    # Solve with BFS
    problem = WaterJugProblem(jug1_capacity=3, jug2_capacity=4,
                              goal_state=(0, 2), initial_state=(0, 0))
    solution = problem.bfs()
    
    if solution:
        problem.print_solution(solution, "BFS")
        
        # Count paths
        problem2 = WaterJugProblem(jug1_capacity=3, jug2_capacity=4,
                                   goal_state=(0, 2), initial_state=(0, 0))
        path_count = problem2.count_all_paths_dfs()
        print(f"\n Statistics:")
        print(f"  - Solution length: {len(solution)} steps")
        print(f"  - Total paths to goal: {path_count}")


def demo_eight_puzzle():
    """Demonstrate the 8-Puzzle Problem solution."""
    print("\n" + "="*70)
    print(" 8-PUZZLE PROBLEM DEMONSTRATION ".center(70))
    print("="*70)
    
    initial = [[1, 2, 3], [8, 0, 4], [7, 6, 5]]
    goal = [[2, 8, 1], [0, 4, 3], [7, 6, 5]]
    
    print("\nProblem Setup:")
    print("  Initial State:")
    for row in initial:
        print("    " + " ".join(str(x) if x != 0 else "-" for x in row))
    
    print("\n  Goal State:")
    for row in goal:
        print("    " + " ".join(str(x) if x != 0 else "-" for x in row))
    
    # Solve with both heuristics
    print("\n" + "-"*70)
    print("Solving with A* using Misplaced Tiles Heuristic...")
    solver1 = EightPuzzleSolver(initial, goal)
    solution1 = solver1.a_star_search('misplaced')
    path1 = solver1.get_solution_path(solution1)
    
    print("\n" + "-"*70)
    print("Solving with A* using Manhattan Distance Heuristic...")
    solver2 = EightPuzzleSolver(initial, goal)
    solution2 = solver2.a_star_search('manhattan')
    path2 = solver2.get_solution_path(solution2)
    
    # Display comparison
    print("\n" + "="*70)
    print(" HEURISTIC COMPARISON ".center(70))
    print("="*70)
    
    print("\n┌─────────────────────────┬──────────────┬──────────────────┐")
    print("│ Heuristic               │ Moves        │ Nodes Expanded   │")
    print("├─────────────────────────┼──────────────┼──────────────────┤")
    print(f"│ Misplaced Tiles         │ {len(path1)-1:^12} │ {solver1.nodes_expanded:^16} │")
    print(f"│ Manhattan Distance      │ {len(path2)-1:^12} │ {solver2.nodes_expanded:^16} │")
    print("└─────────────────────────┴──────────────┴──────────────────┘")
    
    efficiency = ((solver1.nodes_expanded - solver2.nodes_expanded) / 
                  solver1.nodes_expanded * 100)
    print(f"\n Manhattan Distance is {efficiency:.1f}% more efficient!")
    
    # Show a few steps of the solution
    print("\n" + "-"*70)
    print("First 3 steps of solution (Manhattan Distance):")
    for i in range(min(4, len(path2))):
        state = path2[i]
        print(f"\nStep {i}: {state.move}")
        state.print_board()


def main():
    """Main demonstration function."""
    print("\n" + "="*70)
    
    demo_water_jug()
    
    print("\n" + "="*70)

    
    demo_eight_puzzle()
    
    print("\n" + "="*70)
    print("\n")


if __name__ == "__main__":
    main()
