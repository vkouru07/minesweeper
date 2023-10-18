import random
import re

movements = [[-1, -1], [-1, 0], [-1, 1],
             [0, -1],           [0, 1],
             [1, -1], [1, 0], [1, 1]]

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

        self.n_bombs = random.randrange (1, int(self.COLS * self.ROWS / 4) + 1)
        planted = 0
        while planted < self.n_bombs:
            x = random.randrange (self.COLS)
            y = random.randrange (self.ROWS)
            
            if self.board[y][x].isbomb:
                continue
            self.board[y][x].isbomb = True
            for move in movements:
                try:
                    self.board[y + move[0]][x + move[1]].surrounding += 1
                except IndexError:
                    pass
                
            planted += 1


    def __str__ (self):
        st = ""
        for row in self.board:
            for s in row:
                st += str(s) + " "
            st += "\n"
        return st

    # true if safe, false if gameover  
    def turn (self, r:int, c:int, f:bool) -> bool:
        if r < 0 or r >= self.ROWS or c < 0 or c >= self.COLS:
            return True
        if f:
            self.board[r][c].flagged = not self.board[r][c].flagged
            return True
        
        self.board[r][c].visible = True
        if self.board[r][c].isbomb:
            return False
        
        self._remptyspace (r, c)
        return True

    def _remptyspace (self, r:int, c:int):
        if self.board[r][c].isbomb:
            return
        if self.board[r][c].surrounding != 0:
            return
        
        self.board[r][c].visible = True
        for move in movements:
            self._remptyspace (r + move[0], c + move[1])