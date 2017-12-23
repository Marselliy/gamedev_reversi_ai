import sys
import copy

HOLE = -1
EMPTY = 0
DIRECTIONS = [
    (0, 1),
    (1, 0),
    (0, -1),
    (-1, 0),
    (-1, -1),
    (-1, 1),
    (1, -1),
    (1, 1),
]

def cache(function):
    memo = {}
    def wrapper(*args):
        if args[0].hash in memo:
            return memo[args[0].hash]
        else:
            rv = function(*args)
            memo[args[0].hash] = rv
            return rv
    return wrapper

class State:
    def __init__(self, w, h):
        self.width=w
        self.height=h
        self.field=dict()
        for x in range(h):
            for y in range(w):
                self.field[(x, y)] = EMPTY
        self.field[(h // 2, w // 2)] = 1
        self.field[(h // 2 - 1, w // 2 - 1)] = 1
        self.field[(h // 2 - 1, w // 2)] = 2
        self.field[(h // 2, w // 2 - 1)] = 2    
        
        self.player = 1
        self.compute_hash()
        
    def compute_hash(self):
        self.hash = hash((frozenset(self.field.items()), self.player))
        
    def make_move(self, pos):
        adversary = 3 - self.player

        state = copy.copy(self)
        state.field = dict(self.field)
        state.player = adversary

        for direction in DIRECTIONS:
            terminate = False
            first_move = True
            cur = pos
            while not terminate:
                cur = (cur[0] + direction[0], cur[1] + direction[1])
                try:
                    if state.field[cur] == EMPTY or state.field[cur] == HOLE:
                        terminate = True
                        continue
                    if state.field[cur] == self.player:
                        if not first_move:
                            while cur != pos:
                                state.field[cur] = self.player
                                cur = (cur[0] - direction[0], cur[1] - direction[1])
                            state.field[pos] = self.player
                        terminate = True
                        continue
                    if state.field[cur] == adversary:
                        first_move = False
                        continue
                except:
                    terminate = True
                    
        state.compute_hash()
        return state 
    
    @cache    
    def expand_state(self, retry=False):        
        adversary = 3 - self.player

        next_states = []
        possible_moves = set()

        for x in range(self.height):
            for y in range(self.width):
                if self.field[(x, y)] != self.player:
                    continue

                for direction in DIRECTIONS:
                    terminate = False
                    first_move = True
                    cur = (x, y)
                    depth = 0
                    while not terminate:
                        depth += 1
                        cur = (cur[0] + direction[0], cur[1] + direction[1])
                        try:
                            if self.field[cur] == EMPTY:
                                if not first_move:
                                    new_state = copy.copy(self)
                                    new_state.field = dict(self.field)
                                    new_state.player = adversary

                                    for d in range(depth):
                                        new_state.field[cur] = self.player
                                        cur = (cur[0] - direction[0], cur[1] - direction[1]) 
                                        
                                    new_state.compute_hash()
                                    next_states.append(new_state)

                                terminate = True
                                continue
                            if self.field[cur] == adversary:
                                first_move = False
                                continue
                            if self.field[cur] == HOLE or self.field[cur] == self.player:
                                terminate = True
                                continue
                        except KeyError:
                            terminate = True
                            
        if len(next_states) > 0 or retry:
            return next_states
        state = copy.copy(self)
        state.field = dict(self.field)
        state.player = adversary
        state.compute_hash()
        return state.expand_state(True)
        
    def is_terminal(self):
        return len(self.expand_state()) == 0
        
    def draw(self):
        for x in range(self.height):
            for y in range(self.width):
                if self.field[(x, y)] == EMPTY:
                    sys.stdout.write('. ')
                    continue
                if self.field[(x, y)] == 1:
                    sys.stdout.write('1 ')
                    continue
                if self.field[(x, y)] == 2:
                    sys.stdout.write('2 ')
                    continue
                if self.field[(x, y)] == HOLE:
                    sys.stdout.write('X ')
                    continue
            print() 
            
def rank_cost(state):
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

def get_weighted_rank_cost(weights):
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