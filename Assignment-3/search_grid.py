import math
import heapq

class Node:
    def __init__(self, x, y, parent=None):
        self.x = x
        self.y = y
        self.parent = parent
        self.g = 0  # Cost from start to current node
        self.h = 0  # Heuristic cost from current node to end
        self.f = 0  # Total cost (g + h)

    def __lt__(self, other):
        return self.f < other.f

def get_neighbors(node, grid_rows, grid_cols):
    """Returns valid neighbors including diagonals."""
    neighbors = []
    directions = [
        (-1, 0), (1, 0), (0, -1), (0, 1),   # Cardinals
        (-1, -1), (-1, 1), (1, -1), (1, 1)  # Diagonals
    ]

    for dx, dy in directions:
        nx, ny = node.x + dx, node.y + dy
        if 0 <= nx < grid_rows and 0 <= ny < grid_cols:
            neighbors.append((nx, ny))
    return neighbors

def heuristic(node, end_node):
    """Euclidean distance heuristic for 8-direction movement."""
    return math.sqrt((node.x - end_node.x)**2 + (node.y - end_node.y)**2)

def solve_a_star(grid_map, start_coords, end_coords):
    rows = len(grid_map)
    cols = len(grid_map[0])

    start_node = Node(start_coords[0], start_coords[1])
    end_node = Node(end_coords[0], end_coords[1])

    open_list = []
    closed_set = set()
    
    heapq.heappush(open_list, start_node)

    g_score_map = {(start_node.x, start_node.y): 0}

    while open_list:
        current_node = heapq.heappop(open_list)
        
        # If we reached the destination
        if current_node.x == end_node.x and current_node.y == end_node.y:
            path = []
            curr = current_node
            while curr:
                path.append((curr.x, curr.y))
                curr = curr.parent
            return path[::-1] 

        closed_set.add((current_node.x, current_node.y))

        for nx, ny in get_neighbors(current_node, rows, cols):
            # 1. Check bounds and obstacles
            if grid_map[nx][ny] == 1:
                continue
            if (nx, ny) in closed_set:
                continue

            # 2. Calculate tentative g cost
            dist_cost = math.sqrt((nx - current_node.x)**2 + (ny - current_node.y)**2)
            tentative_g = current_node.g + dist_cost

            if (nx, ny) in g_score_map and tentative_g >= g_score_map[(nx, ny)]:
                continue

            # 4. Create new neighbor node
            neighbor = Node(nx, ny, current_node)
            neighbor.g = tentative_g
            neighbor.h = heuristic(neighbor, end_node)
            neighbor.f = neighbor.g + neighbor.h
            
            g_score_map[(nx, ny)] = tentative_g
            heapq.heappush(open_list, neighbor)

    return None # No path found

def main():

    
    grid = [
        [0, 0, 0, 0, 1, 1, 1, 1], # Row 0
        [0, 0, 1, 1, 1, 1, 1, 1], # Row 1
        [1, 1, 0, 1, 1, 1, 1, 1], # Row 2
        [1, 0, 0, 0, 0, 0, 0, 0]  # Row 3
    ]

    start = (0, 0)
    end = (3, 7)

    path = solve_a_star(grid, start, end)

    # Visualization
    output_grid = [[' ' for _ in range(8)] for _ in range(4)]
    

    for r in range(4):
        for c in range(8):
            if grid[r][c] == 1:
                output_grid[r][c] = '#'
            else:
                output_grid[r][c] = '.'

    if path:
        for (r, c) in path:
            output_grid[r][c] = '*'
    

    output_grid[start[0]][start[1]] = 'S'
    output_grid[end[0]][end[1]] = 'E'

    print("A* Algorithm Solution (Grid Visualization):")
    for row in output_grid:
        print(" ".join(row))

if __name__ == "__main__":
    main()