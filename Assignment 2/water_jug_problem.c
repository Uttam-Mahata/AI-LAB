#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include "water_jug_problem.h"

#define MAX_CAP 100

JugNode* create_node(int j1, int j2, const char* action, JugNode* parent) {
    JugNode* node = (JugNode*)malloc(sizeof(JugNode));
    node->state.jug1 = j1;
    node->state.jug2 = j2;
    strncpy(node->action, action, 49);
    node->action[49] = '\0';
    node->parent = parent;
    return node;
}

bool is_goal(JugState state, int t1, int t2) {
   
    return state.jug1 == t1 && state.jug2 == t2;
}

JugNode* solve_water_jug_bfs(int cap1, int cap2, int target1, int target2) {
    bool visited[MAX_CAP][MAX_CAP];
    memset(visited, 0, sizeof(visited));

    JugNode* queue[10000];
    int front = 0, rear = 0;

    JugNode* start = create_node(0, 0, "Initial State", NULL);
    queue[rear++] = start;
    visited[0][0] = true;

    while (front < rear) {
        JugNode* current = queue[front++];
        int j1 = current->state.jug1;
        int j2 = current->state.jug2;

        if (is_goal(current->state, target1, target2)) {
            return current;
        }

        if (j1 < cap1) {
            if (!visited[cap1][j2]) {
                visited[cap1][j2] = true;
                queue[rear++] = create_node(cap1, j2, "Fill Jug1", current);
            }
        }
        if (j2 < cap2) {
            if (!visited[j1][cap2]) {
                visited[j1][cap2] = true;
                queue[rear++] = create_node(j1, cap2, "Fill Jug2", current);
            }
        }
        if (j1 > 0) {
            if (!visited[0][j2]) {
                visited[0][j2] = true;
                queue[rear++] = create_node(0, j2, "Empty Jug1", current);
            }
        }
        if (j2 > 0) {
            if (!visited[j1][0]) {
                visited[j1][0] = true;
                queue[rear++] = create_node(j1, 0, "Empty Jug2", current);
            }
        }
        if (j1 > 0 && j2 < cap2) {
            int amount = (j1 < (cap2 - j2)) ? j1 : (cap2 - j2);
            int nj1 = j1 - amount;
            int nj2 = j2 + amount;
            if (!visited[nj1][nj2]) {
                visited[nj1][nj2] = true;
                queue[rear++] = create_node(nj1, nj2, "Pour Jug1->Jug2", current);
            }
        }
        if (j2 > 0 && j1 < cap1) {
            int amount = (j2 < (cap1 - j1)) ? j2 : (cap1 - j1);
            int nj1 = j1 + amount;
            int nj2 = j2 - amount;
            if (!visited[nj1][nj2]) {
                visited[nj1][nj2] = true;
                queue[rear++] = create_node(nj1, nj2, "Pour Jug2->Jug1", current);
            }
        }
    }
    return NULL;
}

JugNode* solve_water_jug_dfs(int cap1, int cap2, int target1, int target2) {
    JugNode* stack[10000];
    int top = 0;

    bool visited[MAX_CAP][MAX_CAP];
    memset(visited, 0, sizeof(visited));

    JugNode* start = create_node(0, 0, "Initial State", NULL);
    stack[top++] = start;
    
  
    
    while (top > 0) {
        JugNode* current = stack[--top];
        int j1 = current->state.jug1;
        int j2 = current->state.jug2;

        if (visited[j1][j2]) {
            continue; 
        }
        visited[j1][j2] = true;

        if (is_goal(current->state, target1, target2)) {
            return current;
        }

        
        int next_states[6][2];
        char actions[6][50];
        int count = 0;


        next_states[count][0] = cap1; next_states[count][1] = j2; strcpy(actions[count++], "Fill Jug1");
        next_states[count][0] = j1; next_states[count][1] = cap2; strcpy(actions[count++], "Fill Jug2");
        next_states[count][0] = 0; next_states[count][1] = j2; strcpy(actions[count++], "Empty Jug1");
        next_states[count][0] = j1; next_states[count][1] = 0; strcpy(actions[count++], "Empty Jug2");
        {
            int amt = (j1 < (cap2 - j2)) ? j1 : (cap2 - j2);
            next_states[count][0] = j1 - amt; next_states[count][1] = j2 + amt; strcpy(actions[count++], "Pour Jug1->Jug2");
        }
        {
            int amt = (j2 < (cap1 - j1)) ? j2 : (cap1 - j1);
            next_states[count][0] = j1 + amt; next_states[count][1] = j2 - amt; strcpy(actions[count++], "Pour Jug2->Jug1");
        }

        for (int i = 0; i < count; i++) {
            int nj1 = next_states[i][0];
            int nj2 = next_states[i][1];
            if (nj1 >= 0 && nj1 <= cap1 && nj2 >= 0 && nj2 <= cap2) {
                if (!visited[nj1][nj2]) {
                    stack[top++] = create_node(nj1, nj2, actions[i], current);
                }
            }
        }
    }
    return NULL;
}

void dfs_count(int j1, int j2, int cap1, int cap2, int t1, int t2, 
               bool path_visited[MAX_CAP][MAX_CAP], int depth, int max_depth, int* count) {
    
    if (j1 == t1 && j2 == t2) {
        (*count)++;
        return;
    }

    if (depth >= max_depth) return;

    path_visited[j1][j2] = true;

    int next_states[6][2];
    int c = 0;
    next_states[c][0] = cap1; next_states[c++][1] = j2;
    next_states[c][0] = j1; next_states[c++][1] = cap2;
  
    next_states[c][0] = 0; next_states[c++][1] = j2;
  
    next_states[c][0] = j1; next_states[c++][1] = 0;
 
    {
        int amt = (j1 < (cap2 - j2)) ? j1 : (cap2 - j2);
        next_states[c][0] = j1 - amt; next_states[c++][1] = j2 + amt;
    }

    {
        int amt = (j2 < (cap1 - j1)) ? j2 : (cap1 - j1);
        next_states[c][0] = j1 + amt; next_states[c++][1] = j2 - amt;
    }

    for (int i = 0; i < c; i++) {
        int nj1 = next_states[i][0];
        int nj2 = next_states[i][1];
        if (nj1 >= 0 && nj1 <= cap1 && nj2 >= 0 && nj2 <= cap2) {
            if (!path_visited[nj1][nj2]) {
                dfs_count(nj1, nj2, cap1, cap2, t1, t2, path_visited, depth + 1, max_depth, count);
            }
        }
    }

    path_visited[j1][j2] = false; 
}

int count_all_paths_dfs(int cap1, int cap2, int target1, int target2) {
    bool path_visited[MAX_CAP][MAX_CAP];
    memset(path_visited, 0, sizeof(path_visited));
    int count = 0;
    dfs_count(0, 0, cap1, cap2, target1, target2, path_visited, 0, 20, &count);
    return count;
}

void print_water_jug_solution(JugNode* goal, const char* algo_name, int cap1, int cap2, JugState initial) {
    if (!goal) return;

    // Reconstruct path
    JugNode* path[100]; // Max path
    int len = 0;
    JugNode* curr = goal;
    while (curr != NULL) {
        path[len++] = curr;
        curr = curr->parent;
    }

    // Print
    printf("\n============================================================\n");
    printf("Solution using %s\n", algo_name);
    printf("============================================================\n");
    printf("Initial State: (%d, %d)\n", initial.jug1, initial.jug2);
    printf("Goal State: (%d, %d)\n", goal->state.jug1, goal->state.jug2);
    printf("Jug Capacities: Jug1=%dL, Jug2=%dL\n", cap1, cap2);
    printf("\nSteps to reach goal:\n");
    printf("%-6s %-20s %-8s %-8s\n", "Step", "Action", "Jug1", "Jug2");
    printf("------------------------------------------------------------\n");

    // Python style:
    // Step 0: Initial State, Initial State
    // Step i: Action i, State i-1
    // Final Step: "Goal Reached", Goal State
    
    printf("%-6d %-20s %-8d %-8d\n", 0, "Initial State", initial.jug1, initial.jug2);
    
    for (int i = len - 1; i > 0; i--) {
        int step = len - i;
        // Print current node's action and its parent's state
        printf("%-6d %-20s %-8d %-8d\n", step, path[i-1]->action, path[i]->state.jug1, path[i]->state.jug2);
    }
    
    // Final goal reached step
    printf("%-6d %-20s %-8d %-8d\n", len, "Goal Reached", goal->state.jug1, goal->state.jug2);

    printf("\nTotal steps: %d\n", len);
}
