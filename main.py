import pgzrun
import math
import random
import minesweeper
from pgzero.builtins import Actor, mouse

TITLE = "minesweeper"

ROWS = 10
COLS = 14
S_WIDTH = 45

WIDTH = COLS * S_WIDTH
HEIGHT = ROWS * S_WIDTH
BOMBS = random.randrange (math.floor(ROWS * COLS/8), math.floor(ROWS * COLS/5))

board = minesweeper.Minesweeper (ROWS, COLS, BOMBS, S_WIDTH)
first_click = True
gameover = False

def on_gameover (won:bool):
    if won:
        print ("nice")
    else:
        print ("failed")

def on_mouse_down (pos, button):
    global gameover
    if not gameover:
        row = math.floor(pos[1]/S_WIDTH)
        col = math.floor(pos[0]/S_WIDTH)

        global first_click
        
        if first_click:
            board.initboard ((row, col))
            first_click = False

        if button == mouse.RIGHT:
            board.toggle_flag (row, col)
        
        elif board.isbomb (row, col):
            board.pressed_bomb ()
            on_gameover (False)
            gameover = True
        else:
            board.empty_space (row, col)
        
        if board.check_if_won():
            on_gameover (True)
            gameover = True

def draw ():
    board.draw()

pgzrun.go()