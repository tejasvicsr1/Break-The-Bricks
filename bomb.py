from ball import *
import os
import time



class Bomb:

    def __init__(self, paddle, x, y, rows):
        self._paddle = paddle
        self._speedY = 1
        self._x = x
        self._isAlive = 1
        self._rows = rows
        self._y = y

    def move(self):

        check = self._rows - 2

        self._y += self._speedY

        if self._y == check:
            self._isAlive = 0

        plength = self._paddle.getPositionX() + self._paddle.getWidth()

        if self._y == self._paddle.getPositionY() and (self._x >= self._paddle.getPositionX() and self._x < plength):
            self._isAlive = 0
            return 1
        return 0

    def isAlive(self):
        return self._isAlive

    def create(self, grid):
        grid[self._y, self._x] = '+'
