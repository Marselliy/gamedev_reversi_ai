import numpy as np
import argparse
import random
from state import State, HOLE
from costs import ones_cost, get_linear_rank_cost
from state_search import alphabeta

from tkinter import *
from tkinter.messagebox import *

parser = argparse.ArgumentParser(description='Game options.')
parser.add_argument('width', nargs='?', help='Field width', default=8, type=int)
parser.add_argument('height', nargs='?', help='Field height', default=8, type=int)
parser.add_argument('player1', nargs='?', help='human or AI player?', default='human')
parser.add_argument('player2', nargs='?', help='human or AI player?', default='AI')
parser.add_argument('difficulty', nargs='?', help='AI difficulty?', default=5, type=int)
parser.add_argument('weight_filepath', nargs='?', help='Path to weight file')

args = parser.parse_args()

width = args.width
height = args.height
player1 = args.player1
player2 = args.player2
difficulty = args.difficulty
weight_filepath = args.weight_filepath

CELL_SIZE = 100
GRID_PADDING = 0
BACKGROUND_COLOR_GAME = "#92877d"
BACKGROUND_COLOR_CELL_EMPTY = "#9e948a"


class GameGrid(Frame):
    def __init__(self, width, height):
        Frame.__init__(self, width=CELL_SIZE*width, height=CELL_SIZE*height)

        self.width = width
        self.height = height

        self.grid()
        self.master.title('Reversi')

        self.grid_cells = []
        self.init_grid()

        self.init_game()
        
        self.update_grid_cells()
        
        self.mainloop()

    def init_grid(self):
        background = Frame(self, bg=BACKGROUND_COLOR_GAME, width=CELL_SIZE*width, height=CELL_SIZE*height)
        background.grid()
        for i in range(height):
            grid_row = []
            for j in range(width):
                cell = Frame(background, bg=BACKGROUND_COLOR_GAME, width=CELL_SIZE, height=CELL_SIZE)
                cell.grid(row=i, column=j, padx=GRID_PADDING, pady=GRID_PADDING)
                c = Canvas(master=cell, bg=BACKGROUND_COLOR_GAME, width=CELL_SIZE, height=CELL_SIZE)

                c.grid()

                def callback(event, i=i, j=j):
                    self.make_move((i, j))
                c.bind('<Button-1>', callback)

                grid_row.append(c)

            self.grid_cells.append(grid_row)

    def init_game(self):
        self.state = State(width, height)
        self.cost = ones_cost
        try:
            x = np.load(weight_filepath).reshape(height, width)
            d = dict()
            for i in range(x.shape[0]):
                for j in range(x.shape[1]):
                    d[(i, j)] = x[i, j]
            self.cost = get_linear_rank_cost(d)
        except:
            pass

    def update_grid_cells(self):
        for i in range(height):
            for j in range(width):
                if self.state.field[(i, j)] == 1:
                    self.grid_cells[i][j].create_oval(0, 0, CELL_SIZE, CELL_SIZE, width=0, fill='white')
                if self.state.field[(i, j)] == 2:
                    self.grid_cells[i][j].create_oval(0, 0, CELL_SIZE, CELL_SIZE, width=0, fill='black')
                if self.state.field[(i, j)] == HOLE:
                    pass

    def make_move(self, pos):
        if [player1, player2][self.state.player - 1] == 'human':
            self.state = self.state.make_move(pos)
        else:
            try:
                next_state_indices = alphabeta(self.state, difficulty, self.cost)[1]
                self.state = self.state.expand_state()[random.choice(next_state_indices)]
            except TypeError:
                pass
        self.update_grid_cells()
        if self.state.is_terminal():
            self.game_over()

    def game_over(self):
        p1_score = len([v for v in list(self.state.field.values()) if v == 1])
        p2_score = len([v for v in list(self.state.field.values()) if v == 2])
        
        header = 0
        if p1_score > p2_score:
            header = 'Player 1 won!'
        elif p1_score < p2_score:
            header = 'Player 2 won!'
        else:
            header = 'Draw!'
        message = 'Player 1 score: %d \r\nPlayer 2 score: %d' % (p1_score, p2_score)
        showinfo(header, message)


gamegrid = GameGrid(width, height)