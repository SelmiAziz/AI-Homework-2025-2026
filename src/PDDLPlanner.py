from PlannerConnection import PlannerConnection
import os

class PDDLPlanner:
    """
    Genera PDDL e risolve il problema tramite Fast Downward.
    Mantiene TUTTE le azioni push-up/down/left/right e move come nel tuo PDDL originale.
    """

    def __init__(self, level):
        self.level = level
        self.connection = PlannerConnection()
        self.workdir = self.connection.workdir  # cartella benchmarks

    def solve(self):
        # 1. genera domain.pddl e problem.pddl (tutto identico al tuo PDDL originale)
        self._write_pddl()

        # 2. chiama il planner tramite la nuova connection (senza parametri)
        plan = self.connection.run()
        return plan

    def _write_pddl(self):
        rows, cols = len(self.level), len(self.level[0])
        walls, boxes, goals = set(), [], []
        player = None
        positions = []

        for r, row in enumerate(self.level):
            for c, char in enumerate(row):
                if char != '#':
                    positions.append(f"p{r}_{c}")
                if char == '#':
                    walls.add((r, c))
                if char == '$':
                    boxes.append((r, c))
                if char == '.':
                    goals.append((r, c))
                if char == '@':
                    player = (r, c)

        domain_path = os.path.join(self.workdir, "domain.pddl")
        problem_path = os.path.join(self.workdir, "problem.pddl")

        # --- DOMAIN.PDDL (identico) ---
        with open(domain_path,"w") as f:
            f.write("""(define (domain sokoban)
 (:requirements :strips :typing)
 (:types player box position)
 (:predicates
  (player-at ?p - player ?pos - position)
  (box-at ?b - box ?pos - position)
  (goal ?b - box ?pos - position)
  (empty ?pos - position)
  (adj-up ?f ?t - position)
  (adj-down ?f ?t - position)
  (adj-left ?f ?t - position)
  (adj-right ?f ?t - position)
 )
 (:action move
  :parameters (?p - player ?f ?t - position)
  :precondition (and (player-at ?p ?f) (empty ?t)
    (or (adj-up ?f ?t)(adj-down ?f ?t)(adj-left ?f ?t)(adj-right ?f ?t)))
  :effect (and (not (player-at ?p ?f)) (player-at ?p ?t) (empty ?f) (not (empty ?t)))
 )
 (:action push-up
  :parameters (?p - player ?b - box ?f ?t ?n - position)
  :precondition (and (player-at ?p ?f)(box-at ?b ?t)(adj-up ?f ?t)(adj-up ?t ?n)(empty ?n))
  :effect (and (player-at ?p ?t)(not (player-at ?p ?f))(box-at ?b ?n)(not (box-at ?b ?t))(empty ?f)(not (empty ?n)))
 )
 (:action push-down
  :parameters (?p - player ?b - box ?f ?t ?n - position)
  :precondition (and (player-at ?p ?f)(box-at ?b ?t)(adj-down ?f ?t)(adj-down ?t ?n)(empty ?n))
  :effect (and (player-at ?p ?t)(not (player-at ?p ?f))(box-at ?b ?n)(not (box-at ?b ?t))(empty ?f)(not (empty ?n)))
 )
 (:action push-left
  :parameters (?p - player ?b - box ?f ?t ?n - position)
  :precondition (and (player-at ?p ?f)(box-at ?b ?t)(adj-left ?f ?t)(adj-left ?t ?n)(empty ?n))
  :effect (and (player-at ?p ?t)(not (player-at ?p ?f))(box-at ?b ?n)(not (box-at ?b ?t))(empty ?f)(not (empty ?n)))
 )
 (:action push-right
  :parameters (?p - player ?b - box ?f ?t ?n - position)
  :precondition (and (player-at ?p ?f)(box-at ?b ?t)(adj-right ?f ?t)(adj-right ?t ?n)(empty ?n))
  :effect (and (player-at ?p ?t)(not (player-at ?p ?f))(box-at ?b ?n)(not (box-at ?b ?t))(empty ?f)(not (empty ?n)))
 )
)""")

        # --- PROBLEM.PDDL (identico) ---
        with open(problem_path,"w") as f:
            f.write("(define (problem sokoban1)\n (:domain sokoban)\n")
            f.write(" (:objects player1 - player\n")
            for i in range(len(boxes)):
                f.write(f" box{i} - box\n")
            f.write(" " + " ".join(positions) + " - position)\n (:init\n")
            f.write(f" (player-at player1 p{player[0]}_{player[1]})\n")
            for i, b in enumerate(boxes):
                f.write(f" (box-at box{i} p{b[0]}_{b[1]})\n")
                f.write(f" (goal box{i} p{goals[i][0]}_{goals[i][1]})\n")

            occ = {player} | set(boxes)
            for pos in positions:
                r, c = map(int, pos[1:].split('_'))
                if (r, c) not in occ:
                    f.write(f" (empty {pos})\n")
                if (r-1, c) not in walls and r>0:
                    f.write(f" (adj-up p{r}_{c} p{r-1}_{c})\n")
                if (r+1, c) not in walls and r<rows-1:
                    f.write(f" (adj-down p{r}_{c} p{r+1}_{c})\n")
                if (r, c-1) not in walls and c>0:
                    f.write(f" (adj-left p{r}_{c} p{r}_{c-1})\n")
                if (r, c+1) not in walls and c<cols-1:
                    f.write(f" (adj-right p{r}_{c} p{r}_{c+1})\n")
            f.write(" )\n (:goal (and\n")
            for i in range(len(boxes)):
                f.write(f" (box-at box{i} p{goals[i][0]}_{goals[i][1]})\n")
            f.write(" ))\n)")
