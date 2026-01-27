#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "water_jug_problem.h"
#include "eight_puzzle_problem.h"

void demo_water_jug() {
    printf("\n======================================================================\n");
    printf("                       WATER JUG PROBLEM DEMONSTRATION                \n");
    printf("======================================================================\n");

    printf("\nProblem Setup:\n");
    printf("  - Jug 1 Capacity: 3 liters\n");
    printf("  - Jug 2 Capacity: 4 liters\n");
    printf("  - Goal: Get exactly 2 liters in Jug 2\n");
    printf("  - Initial State: Both jugs empty (0, 0)\n");

    int j1 = 3, j2 = 4, t1 = 0, t2 = 2;
    JugState init = {0, 0};

    // BFS
    printf("\n[1] Solving with Breadth First Search (BFS)...\n");
    JugNode* sol_bfs = solve_water_jug_bfs(j1, j2, t1, t2);
    if (sol_bfs) {
        print_water_jug_solution(sol_bfs, "BFS", j1, j2, init);
    } else {
        printf("No solution found using BFS\n");
    }

    // DFS
    printf("\n[2] Solving with Depth First Search (DFS)...\n");
    JugNode* sol_dfs = solve_water_jug_dfs(j1, j2, t1, t2);
    if (sol_dfs) {
        print_water_jug_solution(sol_dfs, "DFS", j1, j2, init);
    } else {
        printf("No solution found using DFS\n");
    }

    // Count Paths
    printf("\n[3] Counting all possible paths to goal state...\n");
    int count = count_all_paths_dfs(j1, j2, t1, t2);
    printf("Total number of different paths to reach goal state: %d\n", count);

    printf("\n\n============================================================\n");
    printf("Problem 2: 3L and 4L jugs, Goal: (2, 0)\n");
    printf("------------------------------------------------------------\n");
    JugNode* sol_bfs2 = solve_water_jug_bfs(3, 4, 2, 0);
    if (sol_bfs2) print_water_jug_solution(sol_bfs2, "BFS", 3, 4, init);
    else printf("No solution found\n");

    printf("\n\n============================================================\n");
    printf("Problem 3: 5L and 3L jugs, Goal: (4, 0)\n");
    printf("------------------------------------------------------------\n");
    JugNode* sol_bfs3 = solve_water_jug_bfs(5, 3, 4, 0);
    if (sol_bfs3) print_water_jug_solution(sol_bfs3, "BFS", 5, 3, init);
    else printf("No solution found\n");
}

void demo_eight_puzzle() {
    printf("\n======================================================================\n");
    printf("                       8-PUZZLE PROBLEM DEMONSTRATION                 \n");
    printf("======================================================================\n");

    int initial[3][3] = {{1, 2, 3}, {8, 0, 4}, {7, 6, 5}};
    int goal[3][3] = {{2, 8, 1}, {0, 4, 3}, {7, 6, 5}};

    printf("\nProblem Setup:\nInitial State:\n");
    for(int i=0; i<3; i++) {
        printf("    ");
        for(int j=0; j<3; j++) initial[i][j] == 0 ? printf("-") : printf("%d ", initial[i][j]);
        printf("\n");
    }
    printf("\nGoal State:\n");
    for(int i=0; i<3; i++) {
        printf("    ");
        for(int j=0; j<3; j++) goal[i][j] == 0 ? printf("-") : printf("%d ", goal[i][j]);
        printf("\n");
    }

    printf("\n----------------------------------------------------------------------\n");
    printf("Solving with A* using Misplaced Tiles Heuristic...\n");
    PuzzleState* sol1 = solve_eight_puzzle(initial, goal, "misplaced");
    int nodes1 = get_nodes_expanded();
    int moves1 = 0;
    if (sol1) {
        PuzzleState* temp = sol1;
        while (temp->parent) { moves1++; temp = temp->parent; }
        print_puzzle_solution(sol1, initial, goal, "misplaced tiles", nodes1);
    }

    printf("\n----------------------------------------------------------------------\n");
    printf("Solving with A* using Manhattan Distance Heuristic...\n");
    PuzzleState* sol2 = solve_eight_puzzle(initial, goal, "manhattan");
    int nodes2 = get_nodes_expanded();
    int moves2 = 0;
    if (sol2) {
        PuzzleState* temp = sol2;
        while (temp->parent) { moves2++; temp = temp->parent; }
        print_puzzle_solution(sol2, initial, goal, "manhattan distance", nodes2);
    }

    printf("\n======================================================================\n");
    printf("                         HEURISTIC COMPARISON                         \n");
    printf("======================================================================\n");
    printf("\n┌─────────────────────────┬──────────────┬──────────────────┐\n");
    printf("│ Heuristic               │ Moves        │ Nodes Expanded   │\n");
    printf("├─────────────────────────┼──────────────┼──────────────────┤\n");
    printf("│ Misplaced Tiles         │ %-12d │ %-16d │\n", moves1, nodes1);
    printf("│ Manhattan Distance      │ %-12d │ %-16d │\n", moves2, nodes2);
    printf("└─────────────────────────┴──────────────┴──────────────────┘\n");

    if (nodes1 > 0 && nodes2 > 0) {
        if (nodes2 < nodes1) {
             printf("\nManhattan Distance is more efficient!\nIt expanded %d fewer nodes.\n", nodes1 - nodes2);
        } else if (nodes1 < nodes2) {
             printf("\nMisplaced Tiles is more efficient!\nIt expanded %d fewer nodes.\n", nodes2 - nodes1);
        } else {
             printf("\nBoth heuristics expanded the same number of nodes.\n");
        }
    }
}

int main() {
    demo_water_jug();
    demo_eight_puzzle();
    return 0;
}
