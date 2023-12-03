import pgzrun
import math
import random
import minesweeper

# import tkinter
# from tkinter import messagebox
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

gamestate = 0 # 0: running, 1: win, 2:lost 

win = Actor ("win")
win.pos = WIDTH/2, HEIGHT/2
lost = Actor ("lost")
lost.pos = WIDTH/2, HEIGHT/2
again = Actor ("again")
again.pos = WIDTH/2, HEIGHT * 2/3

def on_mouse_down (pos, button):
    global gamestate
    global first_click
    global board

    if gamestate == 0:
        row = math.floor(pos[1]/S_WIDTH)
        col = math.floor(pos[0]/S_WIDTH)
        
        if first_click:
            board.initboard ((row, col))
            first_click = False

        if button == mouse.RIGHT:
            board.toggle_flag (row, col)
        
        elif board.isbomb (row, col):
            board.pressed_bomb ()
            gamestate = 2
            return
        else:
            board.empty_space (row, col)
        
        if board.check_if_won():
            gamestate = 1
    elif again.collidepoint (pos):
        gamestate = 0
        first_click = True
        board = minesweeper.Minesweeper (ROWS, COLS, BOMBS, S_WIDTH)


def draw ():
    if gamestate == 0:
        board.draw ()
    else:
        if gamestate == 1:
            win.draw()
        elif gamestate == 2:
            lost.draw()
        again.draw ()

pgzrun.go()