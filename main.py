import pgzrun
from minesweeper import *

gameover = False

# WIDTH = 1000
# HEIGHT = 900

def get_turn ():
    r = int(input ("row (starting from 0) "))
    c = int(input ("col (starting from 0) "))
    f1 = input ("are you toggling a flag? (y/n) ")
    f = True
    if "n" in f1:
        f = False
    
    return [r, c, f]
    

# def on_mouse_move (pos: tuple):
#     pass

# def update (delta_time: float):
#     pass

# def draw ():
#     pass


board = Board(4, 6)

while not gameover:
    print (board)
    move = get_turn()
    gameover = not board.turn(move[0], move[1], move[2])

board.setall_visible()
print (board)
print ("done")
# pgzrun.go()
