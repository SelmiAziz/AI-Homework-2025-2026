from state import State
from action import Action

class Node: 
  def __init__(self, state, parent = None , action = None , pathCost = 0): 
  	self.state = state 
  	self.parent = parent
  	self.action = action
  	self.pathCost = pathCost
  
  def g(self): 
  	return self.pathCost
  
  def createChild(self, problem, action): 
  	return Node(problem.childState(self.state, action), self,action, self.pathCost + action.cost) 
  
  def printPath(self):
    if self.parent: 
  	  self.parent.printPath()
    else: 
    	print("Start")
    if self.action: 
    	print("Move:", self.action.name) 
    self.state.print() 
