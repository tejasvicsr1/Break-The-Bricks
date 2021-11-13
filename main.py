import os
import time
from grid import *
from ball import *
from input import *
from art import *

rows, columns = os.popen('stty size', 'r').read().split()
os.system('clear')
# columns = int(columns)
# rows = int(rows)

# N to change level
# Bricks fall
# Fireball powerup
# Laser powerup
# 

if int(rows)<31:
    gridObj = Grid(20, 61)
else:
    gridObj = Grid(30, 81)

if int(columns) >= 102:
    gridObj = Grid(30, 81)
else:
    gridObj = Grid(20, 61)

# print(gridObj.gameOn())

isplaying = 0

while gridObj.gameOn() == 1:
    if isplaying == 0:
        os.system("clear")
        print(text2art("Break The Bricks"))
        print(text2art("Rules:", font="cybermedium"))
        print("1. Press p to play the game.")
        print("2. Press q to quit the game.")
        print("3. Use a and d to move the paddle left and right respectively.")
        print("4. Press the spacebar to release the ball.")
        print("5. Press q to quit the game.")
        print("6. Break maximum bricks to earn points.")
        print("7. Do not let the ball hit the ground.")
        firsttext = input_to()
        if (firsttext == "p" or firsttext == "P"):
            isplaying = 1
            
        if (firsttext == "q" or firsttext == "Q"):
            break
    else:
        print("*"*81)
        text = input_to()
        if(text == 'q' or text == "Q"):
            break
        else:
            os.system('clear')
            gridObj.printView(text)
        
    
os.system('clear')
if isplaying == 1:
    print(text2art("Game Over"))
    print(text2art("Thanks for playing.", font="cybermedium"))
    print('You played for ' +  str(int(time.time() - gridObj.time())) + ' secs')
    print('You had ' + str(gridObj.lives()) + " lives left.")
    print('You reached level ' + str(gridObj.level()))
    print('Your score was ' + str(gridObj.score()) + " points.")
else:
    print(text2art("Please play the game."))




