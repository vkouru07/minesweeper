import pgzrun
from minesweeper import *
from goo import *

gameover = False

WIDTH = 1000
HEIGHT = 900

def on_mouse_down (pos):
    pass

def update (delta_time: float):
    pass

def draw ():
    pass

board = Board(4, 6)
goop = Goo (board, 0, 0)

pgzrun.go()

# while not gameover:
#     print (board)
#     move = get_turn()
#     gameover = not board.turn(move[0], move[1], move[2])

# board.setall_visible()
# print (board)
# print ("done")
