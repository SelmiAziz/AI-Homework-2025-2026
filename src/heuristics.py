# heuristics.py

def h_null(state):
    """Heuristica nulla"""
    return 0


def h_box_mismatch(state):
    """Numero di box non sui goal"""
    return sum(1 for b in state.boxes if b not in state.map.goals)


def h_manhattan(state):
    """Somma distanza Manhattan box-goal"""
    total = 0
    for b in state.boxes:
        total += min(
            abs(b[0] - g[0]) + abs(b[1] - g[1])
            for g in state.map.goals
        )
    return total


def h_manhattan_improved(state):
    """
    Manhattan + penalità deadlock semplice
    (box in angolo non-goal)
    """
    dist = 0
    for b in state.boxes:
        if b in state.map.goals:
            continue

        dist += min(
            abs(b[0] - g[0]) + abs(b[1] - g[1])
            for g in state.map.goals
        )

        r, c = b
        walls = state.map.walls

        # deadlock: angolo
        if ((r-1, c) in walls or (r+1, c) in walls) and \
           ((r, c-1) in walls or (r, c+1) in walls):
            dist += 1000

    return dist

