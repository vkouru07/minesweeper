import random
import re

class Board:
    class _Space:
        def __init__ (self):
            self.visible = False
            self.flagged = False
            self.isbomb = False
            self.surrounding = 0
        
        def __str__(self) -> str:
            if self.visible:
                if self.isbomb:
                    return "ø"
                return str(self.surrounding)
            if self.flagged:
                return "%"
            return "_"
    
    def __init__(self, rows: int, cols: int):
        self.ROWS = rows
        self.COLS = cols

        self._rand_board()

    def _rand_board (self):
        self.board = [[self._Space() for _ in range (self.COLS)] for _ in range(self.ROWS)]

        self.n_bombs = random.randrange (16, 20)
        planted = 0
        while planted < self.n_bombs:
            x = random.randrange (self.COLS)
            y = random.randrange (self.ROWS)
            
            if self.board[y][x].isbomb:
                continue
            self.board[y][x].isbomb = True
            planted += 1

    def draw (self):
        print ("called")
        for row in self.board:
            for bomb in row:
                print (bomb, sep="")
            print()

    def __str__ (self):
        pass

    