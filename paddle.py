import numpy
from ball import *
from colorama import Fore, Back, Style

class Paddle:
    def __init__(self, rows, columns):
        self._y = 25
        self._columns = columns
        self._speedX = 2
        self._width = 7
        self._laser = 0
        self._rows = rows
        self._x = 40

    def getPositionX(self):
        return self._x

    def changePosition(self, text):
        if text == 'a' or text == 'A':
            if self._x  > 1:
                self._x -= self._speedX
            else:
                pass
        elif text == 'd' or text == 'D':
            if  self._x + self._width < self._columns-1:
                self._x += self._speedX
            else:
                pass

    def changeWidth(self, width):
        if self._width + width >= 3:
            self._width += width

    def getPositionY(self):
        return self._y

    def createPaddle(self, grid):
        look = Back.BLACK + "=" + Back.RESET
        grid[self._y, self._x:self._x + self._width] = look
        if self._laser:
            grid[self._y - 1, self._x + self._width - 1] = "^"
            grid[self._y - 1, self._x] = "^"

    def getWidth(self):
        return self._width

    def laser(self):
        self._laser = 1