import time
from ball import *

class PowerUp:

    def __init__(self, rows, columns, x, y, speedX, speedY):
        self._matrix = 'P'
        self._rows = rows
        self._executed = 0
        self._columns = columns
        self._speedY = speedY
        self._isActive = 1
        self._speedX = speedX
        self._speedY = 1
        self._x = x
        self._lastChange = time.time()
        self._y = y
        self._exists = 1
        self._createTime = time.time()

    def checkPaddleCollision(self, paddle):
        if self._x >= paddle.getPositionX():
            if self._x < paddle.getPositionX() + paddle.getWidth(): 
                if (self._y == paddle.getPositionY()):
                    self._exists = 0
                    return 1
        else:
            return 0

    def remove(self):
        self._isActive = 0
    
    def getPowerUp(self):
        pass

    def isActive(self):
        return self._isActive

    def setLastChange(self, time):
        self._lastChange = time

    def move(self):
        ypos = self._y + self._speedY
        if ypos == 0:
            self._speedY *= -1

        if ypos >= self._rows-1:
            self._exists = 0
        
        xpos = self._x + self._speedX

        if xpos <= 0 or xpos >= self._columns - 1:
            self._speedX = self._speedX * -1

        self._x = self._speedX + self._x
        self._y = self._speedY + self._y

    def executed(self):
        self._executed = 1
    
    def isExecuted(self):
        return self._executed

    def getCreateTime(self):
        return self._createTime

    def getLastChange(self):
        return self._lastChange

    def createPowerup(self, grid):
        if not self._exists:
            pass
        else:
            grid[self._y, self._x] = self._matrix
    
class Shrink(PowerUp):

    def __init__(self, rows, columns, x, y, speedX, speedY):
        text = "S"
        super().__init__(rows, columns, x, y, speedX, speedY)
        self._matrix = text

    def getPowerUp(self):
        text = "shrink"
        return text

class Multiply(PowerUp):

    def __init__(self, rows, columns, x, y, speedX, speedY):
        text = "M"
        super().__init__(rows, columns, x, y, speedX, speedY)
        self._matrix = text

    def getPowerUp(self):
        text = "multiply"
        return text

class Fast(PowerUp):

    def __init__(self, rows, columns, x, y, speedX, speedY):
        text = "F"
        super().__init__(rows, columns, x, y, speedX, speedY)
        self._matrix = text

    def getPowerUp(self):
        text = "fast"
        return text

class Grab(PowerUp):

    def __init__(self, rows, columns, x, y, speedX, speedY):
        text = "G"
        super().__init__(rows, columns, x, y, speedX, speedY)
        self._matrix = text

    def getPowerUp(self):
        text = "grab"
        return text

class Thru(PowerUp):
    
    def __init__(self, rows, columns, x, y, speedX, speedY):
        text = "T"
        super().__init__(rows, columns, x, y, speedX, speedY)
        # Example of polymorphism
        self._matrix = text

    def getPowerUp(self):
        text = "thru"
        return text


class Expand(PowerUp):
    
    def __init__(self, rows, columns, x, y, speedX, speedY):
        text = "E"
        super().__init__(rows, columns, x, y, speedX, speedY)
        self._matrix = text

    def getPowerUp(self):
        text = "expand"
        return text

class Fireball(PowerUp):
    
    def __init__(self, rows, columns, x, y, speedX, speedY):
        text = 'B'
        super().__init__(rows, columns, x, y, speedX, speedY)
        self._matrix = text

    def getPowerUp(self):
        text = 'fireball'
        return text

class Laser(PowerUp):

    def __init__(self, rows, columns, x, y, speedX, speedY):
        text = 'L'
        super().__init__(rows, columns, x, y, speedX, speedY)
        self._matrix = text

    def getPowerUp(self):
        text = 'laser'
        return text