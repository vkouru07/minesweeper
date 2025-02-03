import pgzrun
import math
import random
import minesweeper
import os 

# import tkinter
# from tkinter import messagebox
from pgzero.builtins import Actor, mouse
from pgzero import screen
import oth  

import database 

os.environ['SDL_VIDEO_CENTERED'] = '1'

TITLE = "minesweeper"

ROWS = 18
COLS = 28
S_WIDTH = 45

WIDTH = COLS * S_WIDTH
HEIGHT = ROWS * S_WIDTH
BOMBS = random.randrange (math.floor(ROWS * COLS/8), math.floor(ROWS * COLS/5))

board = minesweeper.Minesweeper (ROWS, COLS, BOMBS, S_WIDTH)
first_click = True

gamestate = 0 # 0: running, 1: win, 2:lost 
game_score = 0 

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
        
        elif not board.isflagged (row, col) and board.isbomb (row, col):
            board.pressed_bomb ()
            gamestate = 2
            return
        else:
            board.empty_space (row, col)
        
        board.draw ()
        if board.check_if_won():
            gamestate = 1

    elif again.collidepoint (pos):
        gamestate = 0
        first_click = True
        board = minesweeper.Minesweeper (ROWS, COLS, BOMBS, S_WIDTH)


def draw ():
    board.draw ()
    if gamestate != 0:
        if gamestate == 1:
            win.draw()
        elif gamestate == 2:
            # database.save_high_score ("test2", 2)
            lost.draw()
        
        with database.HighScoreManager() as highscore_manager:
            if highscore_manager.insert_score('', game_score + 1):  # Pass an empty name initially
                # If it's a new high score, ask for the player's name
                player_name = input("Congratulations! You made a new high score! Enter your name: ")
                # Update the high score with the player's name
                highscore_manager.insert_score(player_name, game_score)
        again.draw ()

pgzrun.go()

print (database.load_high_scores()) 