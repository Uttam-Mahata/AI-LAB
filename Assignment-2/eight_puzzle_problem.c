#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <stdbool.h>
#include "eight_puzzle_problem.h"

#define HASH_SIZE 10007
#define MAX_OPEN_SET 200000

static int g_nodes_expanded = 0;

int get_nodes_expanded() {
    return g_nodes_expanded;
}

typedef struct HashEntry {
    unsigned long long key;
    PuzzleState* state;
    struct HashEntry* next;
} HashEntry;

HashEntry* visited_table[HASH_SIZE];

unsigned long long compute_hash(int board[3][3]) {
    unsigned long long h = 0;
    for (int i = 0; i < 3; i++) {
        for (int j = 0; j < 3; j++) {
            h = (h << 4) | (board[i][j] & 0xF);
        }
    }
    return h;
}

void init_hash_table() {
    for (int i = 0; i < HASH_SIZE; i++) visited_table[i] = NULL;
}

void add_to_closed(PuzzleState* state) {
    unsigned long long key = compute_hash(state->board);
    int idx = key % HASH_SIZE;
    HashEntry* entry = (HashEntry*)malloc(sizeof(HashEntry));
    entry->key = key;
    entry->state = state;
    entry->next = visited_table[idx];
    visited_table[idx] = entry;
}

bool is_in_closed(int board[3][3]) {
    unsigned long long key = compute_hash(board);
    int idx = key % HASH_SIZE;
    HashEntry* curr = visited_table[idx];
    while (curr) {
        if (curr->key == key) return true; 
        curr = curr->next;
    }
    return false;
}

void free_hash_table() {
    for (int i = 0; i < HASH_SIZE; i++) {
        HashEntry* curr = visited_table[i];
        while (curr) {
            HashEntry* temp = curr;
            curr = curr->next;
           
            free(temp);
        }
        visited_table[i] = NULL;
    }
}

PuzzleState* open_set[MAX_OPEN_SET];
int open_set_size = 0;

void push_heap(PuzzleState* state) {
    int i = open_set_size++;
    while (i > 0) {
        int p = (i - 1) / 2;
        if (open_set[p]->f_cost <= state->f_cost) break;
        open_set[i] = open_set[p];
        i = p;
    }
    open_set[i] = state;
}

PuzzleState* pop_heap() {
    if (open_set_size == 0) return NULL;
    PuzzleState* ret = open_set[0];
    PuzzleState* last = open_set[--open_set_size];
    int i = 0;
    while (i * 2 + 1 < open_set_size) {
        int left = i * 2 + 1;
        int right = i * 2 + 2;
        int min = left;
        if (right < open_set_size && open_set[right]->f_cost < open_set[left]->f_cost) {
            min = right;
        }
        if (last->f_cost <= open_set[min]->f_cost) break;
        open_set[i] = open_set[min];
        i = min;
    }
    open_set[i] = last;
    return ret;
}

int heuristic_misplaced(int board[3][3], int goal[3][3]) {
    int count = 0;
    for (int i = 0; i < 3; i++)
        for (int j = 0; j < 3; j++)
            if (board[i][j] != 0 && board[i][j] != goal[i][j])
                count++;
    return count;
}

int heuristic_manhattan(int board[3][3], int goal[3][3]) {
    int dist = 0;
    for (int r = 0; r < 3; r++) {
        for (int c = 0; c < 3; c++) {
            int val = board[r][c];
            if (val != 0) {
                for (int gr = 0; gr < 3; gr++) {
                    for (int gc = 0; gc < 3; gc++) {
                        if (goal[gr][gc] == val) {
                            dist += abs(r - gr) + abs(c - gc);
                        }
                    }
                }
            }
        }
    }
    return dist;
}

PuzzleState* create_puzzle_state(int board[3][3], int g, int h, PuzzleState* parent, const char* move) {
    PuzzleState* s = (PuzzleState*)malloc(sizeof(PuzzleState));
    memcpy(s->board, board, 9 * sizeof(int));
    s->g_cost = g;
    s->h_cost = h;
    s->f_cost = g + h;
    s->parent = parent;
    strcpy(s->move, move);
    return s;
}

void find_empty(int board[3][3], int* r, int* c) {
    for (int i = 0; i < 3; i++)
        for (int j = 0; j < 3; j++)
            if (board[i][j] == 0) {
                *r = i; *c = j;
                return;
            }
}

int are_boards_equal(int b1[3][3], int b2[3][3]) {
    for (int i=0; i<3; i++)
        for (int j=0; j<3; j++)
            if (b1[i][j] != b2[i][j]) return 0;
    return 1;
}

PuzzleState* solve_eight_puzzle(int start[3][3], int goal[3][3], const char* heuristic_type) {
    g_nodes_expanded = 0;
    init_hash_table();
    open_set_size = 0;

    int (*h_func)(int[3][3], int[3][3]) = (strcmp(heuristic_type, "misplaced") == 0) ? heuristic_misplaced : heuristic_manhattan;

    PuzzleState* root = create_puzzle_state(start, 0, h_func(start, goal), NULL, "Initial");
    push_heap(root);

    while (open_set_size > 0) {
        PuzzleState* current = pop_heap();

        if (is_in_closed(current->board)) {
            // Already visited this state with lower or equal cost? 
            // A* check: if in closed set, we generally skip unless we found a shorter path. 
            // Simple implementation: just skip.
            // Note: In strict A*, if we find a better path to a node in closed, we re-open. 
            // With consistent heuristic (Monotone), first visit is optimal. Manhattan is consistent.
            continue;
        }

        if (are_boards_equal(current->board, goal)) {
            // Keep hash table for pointers (parents), but maybe clear later?
            // User script will finish and exit.
            return current;
        }

        add_to_closed(current);
        g_nodes_expanded++;

        int r, c;
        find_empty(current->board, &r, &c);

        int dr[] = {-1, 1, 0, 0};
        int dc[] = {0, 0, -1, 1};
        char* moves[] = {"Up", "Down", "Left", "Right"};

        for (int i = 0; i < 4; i++) {
            int nr = r + dr[i];
            int nc = c + dc[i];

            if (nr >= 0 && nr < 3 && nc >= 0 && nc < 3) {
                int new_board[3][3];
                memcpy(new_board, current->board, 9 * sizeof(int));
                new_board[r][c] = new_board[nr][nc];
                new_board[nr][nc] = 0;

                if (!is_in_closed(new_board)) {
                    int new_g = current->g_cost + 1;
                    PuzzleState* neighbor = create_puzzle_state(new_board, new_g, h_func(new_board, goal), current, moves[i]);
                    push_heap(neighbor);
                }
            }
        }
    }
    
    return NULL;
}

void print_board(int board[3][3]) {
    for (int i=0; i<3; i++) {
        for (int j=0; j<3; j++) {
            if (board[i][j] == 0) printf("- ");
            else printf("%d ", board[i][j]);
        }
        printf("\n");
    }
}

void print_puzzle_solution(PuzzleState* goal, int start[3][3], int goal_board[3][3], const char* heuristic, int nodes_expanded) {
    printf("\n============================================================\n");
    printf("Solution using A* with %s Heuristic\n", heuristic);
    printf("============================================================\n");
    printf("Initial State:\n");
    print_board(start);
    printf("\nGoal State:\n");
    print_board(goal_board);
    
    if (!goal) {
        printf("No solution found.\n");
        return;
    }

    PuzzleState* path[1000];
    int len = 0;
    PuzzleState* curr = goal;
    while(curr) {
        path[len++] = curr;
        curr = curr->parent;
    }

    printf("\nNumber of moves: %d\n", len - 1);
    printf("Nodes expanded: %d\n", nodes_expanded);
    printf("\nSolution Steps:\n");
    printf("------------------------------------------------------------\n");

    for (int i = len - 1; i >= 0; i--) {
        printf("\nStep %d: %s\n", len - 1 - i, path[i]->move);
        printf("g=%d, h=%d, f=%d\n", path[i]->g_cost, path[i]->h_cost, path[i]->f_cost);
        print_board(path[i]->board);
    }
    printf("\n============================================================\n");
}
