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
  
  def childNode(self, problem, action): 
  	return Node(problem.childState(self.state, action), self,action, self.pathCost + action.cost) 
  
  def solution(self): 
    actions = []
  	
    node = self
    
    while node.parent is not None: 
    	actions.append(node.action) 
    	node = node.parent
    
    actions.reverse()
    return actions
    
