from state import State

class SokobanState(State):
    def __init__(self, player, boxes, mapSokoban): 
        self.player = player
        self.boxes = frozenset(boxes)
        self.map = mapSokoban
    
    def __hash__(self):
        return hash((self.player, self.boxes))
    
    def __eq__(self, other):
        return self.player == other.player and self.boxes == other.boxes
    
    def __lt__(self, other):
        return (self.player, sorted(self.boxes)) < (other.player, sorted(other.boxes))
    
    def print(self):
        for r in range(self.map.rows): 
            row = ""
            for c in range(self.map.cols): 
                pos = (r, c)
                if pos in self.map.walls:
                    row += "#"
                elif pos == self.player:
                    if pos in self.map.goals:
                        row += "+"   # player sul goal
                    else:
                        row += "@"   # player normale
                elif pos in self.boxes:
                    if pos in self.map.goals:
                        row += "*"   # box sul goal
                    else:
                        row += "$"   # box normale
                elif pos in self.map.goals:
                    row += "."       # goal vuoto
                else:
                    row += " "       # spazio vuoto
            print(row)
        print()

