# Assignment-6: Q-Learning AGV Navigation

**Problem:** Navigation of an Autonomous Guided Vehicle (AGV) in a Smart Fulfillment Center using Reinforcement Learning.

## Overview

A Q-learning agent is trained to navigate a 6×6 warehouse grid from a charging station at **(0,0)** to a shipping dock at **(5,5)**, while avoiding hazard zones. The agent has no prior knowledge of the floor plan and learns entirely through trial-and-error exploration.

## Environment

| Property | Value |
|----------|-------|
| Grid size | 6 × 6 (36 states) |
| Start state | (0, 0) — top-left |
| Goal state | (5, 5) — bottom-right |
| Hazard cells | (2,2), (2,3), (3,2) |
| Actions | Up, Down, Left, Right |
| Wall behavior | Actions hitting boundaries keep the AGV in place |

## Reward Structure

| Event | Reward |
|-------|--------|
| Reaching goal (5,5) | **+100** (episode terminates) |
| Entering a hazard cell | **−50** (episode continues) |
| Any other step | **−1** (encourages shortest path) |

## Q-Learning Algorithm

The agent maintains a Q-table of shape **36 × 4** (states × actions), initialized to zero, and updates it using the Bellman equation:

```
Q(S, A) ← Q(S, A) + α × [R + γ × max_a Q(S', a) − Q(S, A)]
```

### Hyperparameters

| Parameter | Value |
|-----------|-------|
| Learning rate α | 0.1 |
| Discount factor γ | 0.9 |
| Epsilon start (ε) | 1.0 |
| Epsilon min | 0.01 |
| Epsilon decay | 0.995 per episode |
| Training episodes | 1000 |
| Max steps/episode | 200 |

The ε-greedy strategy starts with full exploration (ε = 1.0) and decays to near-full exploitation (ε ≈ 0.01) by ~episode 900.

## Files

```
Assignment-6/
├── agv_navigation.py           # Main Q-learning implementation
├── output.txt                  # Console log (Q-tables, path, stats)
├── q_learning_rewards.png      # Plot: Total Reward vs Episodes
├── q_learning_optimal_actions.png  # Plot: % Optimal Actions vs Episodes
├── optimal_path.png            # Grid visualization of learned policy & path
└── README.md                   # This file
```

## Running

```bash
uv run python Assignment-6/agv_navigation.py
```

## Outputs

### 1. Initial Q-Table
Printed before training — all values are 0.0 (as required).

### 2. Final Q-Table
After 1000 episodes, the Q-table shows learned action-values. State (5,4) correctly learns Q=+100 for the Down action (directly into the goal).

### 3. Policy Grid
A 6×6 ASCII grid showing the best action (↑↓←→) learned for each cell. Hazard cells are marked `HZ`, goal as `GOAL`.

### 4. Learning Curves
- **Plot 1** (`q_learning_optimal_actions.png`): % Greedy Actions vs Episodes — rises toward 100% as ε decays.
- **Plot 2** (`q_learning_rewards.png`): Total Reward vs Episodes — converges to ~+90 as the agent learns the optimal path.

### 5. Optimal Path
The trained agent follows a 10-step collision-free path around the hazard cluster, e.g.:
```
(0,0) → (1,0) → (2,0) → (3,0) → (4,0) → (4,1) → (4,2) → (5,2) → (5,3) → (5,4) → (5,5)
```
The path visualisation (`optimal_path.png`) shows the grid with color-coded cells and policy arrows.

## Code Structure

| Class / Function | Purpose |
|-----------------|---------|
| `WarehouseEnv` | Grid environment: state indexing, transitions, rewards |
| `QLearningAgent` | Q-table, ε-greedy selection, Bellman update |
| `train()` | Main training loop over episodes |
| `print_q_table()` | Formatted Q-table display |
| `print_best_actions_grid()` | ASCII policy grid |
| `get_optimal_path()` | Greedy path extraction post-training |
| `plot_reward_curve()` | Matplotlib reward convergence plot |
| `plot_optimal_action_curve()` | Matplotlib %-greedy-actions plot |
| `plot_optimal_path()` | Matplotlib grid + path + policy arrows |
