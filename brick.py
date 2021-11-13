from colorama import Fore, Back, Style
import random
import time
from powerup import *

class Brick:

    """Class for all the bricks"""
    def __init__(self, rows, columns):
        self._rows = rows
        self._x = 10
        self._hasPowerUp = random.randint(1, 10)
        self._matrix = Fore.RED + "#" + Fore.RESET
        self._exists = 1
        self._y = 15
        self._strength = 1
        self._isExploding = 0
        self._columns = columns

    def getPositionY(self):
        return self._y

    def isExploding(self):
        return self._isExploding

    """Reduce strength of brick after collision"""
    def reduceStrength(self, speedX, speedY):
        
        if self._strength == 1:
            powerup = None
            self._strength = 0
            self._exists = 0
            if self._hasPowerUp >= 1 and self._hasPowerUp <= 5:
                # powerup = random.choice([Laser])(self._rows, self._columns, self._x, self._y, speedX, speedY)
                powerup = random.choice([Expand, Shrink, Multiply, Fast, Thru, Grab, Fireball, Laser])(self._rows, self._columns, self._x, self._y, speedX, speedY)
            score = 10
            return score, powerup
            
        if self._exists:
            self._strength = self._strength - 1
            ans = self._strength
            if ans == 2:
                self._matrix = Fore.GREEN + "#" + Fore.RESET
            elif ans == 2:
                self._matrix = Fore.RED + "#" + Fore.RESET
            return 10, None
        return 0, None

    def getPositionX(self):
        return self._x

    def exists(self):
        return self._exists

    """Destroy bricks if near explosive bricks"""
    def destroy(self, speedX, speedY):
        self._exists = 0
        ans = self._hasPowerUp
        if ans >= 1 and ans <= 5:
            powerup = random.choice([Expand, Shrink, Multiply, Fast, Thru, Grab, Laser])(self._rows, self._columns, self._x, self._y, speedX, speedY)
            score = 10
            return score, powerup
        return 0, None

    def setPosition(self, x, y):
        self._x = x
        self._y = y

    def createBrick(self, grid):
        grid[self._y, self._x] = self._matrix

    
    """Differents Strength bricks"""
class Strength1(Brick):
    def __init__(self, rows, columns):
        self._hasPowerUp = random.randint(1,10)
        self._columns = columns
        self._strength = 1
        self._exists = 1
        self._rows = rows
        self._isExploding = 0
        self._matrix = Fore.RED + "#" + Fore.RESET

class Strength2(Brick):
    def __init__(self, rows, columns):
        self._hasPowerUp = random.randint(1,10)
        self._columns = columns
        self._strength = 2
        self._exists = 1
        self._rows = rows
        self._isExploding = 0
        self._matrix = Fore.GREEN + "#" + Fore.RESET

class Strength3(Brick):
    def __init__(self, rows, columns):
        self._hasPowerUp = random.randint(1,10)
        self._columns = columns
        self._strength = 3
        self._exists = 1
        self._rows = rows
        self._isExploding = 0
        self._matrix = Fore.YELLOW + "#" + Fore.RESET

class StrengthInf(Brick):
    def __init__(self, rows, columns):
        self._hasPowerUp = random.randint(1,10)
        self._columns = columns
        self._strength = 99999999
        self._exists = 1
        self._rows = rows
        self._isExploding = 0
        self._matrix = Fore.BLACK + "#" + Fore.RESET

class StrengthExp(Brick):
    def __init__(self, rows, columns):
        self._hasPowerUp = random.randint(1,10)
        self._columns = columns
        self._strength = 1
        self._exists = 1
        self._rows = rows
        self._isExploding = 1
        self._matrix = Fore.CYAN + "#" + Fore.RESET

class Rainbow(Brick):
    def __init__(self, rows, columns):
        self._hasPowerUp = random.randint(1, 10)
        self._exists = 1
        self._rows = rows
        self._isExploding = 0
        self._columns = columns