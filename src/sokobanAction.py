from action import Action

class SokobanAction(Action): 
	def __init__(self, name, mr, mc): 
		super().__init__(name)
		self.mr = mr
		self.mc = mc

