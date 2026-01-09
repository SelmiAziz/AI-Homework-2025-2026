class SokobanMap:	
  def __init__(self,walls, goals, rows, cols):
    self.walls = frozenset(walls)
    self.goals = frozenset(goals)
    self.rows = rows 
    self.cols = cols
  def printAll(self): 
  	print(self.walls)
  	print(self.goals)
  	print(self.rows)
  	print(self.cols)
