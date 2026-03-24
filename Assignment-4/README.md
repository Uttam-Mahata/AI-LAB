# Assignment 4 — 3D Drone Rescue Navigation (A\* Search)

## Problem

An AI-powered drone must navigate a layered 3D smart city, rescue all stranded
survivors (G1, G2, …), and return to base (B) while minimising total energy
consumption.  The implementation uses the **A\* search algorithm** with a
3D Euclidean heuristic.

## Grid

The city is a `rows × cols × levels` grid loaded from a JSON file.

| Symbol | Meaning               | Cost to enter |
|--------|-----------------------|---------------|
| `0`    | Road / open space     | 1             |
| `1`    | Building / obstacle   | impassable    |
| `F`    | Fire zone             | 3             |
| `S`    | Drone start           | 1             |
| `Gn`   | Survivor (goal)       | 1             |
| `R`    | Recharge station      | 1             |
| `B`    | Base (final goal)     | 1             |

## Movement & Energy Costs

Six-directional movement (no diagonals):

```
Horizontal (N/S/E/W) : terrain_cost(destination)
Ascending  (z + 1)   : terrain_cost(destination) + 2
Descending (z − 1)   : 1   (gravity assist)
```

## Files

| File                          | Description                        |
|-------------------------------|------------------------------------|
| `drone_navigation.py`         | Main A\* implementation             |
| `city_grid.json`              | Example 5×5×3 city grid            |
| `output.txt`                  | Mission log (generated on run)     |
| `a_star_3d_documentation.tex` | Full LaTeX documentation           |

## Usage

```bash
python drone_navigation.py city_grid.json
python drone_navigation.py city_grid.json --energy 80 --recharge-penalty 10
```

## Algorithm Summary

1. **Goal ordering** — greedy nearest-neighbour heuristic orders survivors.
2. **Segment A\*** — A\* is run independently for each segment:
   `S → G1 → G2 → … → Gn → B`.
3. **Recharge logic** — if energy is insufficient for the next segment, the
   drone is diverted to the nearest recharge station (R), restoring energy to
   `initial_energy − recharge_penalty`.
4. **Edge cases** — no valid path, energy depletion before R, unreachable B.
