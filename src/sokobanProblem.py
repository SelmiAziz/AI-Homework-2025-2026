from problem import Problem
from sokobanState import SokobanState
from sokobanAction import SokobanAction

class SokobanProblem(Problem):
    """
    Rappresenta un problema Sokoban.
    Gestisce gli stati, le azioni valide e il goal.
    """

    def __init__(self, initialState): 
        super().__init__(initialState)
    
    def goalState(self, state): 
        """
        Lo stato è goal se tutte le scatole sono sui goal.
        Il giocatore può stare dove vuole.
        """
        return state.boxes == self.initialState.map.goals
  
    def getStateActions(self, state): 
        """
        Restituisce tutte le azioni valide in uno stato.
        Controlla muri, scatole e altri ostacoli.
        """
        actions = []
        for name, dr, dc in [("Up", -1, 0), ("Down", 1, 0), ("Left", 0, -1), ("Right", 0, 1)]:
            r, c = state.player
            nr, nc = r + dr, c + dc  # nuova posizione player

            # Se c'è un muro, skip
            if (nr, nc) in self.initialState.map.walls:
                continue

            # Se c'è una scatola
            if (nr, nc) in state.boxes:
                br, bc = nr + dr, nc + dc  # posizione box dopo spinta

                # Controlla muro o altra scatola
                if (br, bc) in state.map.walls or (br, bc) in state.boxes:
                    continue

                # Aggiungi azione push
                actions.append(SokobanAction(name, dr, dc))
            else:
                # Azione semplice senza spingere
                actions.append(SokobanAction(name, dr, dc))
        return actions
  
    def childState(self, state, action):
        """
        Restituisce il nuovo stato ottenuto applicando un'azione.
        """
        dr, dc = action.mr, action.mc
        nr, nc = state.player[0] + dr, state.player[1] + dc
        boxes = set(state.boxes)

        # Se il player spinge una scatola, aggiorna la sua posizione
        if (nr, nc) in boxes:
            boxes.remove((nr, nc))
            boxes.add((nr + dr, nc + dc))

        return SokobanState((nr, nc), boxes, state.map)

