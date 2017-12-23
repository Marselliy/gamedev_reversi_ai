def alphabeta(state, depth, cost, a=(-float('inf')), b=float('inf'), first=True):
    if depth == 0 or state.is_terminal():
        return cost(state)
    if state.player == 1:
        v = -float('inf')
        if first:
            next_states = {}
        for i, s in enumerate(state.expand_state()):
            m = alphabeta(s, depth - 1, cost, a, b, first=False)
            if m >= v:
                v = m
                if first:
                    if m in next_states.keys():
                        next_states[m].append(i)
                    else:
                        next_states[m] = [i]
            a = max(a, v)
            if b <= a:
                break
        if first:
            return v, next_states[v]
        return v
    else:
        v = float('inf')
        if first:
            next_states = {}
        for i, s in enumerate(state.expand_state()):
            m = alphabeta(s, depth - 1, cost, a, b, first=False)
            if m <= v:
                v = m
                if first:
                    if m in next_states.keys():
                        next_states[m].append(i)
                    else:
                        next_states[m] = [i]
            b = min(b, v)
            if b <= a:
                break
        if first:
            return v, next_states[v]
    return v