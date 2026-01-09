from abc import ABC, abstractmethod

class Action(ABC): 
	def __init__(self, name: str, cost: float = 1.0): 
		self.name = name
		self.cost = cost
