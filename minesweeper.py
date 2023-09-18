import random
import re

class Board:
    def __init__(self, rows: int, cols: int):
        self.ROWS = rows
        self.COLS = cols

        self.rand_board()
        
        pass

    def rand_board (self):
        # it is visible? is it a bomb? num surrounding bombs? 
        self.board = [[[False, False, 0] for _ in range (self.COLS)] for _ in range(self.ROWS)]

        self.n_bombs = random.randrange (16, 20)
        planted = 0
        while planted < self.n_bombs:
            x = random.randrange (0, self.COLS)
            y = random.randrange (self.ROWS)

            if [y][x][1]:
                continue
            [y][y][1] = True
            planted += 1

    def draw ():
        pass

    def __str__ (self):
        pass
