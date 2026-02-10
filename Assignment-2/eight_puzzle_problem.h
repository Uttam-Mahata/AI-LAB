#ifndef EIGHT_PUZZLE_PROBLEM_H
#define EIGHT_PUZZLE_PROBLEM_H

typedef struct PuzzleState {
    int board[3][3];
    int g_cost;
    int h_cost;
    int f_cost;
    struct PuzzleState* parent;
    char move[20];
} PuzzleState;

PuzzleState* solve_eight_puzzle(int start[3][3], int goal[3][3], const char* heuristic_type);
void print_puzzle_solution(PuzzleState* goal, int start[3][3], int goal_board[3][3], const char* heuristic, int nodes_expanded);
int get_nodes_expanded(); 

#endif
