import pgzrun
import math
import random
import minesweeper
from pgzero.builtins import Actor, mouse


TITLE = "minesweeper"

ROWS = 10
COLS = 10
S_WIDTH = 45

WIDTH = COLS * S_WIDTH
HEIGHT = ROWS * S_WIDTH
BOMBS = random.randrange (math.floor(ROWS * COLS/8), math.floor(ROWS * COLS/5))

board = minesweeper.Minesweeper (ROWS, COLS, BOMBS, S_WIDTH)

def on_gameover ():
    print ("failed")

def on_mouse_down (pos, button):
    row = math.floor(pos[1]/S_WIDTH)
    col = math.floor(pos[0]/S_WIDTH)

    if button == mouse.RIGHT:
        board.toggle_flag (row, col)
    
    elif board.isbomb (row, col):
        board.pressed_bomb ()
    else:
        board.empty_space (row, col)

def draw ():
    board.draw()

pgzrun.go()