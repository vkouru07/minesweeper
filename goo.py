import minesweeper as mine
import pgzrun

class Goo:
    class _Space (pgzrun.Actor):
        def __init__(self, isbomb: bool, surrounding: int, x:int, y:int):
            WIDTH = 35 # TODO 
            self.visible = False
            self.flagged = False
            self.isbomb = isbomb
            self.surrounding = surrounding
            super ("flagged", (x, y)) # TODO probably terrible practice 
        
        def update (self):
            if self.visible:
                if self.isbomb:
                    self.image = "bomb"
                else:
                    self.image = "nm" + self.surrounding
            else:
                if self.flagged:
                    self.image = "flagged"
                else:
                    self.image = "blank"

    def __init__(self, board: mine.Board, x:int, y:int):
        self.textboard = board.board
        self.ROWS = board.ROWS
        self.COlS = board.COLS
        self.x = x
        self.y = y
        self.board = [[None for _ in range (self.COlS)] for _ in range (self.ROWS)]
        self._create_board ()

    def _create_board (self):
        for r in range (self.ROWS):
            for c in range (self.COlS):
                b = self.textboard [r][c]
                self.board[r][c] = self._Space (b.isbomb, b.surrounding, self.x + c * self._Space.WIDTH)
                self.board[r][c].draw()

    def update (self, r, c, f):
        pass
    
    def _draw (self):
        pass

    def handle_click (pos):
        pass