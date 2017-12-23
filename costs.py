def ones_cost(state):
    s = 0
    for v in state.field:
        if state.field[v] == 1:
            s += 1
            continue
        if state.field[v] == 2:
            s += -1
            continue
    return s - state.player

def dummy_cost(state):
    return 0

def get_linear_rank_cost(weights):
    def f(state):
        s = 0
        for v in weights:
            if state.field[v] == 1:
                s += weights[v]
                continue
            if state.field[v] == 2:
                s += -weights[v]
                continue
        return s - state.player
    return f