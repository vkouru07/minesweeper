import random
import re
import logging

# row, col 
MOVEMENTS = [[-1, -1], [-1, 0], [-1, 1],
             [0, -1],           [0, 1],
             [1, -1], [1, 0], [1, 1]]
CROSS_MOVEMENTS = [MOVEMENTS[1], MOVEMENTS[3], MOVEMENTS[4], MOVEMENTS[6]]

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

        self.board = None
        self.n_bombs = 0
        self._rand_board()
        self.n_non_bomb_squares = self.ROWS * self.COLS - self.n_bombs
        

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
            for move in MOVEMENTS:
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
        self._remptyspace (r, c, True)
        return True

    def _remptyspace (self, r:int, c:int, first):
        if r < 0 or r >= self.ROWS or c < 0 or c >= self.COLS:
            return
        if self.board[r][c].isbomb or not first and self.board[r][c].visible:
            return
        
        if self.board[r][c].surrounding > 0:
            for move in MOVEMENTS:
                self.board[r + move[0]][c + move[1]].visible = True
                self.n_non_bomb_squares -= 1
            return
        
        self.board[r][c].visible = True
        self.n_non_bomb_squares -= 1

        for move in CROSS_MOVEMENTS:
            self._remptyspace (r + move[0], c + move[1], False)
        return
        
    def setall_visible (self):
        for row in self.board:
            for s in row:
                s.visible = True