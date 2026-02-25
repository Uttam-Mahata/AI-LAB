import heapq
import math

class AStarSolver:
    def __init__(self, grid, start, goal, allow_diagonal=True):
        self.grid = grid
        self.rows = len(grid)
        self.cols = len(grid[0])
        self.start = start
        self.goal = goal
        self.allow_diagonal = allow_diagonal

    def heuristic(self, a, b):
        """
        Calculates the Euclidean distance between node a and node b.
        
        """
        return math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)

    def get_neighbors(self, node):
        """
        Returns valid neighbors for a given node (r, c).
        """
        neighbors = []
        r, c = node
        
        # Cardinal directions: Cost 1
        moves = [
            (0, 1, 1), (0, -1, 1), (1, 0, 1), (-1, 0, 1)
        ]
        
        # Diagonals: Cost sqrt(2) ~= 1.414
        if self.allow_diagonal:
            diag_cost = math.sqrt(2)
            moves.extend([
                (1, 1, diag_cost), (1, -1, diag_cost), 
                (-1, 1, diag_cost), (-1, -1, diag_cost)
            ])

        for dr, dc, cost in moves:
            nr, nc = r + dr, c + dc

            # Checking bounds
            if 0 <= nr < self.rows and 0 <= nc < self.cols:
                # Checking if obstacle (1 is obstacle, 0 is free)
                if self.grid[nr][nc] == 0:
                    # Corner-cutting prevention for diagonal moves
                    if abs(dr) + abs(dc) == 2:
                        if self.grid[r + dr][c] == 1 or self.grid[r][c + dc] == 1:
                            continue
                    neighbors.append(((nr, nc), cost))
                    
        return neighbors

    def solve(self):
        open_set = []
        heapq.heappush(open_set, (0, self.start))
        
        # Path Reconstruction
        came_from = {}
        
        g_score = {node: float('inf') for r in range(self.rows) for c in range(self.cols) for node in [(r, c)]}
        g_score[self.start] = 0
        
        f_score = {node: float('inf') for r in range(self.rows) for c in range(self.cols) for node in [(r, c)]}
        f_score[self.start] = self.heuristic(self.start, self.goal)

        nodes_visited = 0

        while open_set:
            current_f, current = heapq.heappop(open_set)
            nodes_visited += 1

            if current == self.goal:
                return self.reconstruct_path(came_from, current), g_score[self.goal]

            for neighbor, move_cost in self.get_neighbors(current):
                tentative_g = g_score[current] + move_cost

                if tentative_g < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g
                    f = tentative_g + self.heuristic(neighbor, self.goal)
                    f_score[neighbor] = f
                    
                    heapq.heappush(open_set, (f, neighbor))

        return None, float('inf') # No path found

    def reconstruct_path(self, came_from, current):
        total_path = [current]
        while current in came_from:
            current = came_from[current]
            total_path.append(current)
        return total_path[::-1]



grid_layout = [
    [0, 0, 0, 0, 1, 1, 1, 1],
    [0, 0, 0, 1, 1, 1, 1, 1],
    [1, 0, 0, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0]
]

start_pos = (0, 0)
end_pos = (3, 7)  

solver = AStarSolver(grid_layout, start_pos, end_pos)
path, cost = solver.solve()

print(f"Path found: {path}")
print(f"Total Movement Cost (g): {cost:.4f}\n")

print("Grid Visualization:")
print("S: Start, E: End, #: Obstacle, .: Empty, *: Path")
print("-" * 20)

grid_visual = [['.' if cell == 0 else '#' for cell in row] for row in grid_layout]

for r, c in path:
    if (r, c) != start_pos and (r, c) != end_pos:
        grid_visual[r][c] = '*'

grid_visual[start_pos[0]][start_pos[1]] = 'S'
grid_visual[end_pos[0]][end_pos[1]] = 'E'

for row in grid_visual:
    print(" ".join(row))
print("-" * 20)

with open("output.txt", "w") as f:
    f.write(f"Path found: {path}\n")
    f.write(f"Total Movement Cost (g): {cost:.4f}\n\n")
    f.write("Grid Visualization:\n")
    f.write("S: Start, E: End, #: Obstacle, .: Empty, *: Path\n")
    f.write("-" * 20 + "\n")
    for row in grid_visual:
        f.write(" ".join(row) + "\n")
    f.write("-" * 20 + "\n")
