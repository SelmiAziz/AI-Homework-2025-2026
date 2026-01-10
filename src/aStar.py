from node import Node
from problem import Problem
from typing import Callable
from state import State
import heapq
import itertools
import time

class AStar:
    def __init__(self, heuristic: Callable[[State], float]):
        self.heuristic = heuristic
        # metriche
        self.expandedNodes = 0
        self.generatedNodes = 0
        self.branchingFactors = []
        self.maxFrontier = 0
        self.maxExplored = 0
        self.timeElapsed = 0

    def run(self, problem: Problem):
        start_time = time.time()

        frontier = []
        counter = itertools.count()
        heapq.heappush(frontier, (0, next(counter), Node(problem.initialState)))
        explored = set()

        while True:
            # Se la frontier è vuota → failure
            if not frontier:
                self.timeElapsed = time.time() - start_time
                print("Failure: soluzione non trovata")
                return None

            # estrai nodo con f minimo
            _, _, node = heapq.heappop(frontier)

            # controllo goal
            if problem.goalState(node.state):
                self.timeElapsed = time.time() - start_time
                return node.solution()

            explored.add(node.state)
            self.expandedNodes += 1

            actions = problem.getStateActions(node.state)
            self.branchingFactors.append(len(actions))
            self.generatedNodes += len(actions)

            for action in actions:
                childNode = node.childNode(problem, action)
                childState = childNode.state
                f_child = childNode.g() + self.heuristic(childState)

                # cerca se esiste già un nodo con lo stesso stato nella frontier
                replaced = False
                for i, (f_existing, _, existingNode) in enumerate(frontier):
                    if existingNode.state == childState:
                        if f_child < f_existing:
                            # sostituisci il nodo esistente con il nuovo
                            frontier[i] = (f_child, next(counter), childNode)
                            heapq.heapify(frontier)  # ricrea l'heap
                        replaced = True
                        break

                # se non era presente, aggiungi normalmente
                if not replaced and childState not in explored:
                    heapq.heappush(frontier, (f_child, next(counter), childNode))

            # aggiorna memoria massima
            self.maxFrontier = max(self.maxFrontier, len(frontier))
            self.maxExplored = max(self.maxExplored, len(explored))


