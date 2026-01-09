from node import Node
from problem import Problem
from typing import List, Tuple, Set, Callable
from state import State
import heapq
import itertools 

class AStar:
  def __init__(self, heuristic: Callable[[State], float]): 
    self.heuristic = heuristic 
    self.expandedNodes = 0
  
  def run(self, problem:Problem):
    frontier = []
    counter = itertools.count()
    heapq.heappush(frontier, (0, next(counter), Node(problem.initialState)))
    explored = set() 
    
    while frontier: 
      _, _, node = heapq.heappop(frontier)
      if node.state in explored: 
        continue
      self.expandedNodes += 1
      if problem.goalState(node.state):
        return node
      explored.add(node.state)
      for action in problem.getStateActions(node.state):
        childState = problem.childState(node.state, action)
        #la seguente non mi torna
        childNode = node.createChild(problem, action) 
        if childState not in explored: 
        	heapq.heappush(frontier, (childNode.g()+self.heuristic(childState), next(counter), childNode))
    print("Non trovato sol")
    return None
