import heapq
import math
import json
import sys
import argparse
import os
import itertools


OBSTACLE = '1'
FIRE     = 'F'

# 6-directional offsets: (dx, dy, dz, direction_label)
DIRECTIONS = [
    (-1,  0,  0, 'North'),
    ( 1,  0,  0, 'South'),
    ( 0,  1,  0, 'East'),
    ( 0, -1,  0, 'West'),
    ( 0,  0,  1, 'Up'),
    ( 0,  0, -1, 'Down'),
]

LEVEL_NAMES = {0: 'Ground Level', 1: 'Mid Level', 2: 'Sky Level'}


class CityGrid:

    def __init__(self, data):
        dims = data['dimensions']
        self.rows   = dims['rows']
        self.cols   = dims['cols']
        self.levels = dims['levels']
        self.grid   = data['grid']                    # [z][x][y]
        self.default_energy   = data.get('initial_energy',   100)
        self.default_penalty  = data.get('recharge_penalty',   5)

        self.start             = None
        self.base              = None
        self.goals             = {}    # 'G1' → (x,y,z)
        self.recharge_stations = []

        for z in range(self.levels):
            for x in range(self.rows):
                for y in range(self.cols):
                    cell = self.grid[z][x][y]
                    if cell == 'S':
                        self.start = (x, y, z)
                    elif cell == 'B':
                        self.base = (x, y, z)
                    elif cell == 'R':
                        self.recharge_stations.append((x, y, z))
                    elif len(cell) >= 2 and cell[0] == 'G' and cell[1:].isdigit():
                        self.goals[cell] = (x, y, z)


    def get_cell(self, x, y, z):
        if 0 <= x < self.rows and 0 <= y < self.cols and 0 <= z < self.levels:
            return self.grid[z][x][y]
        return None

    @staticmethod
    def terrain_cost(cell):
        return 3.0 if cell == FIRE else 1.0

    @staticmethod
    def is_passable(cell):
        return cell is not None and cell != OBSTACLE

    def move_cost(self, dest_cell, dz):

        if dz > 0:
            return self.terrain_cost(dest_cell) + 2.0
        if dz < 0:
            return 1.0
        return self.terrain_cost(dest_cell)

    def get_neighbors(self, pos):

        x, y, z = pos
        result = []
        for dx, dy, dz, _ in DIRECTIONS:
            nx, ny, nz = x + dx, y + dy, z + dz
            cell = self.get_cell(nx, ny, nz)
            if self.is_passable(cell):
                result.append(((nx, ny, nz), self.move_cost(cell, dz)))
        return result



_TIE_COUNTER = itertools.count()   # unique int per push → avoids tuple comparisons


def heuristic(a, b):
    return math.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2 + (a[2]-b[2])**2)


def astar_3d(city_grid, start, goal):

    if start == goal:
        return [start], 0.0

    open_set = []
    heapq.heappush(open_set, (heuristic(start, goal), 0.0, next(_TIE_COUNTER), start))

    came_from = {}
    g_score   = {start: 0.0}

    while open_set:
        f_val, g_val, _, current = heapq.heappop(open_set)

        if current == goal:
            return _reconstruct_path(came_from, current), g_score[goal]

        if g_val > g_score.get(current, float('inf')):
            continue

        for neighbor, cost in city_grid.get_neighbors(current):
            tentative_g = g_score[current] + cost
            if tentative_g < g_score.get(neighbor, float('inf')):
                came_from[neighbor] = current
                g_score[neighbor]   = tentative_g
                f_new = tentative_g + heuristic(neighbor, goal)
                heapq.heappush(open_set, (f_new, tentative_g, next(_TIE_COUNTER), neighbor))

    return None, float('inf')


def _reconstruct_path(came_from, current):
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)
    return path[::-1]


def _greedy_goal_order(start, goals_dict):

    remaining = dict(goals_dict)
    ordered, current = [], start
    while remaining:
        nearest_label, nearest_pos = min(
            remaining.items(), key=lambda kv: heuristic(current, kv[1])
        )
        ordered.append((nearest_label, nearest_pos))
        current = nearest_pos
        del remaining[nearest_label]
    return ordered


def _find_nearest_recharge(city_grid, current_pos):

    best_pos, best_path, best_cost = None, None, float('inf')
    for r_pos in city_grid.recharge_stations:
        path, cost = astar_3d(city_grid, current_pos, r_pos)
        if path is not None and cost < best_cost:
            best_pos, best_path, best_cost = r_pos, path, cost
    return best_pos, best_path, best_cost


def plan_mission(city_grid, initial_energy, recharge_penalty):

    log      = []
    segments = []

    if not city_grid.start:
        return _fail([], 0.0, 0.0, segments, log, "No start position (S) found in grid.")
    if not city_grid.base:
        return _fail([], 0.0, 0.0, segments, log, "No base station (B) found in grid.")

    if not city_grid.goals:
        log.append("  [!] No survivor goals found — flying directly to base.")

    ordered_goals = _greedy_goal_order(city_grid.start, city_grid.goals)
    waypoints     = ordered_goals + [("Base (B)", city_grid.base)]

    full_path      = [city_grid.start]
    total_cost     = 0.0
    current_energy = float(initial_energy)
    current_pos    = city_grid.start

    log.append(f"  Goal visit order: {' → '.join(lbl for lbl, _ in ordered_goals)} → Base (B)")

    for label, next_goal in waypoints:
        log.append(f"\n{'─'*52}")
        log.append(f"  Target : {label}  at  {next_goal}")

        path, cost = astar_3d(city_grid, current_pos, next_goal)

        if path is None:
            log.append(f"  [ERROR] No valid path from {current_pos} to {label}.")
            return _fail(full_path, total_cost, current_energy, segments, log,
                         f"No path to {label}.")

        # ── recharge check ────────────────────────────────────────────────────
        if cost > current_energy:
            log.append(
                f"  [!] Insufficient energy (have={current_energy:.1f}, "
                f"need={cost:.1f}).  Seeking recharge station…"
            )

            r_pos, r_path, r_cost = _find_nearest_recharge(city_grid, current_pos)

            if r_pos is None:
                log.append("  [ERROR] No recharge station reachable from current position.")
                return _fail(full_path, total_cost, current_energy, segments, log,
                             "No recharge station reachable.")

            if r_cost > current_energy:
                log.append(
                    f"  [ERROR] Energy ({current_energy:.1f}) depleted before reaching "
                    f"nearest R at {r_pos} (cost={r_cost:.1f})."
                )
                return _fail(full_path, total_cost, current_energy, segments, log,
                             "Energy depleted before reaching recharge station.")

            # fly to recharge station
            full_path.extend(r_path[1:])
            total_cost     += r_cost
            current_energy -= r_cost
            segments.append({"label": f"→ Recharge at {r_pos}", "path": r_path, "cost": r_cost})
            log.append(
                f"  Diverting to R at {r_pos}  "
                f"(segment cost={r_cost:.1f}, energy before recharge={current_energy:.1f})"
            )

            # recharge
            current_energy = float(initial_energy) - float(recharge_penalty)
            current_pos    = r_pos
            log.append(
                f"  Recharged.  Energy restored to {current_energy:.1f} "
                f"(penalty={recharge_penalty:.1f})"
            )

            # re-pathfind to goal after recharging
            path, cost = astar_3d(city_grid, current_pos, next_goal)
            if path is None:
                log.append(f"  [ERROR] No path from R station {r_pos} to {label}.")
                return _fail(full_path, total_cost, current_energy, segments, log,
                             f"No path from recharge station to {label}.")
            if cost > current_energy:
                log.append(
                    f"  [ERROR] Even after recharge, energy ({current_energy:.1f}) "
                    f"insufficient for cost={cost:.1f} to reach {label}."
                )
                return _fail(full_path, total_cost, current_energy, segments, log,
                             f"Insufficient energy after recharge to reach {label}.")

        # ── fly to goal ───────────────────────────────────────────────────────
        full_path.extend(path[1:])
        total_cost     += cost
        current_energy -= cost
        segments.append({"label": label, "path": path, "cost": cost})
        current_pos = next_goal

        log.append(f"  Route  : {' → '.join(str(p) for p in path)}")
        log.append(f"  Cost   : {cost:.1f}   |   Energy remaining: {current_energy:.1f}")

    # ── success ───────────────────────────────────────────────────────────────
    return {
        "success":          True,
        "full_path":        full_path,
        "total_cost":       total_cost,
        "energy_remaining": current_energy,
        "segments":         segments,
        "log":              log,
    }


def _fail(full_path, total_cost, energy, segments, log, msg):
    log.append(f"  [ERROR] {msg}")
    return {
        "success":          False,
        "full_path":        full_path,
        "total_cost":       total_cost,
        "energy_remaining": energy,
        "segments":         segments,
        "log":              log,
    }



def visualize_grid(city_grid, path_positions):

    lines = []
    separator = "  +" + "---+" * city_grid.cols

    for z in range(city_grid.levels):
        name = LEVEL_NAMES.get(z, f"Level {z}")
        lines.append(f"\n  z={z}  [{name}]")
        lines.append(separator)

        for x in range(city_grid.rows):
            row_cells = []
            for y in range(city_grid.cols):
                cell = city_grid.get_cell(x, y, z)
                pos  = (x, y, z)

                if pos in path_positions:
                    special = (cell in ('S', 'B', 'R') or
                               (len(cell) >= 2 and cell[0] == 'G' and cell[1:].isdigit()))
                    row_cells.append(f" {cell[:2].ljust(2)}" if special else " * ")
                elif cell == OBSTACLE:
                    row_cells.append(" # ")
                elif cell == FIRE:
                    row_cells.append(" F ")
                elif cell in ('S', 'B', 'R'):
                    row_cells.append(f" {cell} ")
                elif len(cell) >= 2 and cell[0] == 'G' and cell[1:].isdigit():
                    row_cells.append(f"{cell[:2].center(3)}")
                else:
                    row_cells.append(" . ")

            lines.append("  |" + "|".join(row_cells) + "|")
            lines.append(separator)

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="3D Drone A* Navigation — Smart City Rescue Mission",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument('grid_file',
                        help='Path to city grid JSON file')
    parser.add_argument('--energy', type=float, default=None,
                        metavar='ENERGY',
                        help='Initial drone energy (overrides JSON value)')
    parser.add_argument('--recharge-penalty', type=float, default=None,
                        metavar='PENALTY',
                        help='Energy penalty for stopping at a recharge station '
                             '(overrides JSON value)')
    args = parser.parse_args()

    if not os.path.isfile(args.grid_file):
        print(f"[ERROR] Grid file not found: {args.grid_file}", file=sys.stderr)
        sys.exit(1)

    with open(args.grid_file) as fh:
        data = json.load(fh)

    city    = CityGrid(data)
    energy  = args.energy if args.energy is not None else city.default_energy
    penalty = args.recharge_penalty if args.recharge_penalty is not None else city.default_penalty

    SEP = "=" * 60
    survivors_str = (
        ', '.join(f"{k}@{v}" for k, v in sorted(city.goals.items()))
        if city.goals else "None"
    )
    header = [
        SEP,
        "     3D DRONE RESCUE MISSION — A* NAVIGATION SYSTEM",
        SEP,
        f"  Grid dimensions : {city.rows} rows × {city.cols} cols × {city.levels} levels",
        f"  Start (S)       : {city.start}",
        f"  Survivors       : {survivors_str}",
        f"  Base (B)        : {city.base}",
        f"  Recharge (R)    : {city.recharge_stations if city.recharge_stations else 'None'}",
        f"  Initial energy  : {energy}",
        f"  Recharge penalty: {penalty}",
        SEP,
    ]

    result = plan_mission(city, energy, penalty)

    summary = ["", SEP, "  MISSION SUMMARY", SEP]

    if result['success']:
        summary.append("\n  Segments:")
        for seg in result['segments']:
            n_steps = len(seg['path'])
            summary.append(f"    [{seg['label']}]  steps={n_steps}  cost={seg['cost']:.1f}")
        summary += [
            "",
            f"  Full path  ({len(result['full_path'])} positions):",
            f"  {result['full_path']}",
            "",
            f"  Total energy consumed : {result['total_cost']:.1f}",
            f"  Energy remaining      : {result['energy_remaining']:.1f}",
            f"  Mission status        : SUCCESS",
        ]
    else:
        summary += [
            "  Mission FAILED — see log above for error details.",
            f"  Energy consumed so far : {result['total_cost']:.1f}",
            f"  Energy remaining       : {result['energy_remaining']:.1f}",
            f"  Mission status         : FAILED",
        ]

    viz = [
        "",
        SEP,
        "  GRID VISUALISATION",
        "  Legend: S=Start  B=Base  R=Recharge  Gn=Survivor",
        "          F=Fire   #=Wall  *=Path step  .=Free",
        SEP,
        visualize_grid(city, set(result['full_path'])),
        "",
    ]

    all_lines = header + result['log'] + summary + viz
    output_text = "\n".join(all_lines) + "\n"

    print(output_text)

    out_path = os.path.join(
        os.path.dirname(os.path.abspath(args.grid_file)), 'output.txt'
    )
    with open(out_path, 'w') as fh:
        fh.write(output_text)

    print(f"  Output saved → {out_path}")


if __name__ == '__main__':
    main()
