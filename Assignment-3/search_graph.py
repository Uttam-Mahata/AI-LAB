class Graph:
    def __init__(self, heuristics, graph_structure):
        self.heuristics = heuristics
        self.graph = graph_structure
        self.solution_graph = {}
        self.status = {}  

    def get_neighbors(self, node):
        return self.graph.get(node, [])

    def get_heuristic(self, node):
        return self.heuristics.get(node, 0)

    def get_status(self, node):
        return self.status.get(node, False)

    def set_status(self, node, val):
        self.status[node] = val

    def compute_minimum_cost_child_nodes(self, v):
        minimum_cost = float('inf')
        cost_to_child_node_list_dict = {}
        cost_to_child_node_list_dict[minimum_cost] = []
        flag = True

        for child_node_list in self.get_neighbors(v):
            cost = 0
            node_list = []
            for c_node in child_node_list:
                path_cost = 1
                cost = cost + self.get_heuristic(c_node) + path_cost
                node_list.append(c_node)
            
            if cost < minimum_cost:
                minimum_cost = cost
                cost_to_child_node_list_dict[minimum_cost] = node_list
        
        return minimum_cost, cost_to_child_node_list_dict[minimum_cost]

    def ao_star(self, v, backtracking):
        print(f"PROCESSING NODE : {v}")
        print(f"HEURISTIC VALUES : {self.heuristics}")
        print(f"SOLUTION GRAPH : {self.solution_graph}")
        print("-----------------------------------------------------------------------------------------")
        
        if self.get_status(v):
            return

        child_node_list = self.get_neighbors(v)
        if not child_node_list: # Leaf node
             self.set_status(v, True)
             return

        min_cost, child_node_list = self.compute_minimum_cost_child_nodes(v)
        
        self.heuristics[v] = min_cost
        self.set_status(v, True) 
        
        # Track the best branch in solution graph
        self.solution_graph[v] = child_node_list
        
        
        if backtracking:
           
            for child in child_node_list:
                self.set_status(child, False) 
                self.ao_star(child, backtracking)

def main():

    h = {
        'A': 0, 
        'B': 4, 
        'E': 3, 
        'D': 10,
        'H': 2, 
        'K': 3,
        'I': 8, 
        'L': 5 
    }


    graph = {
        'A': [['B', 'E'], ['D']], 
        'B': [['H', 'K']],
        'E': [['H', 'K']],
        'H': [['I']],
        'I': [['L']],
        'K': [['L']], 
        'D': [],
        'L': []
    }

    print("Starting AO* Search...\n")
    ao_star_solver = Graph(h, graph)
    
    ao_star_solver.ao_star('A', True)

    print("\nFINAL SOLUTION:")
    print(f"Optimal Cost at Root A: {ao_star_solver.heuristics['A']}")
    print(f"Solution Graph Structure: {ao_star_solver.solution_graph}")

if __name__ == "__main__":
    main()