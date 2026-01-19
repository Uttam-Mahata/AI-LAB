"""
Water Jug Problem Solver using DFS and BFS

This module solves the classic water jug problem where we have two jugs
of different capacities and need to measure a specific amount of water.

Problem: Given a 3-liter jug and a 4-liter jug, measure exactly 2 liters
in the 4-liter jug using only fill, empty, and pour operations.
"""

from collections import deque
from typing import List, Tuple, Set, Optional


class WaterJugProblem:
    """
    Solver for the water jug problem using search algorithms.
    
    Attributes:
        jug1_capacity: Maximum capacity of the first jug
        jug2_capacity: Maximum capacity of the second jug
        goal_state: Target state (jug1_amount, jug2_amount)
        initial_state: Starting state (default: (0, 0))
    """
    
    def __init__(self, jug1_capacity: int, jug2_capacity: int, 
                 goal_state: Tuple[int, int], initial_state: Tuple[int, int] = (0, 0)):
        """
        Initialize the water jug problem.
        
        Args:
            jug1_capacity: Capacity of jug 1
            jug2_capacity: Capacity of jug 2
            goal_state: Target state (jug1, jug2)
            initial_state: Initial state (default: (0, 0))
        """
        self.jug1_capacity = jug1_capacity
        self.jug2_capacity = jug2_capacity
        self.goal_state = goal_state
        self.initial_state = initial_state
        self.path_count = 0
        self.max_depth = 20  # Maximum depth for path counting to avoid infinite loops
    
    def get_successors(self, state: Tuple[int, int]) -> List[Tuple[Tuple[int, int], str]]:
        """
        Generate all possible successor states from current state.
        
        Operations:
        1. Fill jug 1
        2. Fill jug 2
        3. Empty jug 1
        4. Empty jug 2
        5. Pour from jug 1 to jug 2
        6. Pour from jug 2 to jug 1
        
        Args:
            state: Current state (jug1, jug2)
            
        Returns:
            List of (next_state, action) tuples
        """
        jug1, jug2 = state
        successors = []
        
        # Operation 1: Fill jug 1
        if jug1 < self.jug1_capacity:
            successors.append(((self.jug1_capacity, jug2), "Fill Jug1"))
        
        # Operation 2: Fill jug 2
        if jug2 < self.jug2_capacity:
            successors.append(((jug1, self.jug2_capacity), "Fill Jug2"))
        
        # Operation 3: Empty jug 1
        if jug1 > 0:
            successors.append(((0, jug2), "Empty Jug1"))
        
        # Operation 4: Empty jug 2
        if jug2 > 0:
            successors.append(((jug1, 0), "Empty Jug2"))
        
        # Operation 5: Pour from jug 1 to jug 2
        if jug1 > 0 and jug2 < self.jug2_capacity:
            pour_amount = min(jug1, self.jug2_capacity - jug2)
            successors.append(((jug1 - pour_amount, jug2 + pour_amount), 
                             "Pour Jug1->Jug2"))
        
        # Operation 6: Pour from jug 2 to jug 1
        if jug2 > 0 and jug1 < self.jug1_capacity:
            pour_amount = min(jug2, self.jug1_capacity - jug1)
            successors.append(((jug1 + pour_amount, jug2 - pour_amount), 
                             "Pour Jug2->Jug1"))
        
        return successors
    
    def dfs(self) -> Optional[List[Tuple[Tuple[int, int], str]]]:
        """
        Solve the water jug problem using Depth First Search.
        
        Returns:
            List of (state, action) tuples representing the solution path,
            or None if no solution exists.
        """
        stack = [(self.initial_state, [])]
        visited = set()
        all_paths = []
        
        while stack:
            state, path = stack.pop()
            
            if state in visited:
                continue
            
            visited.add(state)
            
            # Check if goal is reached
            if state == self.goal_state:
                all_paths.append(path + [(state, "Goal Reached")])
                self.path_count += 1
                if len(all_paths) == 1:  # Return first path found
                    return path + [(state, "Goal Reached")]
            
            # Explore successors
            for next_state, action in self.get_successors(state):
                if next_state not in visited:
                    stack.append((next_state, path + [(state, action)]))
        
        return None
    
    def bfs(self) -> Optional[List[Tuple[Tuple[int, int], str]]]:
        """
        Solve the water jug problem using Breadth First Search.
        
        Returns:
            List of (state, action) tuples representing the solution path,
            or None if no solution exists.
        """
        queue = deque([(self.initial_state, [])])
        visited = set()
        visited.add(self.initial_state)
        all_paths = []
        
        while queue:
            state, path = queue.popleft()
            
            # Check if goal is reached
            if state == self.goal_state:
                all_paths.append(path + [(state, "Goal Reached")])
                self.path_count += 1
                return path + [(state, "Goal Reached")]
            
            # Explore successors
            for next_state, action in self.get_successors(state):
                if next_state not in visited:
                    visited.add(next_state)
                    queue.append((next_state, path + [(state, action)]))
        
        return None
    
    def count_all_paths_dfs(self) -> int:
        """
        Count all possible paths to the goal state using DFS.
        
        Returns:
            Number of different paths to reach the goal state.
        """
        stack = [(self.initial_state, [self.initial_state])]
        visited_paths = set()
        path_count = 0
        
        while stack:
            state, path = stack.pop()
            
            # Check if goal is reached
            if state == self.goal_state:
                path_tuple = tuple(path)
                if path_tuple not in visited_paths:
                    visited_paths.add(path_tuple)
                    path_count += 1
                continue
            
            # Avoid cycles in current path
            if len(path) > self.max_depth:
                continue
            
            # Explore successors
            for next_state, action in self.get_successors(state):
                if next_state not in path:  # Avoid cycles
                    stack.append((next_state, path + [next_state]))
        
        return path_count
    
    def print_solution(self, solution: List[Tuple[Tuple[int, int], str]], 
                      algorithm: str):
        """
        Print the solution path in a readable format.
        
        Args:
            solution: List of (state, action) tuples
            algorithm: Name of the algorithm used
        """
        print(f"\n{'='*60}")
        print(f"Solution using {algorithm}")
        print(f"{'='*60}")
        print(f"Initial State: {self.initial_state}")
        print(f"Goal State: {self.goal_state}")
        print(f"Jug Capacities: Jug1={self.jug1_capacity}L, Jug2={self.jug2_capacity}L")
        print(f"\nSteps to reach goal:")
        print(f"{'Step':<6} {'Action':<20} {'Jug1':<8} {'Jug2':<8}")
        print("-" * 60)
        
        print(f"{'0':<6} {'Initial State':<20} {self.initial_state[0]:<8} {self.initial_state[1]:<8}")
        
        for i, (state, action) in enumerate(solution, 1):
            print(f"{i:<6} {action:<20} {state[0]:<8} {state[1]:<8}")
        
        print(f"\nTotal steps: {len(solution)}")


def main():
    """Main function to demonstrate the water jug problem solver."""
    
    # Problem 1: Original problem (3L, 4L jugs, goal: 2L in 4L jug)
    print("\n" + "="*60)
    print("WATER JUG PROBLEM SOLVER")
    print("="*60)
    
    print("\nProblem 1: 3L and 4L jugs, Goal: (0, 2)")
    print("-" * 60)
    
    problem1 = WaterJugProblem(jug1_capacity=3, jug2_capacity=4, 
                                goal_state=(0, 2), initial_state=(0, 0))
    
    # Solve using DFS
    print("\n[1] Solving with Depth First Search (DFS)...")
    solution_dfs = problem1.dfs()
    if solution_dfs:
        problem1.print_solution(solution_dfs, "DFS")
    else:
        print("No solution found using DFS")
    
    # Solve using BFS
    print("\n[2] Solving with Breadth First Search (BFS)...")
    problem2 = WaterJugProblem(jug1_capacity=3, jug2_capacity=4, 
                                goal_state=(0, 2), initial_state=(0, 0))
    solution_bfs = problem2.bfs()
    if solution_bfs:
        problem2.print_solution(solution_bfs, "BFS")
    else:
        print("No solution found using BFS")
    
    # Count all paths
    print("\n[3] Counting all possible paths to goal state...")
    problem3 = WaterJugProblem(jug1_capacity=3, jug2_capacity=4, 
                                goal_state=(0, 2), initial_state=(0, 0))
    path_count = problem3.count_all_paths_dfs()
    print(f"Total number of different paths to reach goal state: {path_count}")
    
    # Problem 2: Different goal state (2L in 3L jug)
    print("\n\n" + "="*60)
    print("Problem 2: 3L and 4L jugs, Goal: (2, 0)")
    print("-" * 60)
    
    problem4 = WaterJugProblem(jug1_capacity=3, jug2_capacity=4, 
                                goal_state=(2, 0), initial_state=(0, 0))
    solution_bfs2 = problem4.bfs()
    if solution_bfs2:
        problem4.print_solution(solution_bfs2, "BFS")
    else:
        print("No solution found")
    
    # Problem 3: Different capacities
    print("\n\n" + "="*60)
    print("Problem 3: 5L and 3L jugs, Goal: (4, 0)")
    print("-" * 60)
    
    problem5 = WaterJugProblem(jug1_capacity=5, jug2_capacity=3, 
                                goal_state=(4, 0), initial_state=(0, 0))
    solution_bfs3 = problem5.bfs()
    if solution_bfs3:
        problem5.print_solution(solution_bfs3, "BFS")
    else:
        print("No solution found")


if __name__ == "__main__":
    main()
