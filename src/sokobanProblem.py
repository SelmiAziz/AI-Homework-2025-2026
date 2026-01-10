from problem import Problem
from sokobanState import SokobanState
from sokobanAction import SokobanAction


class SokobanProblem(Problem):
  def __init__(self,initialState): 
    super().__init__(initialState)
    
  def goalState(self, state): 
  	return state.boxes == self.initialState.map.goals
  
  def getStateActions(self, state): 
    actions = []
    for name, mr, mc in [("Up", -1,0), ("Down", 1,0), ("Left", 0, -1), ("Right", 0, 1)]:
      r,c = state.player
      nr, nc = r +mr, c +mc
      if (nr, nc) in self.initialState.map.walls: continue
      if (nr, nc) in state.boxes: 
      	br, bc = nr+mr, nc + mc
      	if(br,bc) in state.map.walls  or (br, bc) in state.boxes: continue
      	actions.append(SokobanAction(name, mr, mc)) 
      else:
      	actions.append(SokobanAction(name, mr, mc))
    return actions
  
  def childState(self, state, action):
    dr, dc = action.mr, action.mc
    nr, nc = state.player[0]+dr, state.player[1] + dc
    boxes = set(state.boxes)
    if(nr, nc) in boxes:
      boxes.remove((nr, nc))
      boxes.add((nr+dr, nc + dc))
    return SokobanState((nr, nc), boxes, state.map)
    

