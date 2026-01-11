import json
import time

from sokobanMap import SokobanMap
from sokobanProblem import SokobanProblem
from sokobanState import SokobanState
from aStar import AStar
from PDDLPlanner import PDDLPlanner

from heuristics import (
    h_null,
    h_box_mismatch,
    h_manhattan,
    h_manhattan_improved
)

# ===============================
# Caricamento livelli
# ===============================
with open("../levels.json", "r", encoding="utf-8") as f:
    levels = json.load(f)

level = levels["intermediate"][1]

# ===============================
# Parsing livello
# ===============================
walls, goals, boxes = set(), set(), set()
playerStart = None

for r, row in enumerate(level):
    for c, char in enumerate(row):
        if char == "#":
            walls.add((r, c))
        elif char == ".":
            goals.add((r, c))
        elif char == "$":
            boxes.add((r, c))
        elif char == "@":
            playerStart = (r, c)

# ===============================
# Creazione problema Sokoban
# ===============================
m = SokobanMap(walls, goals, len(level), len(level[0]))
s = SokobanState(playerStart, boxes, m)
p = SokobanProblem(s)

# ===============================
# Utility: visualizzazione piano
# ===============================
def visualize_plan(problem, plan):
    state = problem.initialState
    print("START")
    state.print()
    for action in plan:
        print("Move:", action.name)
        state = problem.childState(state, action)
        state.print()

# ===============================
# PDDL – Fast Downward
# ===============================
print("\n--- Generazione PDDL e risoluzione con Fast Downward ---")

pddl_solver = PDDLPlanner(level)
plan_generated = pddl_solver.solve()

if plan_generated:
    print("\n=== Piano PDDL generato ===")
    for step in plan_generated:
        print(step)
    print("\n=== Piano PDDL salvato in plan_actions.txt ===")
else:
    print("Nessun piano PDDL trovato.")

# ===============================
# A* search
# ===============================
heuristics = {
    "Null": h_null,
    "Box mismatch": h_box_mismatch,
    "Manhattan": h_manhattan,
    "Manhattan Improved": h_manhattan_improved
}

solvers = {}
plans = {}

for name, h in heuristics.items():
    print(f"\n--- Running A* with {name} ---")
    solver = AStar(h)
    start = time.time()
    plan = solver.run(p)
    solver.timeElapsed = time.time() - start
    solvers[name] = solver
    plans[name] = plan

# ===============================
# Stampa soluzioni
# ===============================
for name, plan in plans.items():
    if plan:
        print(f"\n=== Soluzione A* {name} ===")
        visualize_plan(p, plan)
    else:
        print(f"\nSoluzione A* {name} NON trovata.")

# ===============================
# Metriche A*
# ===============================
def branch_stats(bf):
    if not bf:
        return 0, 0, 0
    return min(bf), sum(bf) / len(bf), max(bf)

for name, solver in solvers.items():
    minBF, avgBF, maxBF = branch_stats(solver.branchingFactors)
    print(f"\n=== METRICHE A* {name} ===")
    print(f"Nodi espansi: {solver.expandedNodes}")
    print(f"Nodi generati: {solver.generatedNodes}")
    print(f"Branching factor (min/avg/max): {minBF:.2f}/{avgBF:.2f}/{maxBF:.2f}")
    print(f"Max memory frontier: {solver.maxFrontier}")
    print(f"Max memory explored: {solver.maxExplored}")
    print(f"Tempo: {solver.timeElapsed:.4f} s")


