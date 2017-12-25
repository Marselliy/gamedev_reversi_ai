import numpy as np
import argparse
import random
import datetime
from state import State, HOLE
from costs import ones_cost, get_linear_rank_cost
from state_search import alphabeta
import progressbar

from pyswarm import pso

parser = argparse.ArgumentParser(description='Game options.')
parser.add_argument('width', nargs='?', help='Field width', default=4, type=int)
parser.add_argument('height', nargs='?', help='Field height', default=4, type=int)
parser.add_argument('depth', nargs='?', help='Tree search depth', default=3, type=int)
parser.add_argument('iterations', nargs='?', help='PSO iterations', default=10, type=int)
parser.add_argument('swarmsize', nargs='?', help='PSO swarmsize', default=12, type=int)
parser.add_argument('processes', nargs='?', help='Number of processes', default=12, type=int)

args = parser.parse_args()

width = args.width
height = args.height
depth = args.depth
iterations = args.iterations
swarmsize = args.swarmsize
processes = args.processes


def compare_costs(cost1, cost2, rounds=1, depth=5, width=4, height=4):
    total_score = 0
    bar = progressbar.ProgressBar()
    for r in bar(range(rounds)):
        s = State(width, height)
        if r % 2:
            s.player = 3 - s.player

        while not s.is_terminal():
            next_state_indices = 0
            if s.player == 1:
                next_state_indices = alphabeta(s, depth, cost1)[1]
            else:
                next_state_indices = alphabeta(s, depth, cost2)[1]
            s = s.expand_state()[random.choice(next_state_indices)]
            #s.draw()
        total_score += ones_cost(s) > 0
    return total_score / rounds

def h_score(cost, rounds, depth, width, height):
    return compare_costs(cost, ones_cost, rounds, depth, width, height)

def f(x):
    x = x.reshape(height, width)
    d = dict()
    for i in range(x.shape[0]):
        for j in range(x.shape[1]):
            d[(i, j)] = x[i, j]
    y = h_score(get_linear_rank_cost(d), 100, depth, width, height)
    return -y


x = pso(f, -1 * np.ones(height * width), 2 * np.ones(height * width), maxiter=iterations, debug=True, swarmsize=swarmsize, processes=processes)[0]

date = datetime.datetime.now()
filename = './%dx%d_%.4d_%.2d_%.2d_%.2d_%.2d_%.2d' % (width, height, date.year, date.month, date.day, date.hour, date.minute, date.second)

np.save(filename, x)
