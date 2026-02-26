#ifndef WATER_JUG_PROBLEM_H
#define WATER_JUG_PROBLEM_H

typedef struct {
    int jug1;
    int jug2;
} JugState;

typedef struct Node {
    JugState state;
    char action[50];
    struct Node* parent;
} JugNode;

JugNode* solve_water_jug_bfs(int cap1, int cap2, int target1, int target2);
JugNode* solve_water_jug_dfs(int cap1, int cap2, int target1, int target2);
int count_all_paths_dfs(int cap1, int cap2, int target1, int target2);
void print_water_jug_solution(JugNode* goal, const char* algo_name, int cap1, int cap2, JugState initial);

#endif