import json
from sokobanMap import SokobanMap
from sokobanState import SokobanState
from sokobanProblem import SokobanProblem
from sokobanAction import SokobanAction
from aStar import AStar


with open("levels.json", "r", encoding = "utf-8") as f: 
	levels = json.load(f) 


level = levels["intermediate"][0]


walls, goals, boxes = set(), set(), set() 

playerStart = None

for r, row in enumerate(level): 
  for c, char in enumerate(row):
    if char == "#": walls.add((r,c)) 
    if char == ".": goals.add((r,c)) 
    if char == "$": boxes.add((r,c))
    if char == "@": playerStart = (r,c)

m = SokobanMap(walls, goals, len(level), len(level[0]))
s = SokobanState(playerStart, boxes,m)
p = SokobanProblem(m, playerStart, boxes)
a = SokobanAction("Right", 0, -1)


def h_manhattan(state):
        return sum(min(abs(b[0]-g[0])+abs(b[1]-g[1]) for g in state.map.goals) for b in state.boxes)

a = AStar(h_manhattan)


s = a.run(p)

s.printPath()


