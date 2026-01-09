from state import State


class SokobanState(State):
  def __init__(self, player, boxes, mapSokoban): 
    self.player = player
    self.boxes = frozenset(boxes)
    self.map = mapSokoban
    
  def __hash__(self): return hash((self.player, self.boxes)) 
  def __eq__(self, other): return self.player == other.player and self.boxes == other.boxes
  def __lt__(self, other): return (self.player, sorted(self.boxes)) < (other.player, sorted(other.boxes)) 
  def print(self):
    for r in range(self.map.rows): 
        row = ""
        for c in range(self.map.cols): 
            p = (r,c)
            if p in self.map.walls:
                row += "#"
            elif p == self.player:
                row += "@"
            elif p in self.boxes and p in self.map.goals:
                row += "*"   # scatola sul goal
            elif p in self.boxes:
                row += "$"
            elif p in self.map.goals:
                row += "."
            else:
                row += " "
        print(row)
    print()

    
