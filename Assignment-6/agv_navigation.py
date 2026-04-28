import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import random
import os

GRID_SIZE = 6
START     = (0, 0)
GOAL      = (5, 5)
HAZARDS   = {(2, 2), (2, 3), (3, 2)}

ACTIONS     = ['Up', 'Down', 'Left', 'Right']
NUM_ACTIONS = len(ACTIONS)
NUM_STATES  = GRID_SIZE * GRID_SIZE

ACTION_DELTA = {
    0: ( 0, -1),
    1: ( 0,  1),
    2: (-1,  0),
    3: ( 1,  0),
}

REWARD_GOAL   =  100
REWARD_HAZARD =  -50
REWARD_STEP   =   -1

ALPHA     = 0.1
GAMMA     = 0.9
EPS_START = 1.0
EPS_MIN   = 0.01
EPS_DECAY = 0.995

EPISODES  = 1000
MAX_STEPS = 200

OUT_DIR = os.path.dirname(os.path.abspath(__file__))


class WarehouseEnv:
    """
    6×6 deterministic grid-world environment.

    Coordinate convention: (x, y) where x is the column and y is the row.
    (0,0) is top-left; (5,5) is bottom-right.
    State index = y * GRID_SIZE + x   (row-major, 0 … 35)
    """

    @staticmethod
    def state_to_idx(x: int, y: int) -> int:
        return y * GRID_SIZE + x

    @staticmethod
    def idx_to_state(idx: int):
        return (idx % GRID_SIZE, idx // GRID_SIZE)

    def reset(self) -> int:
        return self.state_to_idx(*START)

    def step(self, state_idx: int, action: int):
        x, y = self.idx_to_state(state_idx)
        dx, dy = ACTION_DELTA[action]

        nx = max(0, min(GRID_SIZE - 1, x + dx))
        ny = max(0, min(GRID_SIZE - 1, y + dy))
        next_state = (nx, ny)
        next_state_idx = self.state_to_idx(nx, ny)

        if next_state == GOAL:
            return next_state_idx, REWARD_GOAL, True
        elif next_state in HAZARDS:
            return next_state_idx, REWARD_HAZARD, False
        else:
            return next_state_idx, REWARD_STEP, False


class QLearningAgent:
    """
    Tabular Q-learning agent with ε-greedy exploration.

    Maintains a Q-table of shape (NUM_STATES, NUM_ACTIONS) = (36, 4),
    initialised to all zeros as required by the assignment spec.
    """

    def __init__(self):
        self.q_table = np.zeros((NUM_STATES, NUM_ACTIONS), dtype=float)

    def choose_action(self, state_idx: int, epsilon: float) -> int:
        if random.random() < epsilon:
            return random.randint(0, NUM_ACTIONS - 1)
        return self.greedy_action(state_idx)

    def greedy_action(self, state_idx: int) -> int:
        return int(np.argmax(self.q_table[state_idx]))

    def update(self, s: int, a: int, r: float, s_next: int, done: bool):
        future_value = 0.0 if done else GAMMA * np.max(self.q_table[s_next])
        td_error = r + future_value - self.q_table[s, a]
        self.q_table[s, a] += ALPHA * td_error


def train(agent: QLearningAgent, env: WarehouseEnv, episodes: int):
    reward_history     = []
    opt_action_history = []

    for ep in range(episodes):
        epsilon = max(EPS_MIN, EPS_START * (EPS_DECAY ** ep))

        state = env.reset()
        total_reward = 0.0
        greedy_count = 0
        step_count   = 0

        for _ in range(MAX_STEPS):
            is_greedy = (random.random() >= epsilon)
            if is_greedy:
                action = agent.greedy_action(state)
                greedy_count += 1
            else:
                action = random.randint(0, NUM_ACTIONS - 1)

            next_state, reward, done = env.step(state, action)
            agent.update(state, action, reward, next_state, done)

            state         = next_state
            total_reward += reward
            step_count   += 1

            if done:
                break

        reward_history.append(total_reward)
        pct_greedy = (greedy_count / step_count * 100) if step_count > 0 else 0.0
        opt_action_history.append(pct_greedy)

    return reward_history, opt_action_history


def print_q_table(q_table: np.ndarray, title: str, log: list):
    def tee(line=""):
        log.append(line)

    tee(f"\n{'='*72}")
    tee(f"  {title}")
    tee(f"{'='*72}")
    header = f"{'State':>8}  {'Up':>9}  {'Down':>9}  {'Left':>9}  {'Right':>9}  {'Best':>6}"
    tee(header)
    tee("-" * 72)

    for idx in range(NUM_STATES):
        x, y = WarehouseEnv.idx_to_state(idx)
        vals = q_table[idx]
        best = ACTIONS[int(np.argmax(vals))]
        row = (
            f"  ({x},{y}) [{idx:2d}]  "
            f"{vals[0]:+9.4f}  {vals[1]:+9.4f}  "
            f"{vals[2]:+9.4f}  {vals[3]:+9.4f}  {best:>6}"
        )
        tee(row)
    tee("=" * 72)


def print_best_actions_grid(q_table: np.ndarray, log: list):
    arrow = {0: ' ↑ ', 1: ' ↓ ', 2: ' ← ', 3: ' → '}

    def tee(line=""):
        log.append(line)

    tee("\n  Best Action per Cell (Policy Grid):")
    tee("  " + "+------" * GRID_SIZE + "+")

    for y in range(GRID_SIZE):
        row_str = "  |"
        for x in range(GRID_SIZE):
            if (x, y) == GOAL:
                cell = " GOAL "
            elif (x, y) in HAZARDS:
                cell = "  HZ  "
            elif (x, y) == START:
                cell = f"[{arrow[int(np.argmax(q_table[WarehouseEnv.state_to_idx(x,y)]))]}]"
            else:
                cell = f" {arrow[int(np.argmax(q_table[WarehouseEnv.state_to_idx(x,y)]))]} "
            row_str += cell + "|"
        tee(row_str)
        tee("  " + "+------" * GRID_SIZE + "+")


def get_optimal_path(agent: QLearningAgent, env: WarehouseEnv):
    state = env.reset()
    path  = [WarehouseEnv.idx_to_state(state)]

    for _ in range(50):
        action = agent.greedy_action(state)
        next_state, _, done = env.step(state, action)
        x, y = WarehouseEnv.idx_to_state(next_state)
        path.append((x, y))
        state = next_state
        if done:
            break

    return path


def print_path_ascii(path: list, log: list):
    def tee(line=""):
        log.append(line)

    path_set = set(path)
    symbol = {START: 'S', GOAL: 'G'}
    for hz in HAZARDS:
        symbol[hz] = 'X'

    tee("\n  Optimal Path on Warehouse Grid:")
    tee("     " + "  ".join(str(x) for x in range(GRID_SIZE)))
    tee("    " + "---" * GRID_SIZE)

    for y in range(GRID_SIZE):
        row_str = f"  {y} |"
        for x in range(GRID_SIZE):
            cell = (x, y)
            if cell in symbol:
                ch = symbol[cell]
            elif cell in path_set:
                ch = '*'
            else:
                ch = '.'
            row_str += f" {ch} "
        tee(row_str)

    tee("\n  Legend:  S=Start  G=Goal  X=Hazard  *=Path  .=Free")
    step_list = " → ".join(f"({x},{y})" for x, y in path)
    tee(f"\n  Path ({len(path)-1} steps):\n  {step_list}")


def _smooth(data: list, window: int = 50) -> np.ndarray:
    kernel = np.ones(window) / window
    return np.convolve(data, kernel, mode='valid')


def plot_reward_curve(reward_history: list):
    fig, ax = plt.subplots(figsize=(10, 5))

    episodes = np.arange(1, len(reward_history) + 1)
    ax.plot(episodes, reward_history, alpha=0.3, color='steelblue', linewidth=0.8, label='Episode Reward')

    smoothed = _smooth(reward_history, window=50)
    smooth_x = np.arange(50, len(reward_history) + 1)
    ax.plot(smooth_x, smoothed, color='navy', linewidth=2.0, label='50-ep Moving Average')

    ax.axhline(0, color='gray', linestyle='--', linewidth=0.8)
    ax.set_xlabel("Episode", fontsize=12)
    ax.set_ylabel("Total Reward", fontsize=12)
    ax.set_title("Q-Learning — Average Reward vs. Episodes", fontsize=14, fontweight='bold')
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3)
    fig.tight_layout()

    path = os.path.join(OUT_DIR, "q_learning_rewards.png")
    fig.savefig(path, dpi=150)
    print(f"  [Saved] {path}")
    plt.close(fig)


def plot_optimal_action_curve(opt_action_history: list):
    fig, ax = plt.subplots(figsize=(10, 5))

    episodes = np.arange(1, len(opt_action_history) + 1)
    ax.plot(episodes, opt_action_history, alpha=0.3, color='darkorange', linewidth=0.8,
            label='% Greedy Actions per Episode')

    smoothed = _smooth(opt_action_history, window=50)
    smooth_x = np.arange(50, len(opt_action_history) + 1)
    ax.plot(smooth_x, smoothed, color='saddlebrown', linewidth=2.0, label='50-ep Moving Average')

    ax.set_ylim(0, 105)
    ax.set_xlabel("Episode", fontsize=12)
    ax.set_ylabel("% Greedy (Optimal) Actions", fontsize=12)
    ax.set_title("Q-Learning — % Optimal Actions vs. Episodes", fontsize=14, fontweight='bold')
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3)
    fig.tight_layout()

    path = os.path.join(OUT_DIR, "q_learning_optimal_actions.png")
    fig.savefig(path, dpi=150)
    print(f"  [Saved] {path}")
    plt.close(fig)


def plot_optimal_path(path: list, q_table: np.ndarray):
    fig, ax = plt.subplots(figsize=(8, 8))

    grid_colors = np.ones((GRID_SIZE, GRID_SIZE, 3))

    for hz in HAZARDS:
        grid_colors[hz[1], hz[0]] = [0.95, 0.3, 0.3]

    sx, sy = START
    gx, gy = GOAL
    grid_colors[sy, sx] = [0.2, 0.5, 0.9]
    grid_colors[gy, gx] = [0.2, 0.8, 0.3]

    path_set = set(path)
    for (px, py) in path:
        if (px, py) not in {START, GOAL} and (px, py) not in HAZARDS:
            grid_colors[py, px] = [1.0, 0.98, 0.6]

    ax.imshow(grid_colors, origin='upper', extent=[0, GRID_SIZE, GRID_SIZE, 0])

    for i in range(GRID_SIZE + 1):
        ax.axhline(i, color='gray', linewidth=0.8)
        ax.axvline(i, color='gray', linewidth=0.8)

    dx_map = {0:  0,    1:  0,    2: -0.3, 3:  0.3}
    dy_map = {0: -0.3,  1:  0.3,  2:  0,   3:  0  }
    for idx in range(NUM_STATES):
        x, y = WarehouseEnv.idx_to_state(idx)
        if (x, y) == GOAL or (x, y) in HAZARDS:
            continue
        best_a = int(np.argmax(q_table[idx]))
        cx, cy = x + 0.5, y + 0.5
        ax.annotate(
            "", xy=(cx + dx_map[best_a], cy + dy_map[best_a]),
            xytext=(cx - dx_map[best_a] * 0.5, cy - dy_map[best_a] * 0.5),
            arrowprops=dict(arrowstyle="-|>", color="dimgray", lw=1.2),
        )

    if len(path) > 1:
        px_coords = [p[0] + 0.5 for p in path]
        py_coords = [p[1] + 0.5 for p in path]
        ax.plot(px_coords, py_coords, 'k-o', linewidth=2.5, markersize=7,
                zorder=5, label='Optimal Path')

    for idx in range(NUM_STATES):
        x, y = WarehouseEnv.idx_to_state(idx)
        if (x, y) == START:
            ax.text(x + 0.5, y + 0.5, "START\n(0,0)", ha='center', va='center',
                    fontsize=7, fontweight='bold', color='white')
        elif (x, y) == GOAL:
            ax.text(x + 0.5, y + 0.5, "GOAL\n(5,5)", ha='center', va='center',
                    fontsize=7, fontweight='bold', color='white')
        elif (x, y) in HAZARDS:
            ax.text(x + 0.5, y + 0.5, f"HZ\n({x},{y})", ha='center', va='center',
                    fontsize=7, color='white')
        else:
            ax.text(x + 0.5, y + 0.85, f"({x},{y})", ha='center', va='center',
                    fontsize=6, color='#444444')

    ax.set_xlim(0, GRID_SIZE)
    ax.set_ylim(GRID_SIZE, 0)
    ax.set_xticks(np.arange(0.5, GRID_SIZE, 1))
    ax.set_xticklabels(range(GRID_SIZE))
    ax.set_yticks(np.arange(0.5, GRID_SIZE, 1))
    ax.set_yticklabels(range(GRID_SIZE))
    ax.set_xlabel("Column (x)", fontsize=12)
    ax.set_ylabel("Row (y)", fontsize=12)
    ax.set_title("Q-Learning AGV — Optimal Path & Learned Policy", fontsize=13, fontweight='bold')

    legend_handles = [
        mpatches.Patch(color=[0.2, 0.5, 0.9], label='Start (0,0)'),
        mpatches.Patch(color=[0.2, 0.8, 0.3], label='Goal (5,5)'),
        mpatches.Patch(color=[0.95, 0.3, 0.3], label='Hazard Zone'),
        mpatches.Patch(color=[1.0, 0.98, 0.6], label='Optimal Path'),
    ]
    ax.legend(handles=legend_handles, loc='upper right', fontsize=9,
              framealpha=0.85, edgecolor='gray')

    fig.tight_layout()
    path_out = os.path.join(OUT_DIR, "optimal_path.png")
    fig.savefig(path_out, dpi=150)
    print(f"  [Saved] {path_out}")
    plt.close(fig)


def main():
    log = []

    def tee(*args):
        line = " ".join(str(a) for a in args)
        print(line)
        log.append(line)

    tee("=" * 72)
    tee("  Assignment-6: Q-Learning AGV Navigation — Smart Fulfillment Center")
    tee("=" * 72)
    tee(f"  Grid          : {GRID_SIZE}×{GRID_SIZE}  ({NUM_STATES} states)")
    tee(f"  Start         : {START}")
    tee(f"  Goal          : {GOAL}  (reward = +{REWARD_GOAL})")
    tee(f"  Hazards       : {sorted(HAZARDS)}  (reward = {REWARD_HAZARD} each)")
    tee(f"  Step reward   : {REWARD_STEP}")
    tee(f"  α (lr)        : {ALPHA}    γ (discount): {GAMMA}")
    tee(f"  ε start/min   : {EPS_START} / {EPS_MIN}    decay: {EPS_DECAY}/episode")
    tee(f"  Episodes      : {EPISODES}   Max steps/ep: {MAX_STEPS}")

    env   = WarehouseEnv()
    agent = QLearningAgent()

    print_q_table(agent.q_table, "INITIAL Q-TABLE (Episode 0) — All Zeros", log)

    tee("\n  Training …")
    reward_history, opt_action_history = train(agent, env, EPISODES)
    tee(f"  Training complete.")
    tee(f"  Final ε       : {max(EPS_MIN, EPS_START * EPS_DECAY**(EPISODES-1)):.4f}")
    tee(f"  Last-100 avg reward : {np.mean(reward_history[-100:]):.2f}")
    tee(f"  Last-100 avg optimal: {np.mean(opt_action_history[-100:]):.1f}%")

    print_q_table(agent.q_table, "FINAL Q-TABLE (After Training)", log)

    log_line_tmp = []
    print_best_actions_grid(agent.q_table, log_line_tmp)
    for l in log_line_tmp:
        tee(l)

    optimal_path = get_optimal_path(agent, env)
    log_path_tmp = []
    print_path_ascii(optimal_path, log_path_tmp)
    for l in log_path_tmp:
        tee(l)

    tee("\n  Generating plots …")
    plot_reward_curve(reward_history)
    plot_optimal_action_curve(opt_action_history)
    plot_optimal_path(optimal_path, agent.q_table)

    out_path = os.path.join(OUT_DIR, "output.txt")
    with open(out_path, "w") as f:
        f.write("\n".join(log))
    print(f"\n  [Saved] {out_path}")
    print("=" * 72)


if __name__ == "__main__":
    main()
