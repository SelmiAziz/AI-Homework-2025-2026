import json
import time
from sokobanMap import SokobanMap
from sokobanProblem import SokobanProblem
from sokobanState import SokobanState
from aStar import AStar
from PDDLPlanner import PDDLPlanner  # genera i PDDL e chiama il planner
from PDDLPlan import PDDLPlan        # legge il piano e ricostruisce gli stati

# --- Carica livelli ---
with open("../levels.json", "r", encoding="utf-8") as f: 
    levels = json.load(f) 

# --- Scegli il livello ---
level = levels["easy"][0]

# --- Parsing livello ---
walls, goals, boxes = set(), set(), set()
playerStart = None

for r, row in enumerate(level):
    for c, char in enumerate(row):
        if char == "#": walls.add((r, c))
        if char == ".": goals.add((r, c))
        if char == "$": boxes.add((r, c))
        if char == "@": playerStart = (r, c)

# --- Crea mappa e problema A* ---
m = SokobanMap(walls, goals, len(level), len(level[0]))
s = SokobanState(playerStart, boxes, m)
p = SokobanProblem(s)

# --- Heuristiche ---
def h_null(state):
    return 0

def h_box_mismatch(state):
    return len([b for b in state.boxes if b not in state.map.goals])

def h_manhattan(state):
    return sum(min(abs(b[0]-g[0]) + abs(b[1]-g[1]) for g in state.map.goals) for b in state.boxes)

def h_manhattan_improved(state):
    dist = 0
    for b in state.boxes:
        if b in state.map.goals: continue
        dist += min(abs(b[0]-g[0]) + abs(b[1]-g[1]) for g in state.map.goals)
        r, c = b
        if ((r-1, c) in state.map.walls or (r+1, c) in state.map.walls) and \
           ((r, c-1) in state.map.walls or (r, c+1) in state.map.walls):
            dist += 1000  # penalità deadlock
    return dist

# --- Visualizzazione piano A* ---
def visualize_plan(problem, plan):
    state = problem.initialState
    print("Start")
    state.print()
    for action in plan:
        print("Move:", action.name)
        state = problem.childState(state, action)
        state.print()

# --- Risoluzione A* ---
heuristics = {
    "Manhattan": h_manhattan,
    "Manhattan Improved": h_manhattan_improved
}

solvers = {}
plans = {}

for name, h in heuristics.items():
    print(f"\n--- Running A* with {name} ---")
    solver = AStar(h)
    start_time = time.time()
    plan = solver.run(p)
    solver.timeElapsed = time.time() - start_time
    solvers[name] = solver
    plans[name] = plan

# --- Stampa soluzioni A* ---
for name, plan in plans.items():
    if plan:
        print(f"\n=== Soluzione A* {name} ===")
        visualize_plan(p, plan)
    else:
        print(f"\nSoluzione A* {name} non trovata.")

# --- Branching factor stats ---
def branch_stats(branchingFactors):
    if branchingFactors:
        return min(branchingFactors), sum(branchingFactors)/len(branchingFactors), max(branchingFactors)
    return 0, 0, 0

# --- Stampa metriche A* ---
for name, solver in solvers.items():
    minBF, avgBF, maxBF = branch_stats(solver.branchingFactors)
    print(f"\n=== METRICHE A* {name} ===")
    print(f"Nodi espansi: {solver.expandedNodes}")
    print(f"Nodi generati: {solver.generatedNodes}")
    print(f"Branching factor (min/avg/max): {minBF:.2f}/{avgBF:.2f}/{maxBF:.2f}")
    print(f"Max memoria totale (frontier+explored): {solver.maxFrontier + solver.maxExplored}")
    print(f"Max frontier: {solver.maxFrontier}")
    print(f"Max esplorati: {solver.maxExplored}")
    print(f"Tempo esecuzione: {solver.timeElapsed:.4f} s")

# --- Risoluzione PDDL ---
# ===============================
# Generazione PDDL e salvataggio piano
# ===============================
# ===============================
# Generazione PDDL e salvataggio piano
# ===============================
# ===============================
# Generazione PDDL e salvataggio piano
# ===============================
print("\n--- Generazione PDDL e risoluzione con Fast Downward ---")
pddl_solver = PDDLPlanner(level)
plan_generated = pddl_solver.solve()

if plan_generated:
    print("\n=== Piano PDDL generato ===")
    for step in plan_generated:
        print(step)

    # --- Leggi piano e salva solo le azioni reali ---
    from PDDLPlan import PDDLPlan

    pddl_plan = PDDLPlan()          # legge automaticamente sas_plan
    pddl_plan.load_plan("sas_plan") # filtra solo azioni Sokoban
    pddl_plan.save_actions("plan_actions.txt")  # salva in file

    print("\n=== Piano PDDL salvato in 'plan_actions.txt' ===")
else:
    print("Nessun piano PDDL trovato.")

