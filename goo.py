import minesweeper

class Goo:
    class _Space:
        def __init__(self, isbomb: bool, surrounding: int):
            self.visible = False
            self.flagged = False
            self.isbomb = isbomb
            self.surrounding = surrounding

    def __init__(self, board: minesweeper.Board) -> None:
        self.textboard = board
        self.board = []

    def _create_board (self):
        pass

    def update (self, r, c, f):
        pass
    
    def _draw (self):
        pass

    def handle_click (pos):
        pass