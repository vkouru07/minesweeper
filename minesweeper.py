import pgzrun
from pgzero.builtins import Actor
import random
import oth

class Minesweeper ():
    def __init__(self, rows, cols, n_bombs, s_width):
        self.ROWS = rows
        self.COLS = cols 
        self.BOMBS = n_bombs
        self.S_WIDTH = s_width

        # 0 actor obj, 1 is it a bomb?, 2 surrounding bombs, 3 flagged?, 4 visible?
        self._grid = [[[Actor('11'), False, 0, False, False] for _ in range(self.COLS +1)] for _ in range(self.ROWS +1)]
        self.position_grid ()
    
    def position_grid (self):
        for row in range (self.ROWS):
            for col in range (self.COLS):
                self._grid[row][col][0].pos = self.S_WIDTH * (col + 1/2), self.S_WIDTH * (row + 1/2)

    def initboard (self, pos):
        untouched = [(pos[0] + x[0], pos[1] + x[1]) for x in oth.MOVEMENTS]
        
        planted = 0
        while planted < self.BOMBS:
            r = random.choice (range(self.ROWS))
            c = random.choice (range(self.COLS))

            if self._grid[r][c][1] or (r == pos[0] and c == pos[1]) or (r, c) in untouched:
                continue
            self._grid[r][c][1] = True

            for move in oth.MOVEMENTS:
                try:
                    self._grid [r + move[0]][c + move[1]][2] += 1
                except IndexError:
                    pass
            planted += 1

        self.empty_space (pos[0], pos[1])

    def _update_img (self, row:int, col:int):
     # 0 actor obj, 1 is it a bomb?, 2 surrounding bombs, 3 flagged?, 4 visible?
        if not self._grid [row][col][4]:
            if self._grid [row][col][3]:
                self._grid [row][col][0].image = '11'
            else:
                self._grid [row][col][0].image = '10'
        else:
            if self._grid [row][col][1]:
                self._grid [row][col][0].image = '09'
            else:
                self._grid [row][col][0].image = '0' + str(self._grid[row][col][2])

        self._grid [row][col][0].draw()
    
    def isbomb (self, row:int, col:int) -> bool:
        return self._grid [row][col][1]
    def isflagged (self, row:int, col:int) -> bool:
        return self._grid [row][col][3]

    def pressed_bomb (self):
        for r in range (self.ROWS):
            for c in range (self.COLS):
                self._grid [r][c][4] = True

    def toggle_flag (self, row:int, col:int):
        self._grid[row][col][3] = not self._grid[row][col][3]

    def empty_space (self, row:int, col:int):
        if not self.isflagged(row, col):
            self._rempty_space (row, col)
    
    def _rempty_space (self, row:int, col:int):
         # 0 actor obj, 1 is it a bomb?, 2 surrounding bombs, 3 flagged?, 4 visible?
        if self.isbomb(row, col) or self._grid[row][col][4]:
            return
        
        self._grid[row][col][4] = True
        if self._grid [row][col][2] != 0:
            return

        for move in oth.MOVEMENTS:
            r = row + move[0]
            c = col + move[1]
            if r < 0 or r > self.ROWS -2:
                break
            if c < 0 or c > self.COLS -2: 
                break
            self._rempty_space (r, c)
            # try:
            #     self._rempty_space (row + move[0], col + move[1])
            # except IndexError:
            #     pass
        return
    
    def check_if_won (self) -> bool:
        nonbombs = self.ROWS * self.COLS - self.BOMBS
        for r in range(self.ROWS):
            for c in range(self.COLS):
                if not self._grid[r][c][1] and self._grid[r][c][4]:
                    nonbombs -= 1
        return nonbombs == 0

    def draw (self):
        for r in range (self.ROWS):
            for c in range (self.COLS):
                self._update_img (r, c)

    def print(self):
        for row in self._grid:
            for s in row:
                if not s[4]:
                    if s[3]:
                        print (' ', end=' ')
                    else:
                        print (' ', end=' ')
                else:
                    if s[1]:
                        print ('*', end=' ')
                    else:
                        print (s[2], end=' ')
            print ()
