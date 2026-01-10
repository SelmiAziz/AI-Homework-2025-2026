class SokobanMap:	
  def __init__(self,walls, goals, rows, cols):
    self.walls = frozenset(walls)
    self.goals = frozenset(goals)
    self.rows = rows 
    self.cols = cols
