import time
import os
from grid import *

class Ball:

    def __init__(self, rows, columns, paddle, bricks, x, y, start):
        self._paddle = paddle
        self._bricks = bricks
        self._speedX = 1
        self._x = x
        self._speedY = 1
        self._y = y
        self._lastChange = time.time()
        self._alive = 1
        self._isPresent = 1
        self._rows = rows
        self._thru = 0
        self._fire = 0
        self._grab = 0
        self._start = start
        self._columns = columns

    def changePosWithPaddle(self, text):
        left = ['a', 'A']
        right = ['d', 'D']
        if text in left:
            if self._x  <= 4:
                pass
            else:
                self._x = self._x - 1
        elif text in right:
            if  self._x >= self._columns-5:
                pass
            else:
                self._x = 1 + self._x

    def increaseSpeed(self, speed):
        self._speedX = int(self._speedX * speed)
        self._speedY = int(self._speedY * speed)

    def getPositionY(self):
        return self._y

    def createBall(self, grid):
        grid[self.getPosition()] = '*'

    def getPosition(self):
        return self._y, self._x

    def getPositionX(self):
        return self._x

    def makeThru(self):
        self._thru = 1
    
    def isPresent(self):
        return self._isPresent

    def removeThru(self):
        self._thru = 0

    def setSpeed(self, speedX, speedY):
        self._speedX = speedX
        self._speedY = speedY

    def changeSpeed(self, distance):
        mid = self._paddle.getWidth()//2
        if distance < mid:
            reduceby = mid - distance
            self._speedX -= reduceby
        elif distance == mid:
            pass
        else:
            increaseby = distance - mid
            self._speedX += increaseby

    def setStart(self, start):
        self._start = start

    def getStart(self):
        return self._start

    def grab(self):
        self._grab = 1

    def removeGrab(self):
        self._grab = 0

    def explode(self, k, i, j, fire):
        # There is a change here
        sx = self._speedX
        sy = self._speedY
        self._bricks[k][i][j].destroy(sx, sy)
        
        if self._bricks[k][i][j].isExploding() or fire == 1:
            t = i + 1
            l = j - 1
            b = i - 1
            r = j + 1
            if t < len(self._bricks[k]) and self._bricks[k][t][j].exists():
                self._bricks[k][t][j].destroy(sx, sy)
                self.explode(k, t, j, 0)

            if r < len(self._bricks[k][i]) and self._bricks[k][i][r].exists():
                self._bricks[k][i][r].destroy(sx, sy)
                self.explode(k, i, r, 0)

            if l >= 0 and self._bricks[k][i][l].exists():
                self._bricks[k][i][l].destroy(sx, sy)
                self.explode(k, i, l, 0)

            if b >= 0 and self._bricks[k][b][j].exists():
                self._bricks[k][b][j].destroy(sx, sy)
                self.explode(k, b, j, 0)

            if b >= 0 and l >= 0 and self._bricks[k][b][l].exists():
                self._bricks[k][b][l].destroy(sx, sy)
                self.explode(k, b, l, 0)

            if b >= 0 and r < len(self._bricks[k][i]) and self._bricks[k][b][r].exists():
                self._bricks[k][b][r].destroy(sx, sy)
                self.explode(k, b, r, 0)

            if t < len(self._bricks[k]) and l >= 0 and self._bricks[k][t][l].exists():
                self._bricks[k][t][l].destroy(sx, sy)
                self.explode(k, t, l, 0)

            if t < len(self._bricks[k]) and r < len(self._bricks[k][i]) and self._bricks[k][t][r].exists():
                self._bricks[k][t][r].destroy(sx, sy)
                self.explode(k, t, r, 0)

    def checkCollide(self):
        collided = 0
        ypos = self._y + self._speedY
        xpos = self._x + self._speedX
        if ypos <= 0 or ypos >= self._rows - 1:
            collided = 1

        if xpos <= 0 or xpos >= self._columns - 1:
            collided = 1

        paddlex = self._paddle.getPositionX()
        paddley = self._paddle.getPositionY()

        if self._y == paddley and self._x >= paddlex:
            paddlel = paddlex + self._paddle.getWidth()
            if self._x <= paddlel:
                collided = 1

        for k in range(len(self._bricks)):
            ydis = len(self._bricks[k])
            for i in range(0, ydis):
                xdis = len(self._bricks[k][i])
                for j in range(0, xdis):
                    if self._bricks[k][i][j].exists():
                        xpos = self._bricks[k][i][j].getPositionX()
                        ypos = self._bricks[k][i][j].getPositionY()
                        t = i + 1
                        l = j - 1
                        b = i - 1
                        r = j + 1
                        bricklen = len(self._bricks[k][i])
                        blocklen = len(self._bricks[k])
                        if self._x == xpos + 1 and self._y == ypos and self._speedX != 0:
                            collided = 1

                        elif self._x == xpos - 1 and self._y == ypos and self._speedX != 0:
                            collided  = 1

                        if self._x == xpos and self._y == ypos + 1:
                            collided = 1
                            
                        elif self._x == xpos and self._y == ypos - 1:
                            collided = 1

                        elif self._x == xpos + 1 and self._y == ypos + 1 and self._speedX < 0 and self._speedY < 0:
                            if (r >= bricklen or (r < bricklen and not(self._bricks[k][i][r].exists()))) and (t >= blocklen or (t < blocklen and not(self._bricks[k][t][j].exists()))):
                                collided = 1
                        
                        elif self._x == xpos + 1 and self._y == ypos - 1 and self._speedX < 0 and self._speedY > 0:
                            if (r >= bricklen or (r < bricklen and not(self._bricks[k][i][r].exists())) ) and (i == 0 or (b >= 0 and not(self._bricks[k][b][j].exists()))):
                                collided = 1
                        
                        elif self._x == xpos - 1 and self._y == ypos + 1 and self._speedX > 0 and self._speedY < 0:
                            if ((l >= 0 and not(self._bricks[k][i][l].exists())) or l<0) and ((t < blocklen and not(self._bricks[k][t][j].exists())) or t >= blocklen):
                                collided = 1

                        elif self._x == xpos - 1 and self._y == ypos - 1 and self._speedX > 0 and self._speedY > 0:
                            if ((l >= 0 and not(self._bricks[k][i][l].exists())) or l<0) and ((b >= 0 and not(self._bricks[k][b][j].exists())) or b < 0):
                                collided = 1
        return collided

    def collision(self):
        ypos = self._y + self._speedY
        xpos = self._x + self._speedX
        pxpos = self._paddle.getPositionX()
        pypos = self._paddle.getPositionY()
        powerup = None
        score = 0

        if ypos == 0:
            os.system('aplay -q music/Ice.wav &')
            self._speedY = self._speedY * -1

        if ypos >= self._rows-1:
            os.system('aplay -q music/Death.wav &')
            self._isPresent = 0

        if xpos == 0 or xpos == self._columns - 1:
            os.system('aplay -q music/Ice.wav &')
            self._speedX = self._speedX * -1

        if self._y == pypos - 1 and self._x >= pxpos and self._x <= pxpos + self._paddle.getWidth():
            newspeed = self._x - self._paddle.getPositionX()
            self.changeSpeed(newspeed)
            os.system('aplay -q music/Ice.wav &')
            self._speedY *= -1

            if self._grab == 1:
                ans = 0
                self.setStart(ans)
                return -1, powerup
            return 2, powerup
        
        for k in range(len(self._bricks)):
            ydis = len(self._bricks[k])
            for i in range(0, ydis):
                xdis = len(self._bricks[k][i])
                for j in range(0, xdis):
                    xval = self._bricks[k][i][j].getPositionX()
                    yval = self._bricks[k][i][j].getPositionY()
                    bricklen = len(self._bricks[k][i])
                    blocklen = len(self._bricks[k])
                    t = i + 1
                    b = i - 1
                    l = j - 1
                    r = j + 1
                    if self._bricks[k][i][j].exists():
                        flag = 0
                        if self._x == xval + 1 and self._y == yval and self._speedX != 0:
                            if self._thru:
                                flag = 1
                                scoreBrick, powerup = self._bricks[k][i][j].destroy(self._speedX, self._speedY)
                            else:
                                self._speedX *= -1
                                scoreBrick, powerup = self._bricks[k][i][j].reduceStrength(self._speedX, self._speedY)

                            flag = 1
                            score += scoreBrick

                        elif self._x == xval - 1 and self._y == yval and self._speedX != 0:
                            if self._thru:
                                flag = 1
                                scoreBrick, powerup = self._bricks[k][i][j].destroy(self._speedX, self._speedY)
                            else:
                                self._speedX *= -1
                                scoreBrick, powerup = self._bricks[k][i][j].reduceStrength(self._speedX, self._speedY)

                            flag = 1
                            score += scoreBrick

                        if self._x == xval and self._y == yval + 1:
                            if self._thru:
                                flag = 1
                                scoreBrick, powerup = self._bricks[k][i][j].destroy(self._speedX, self._speedY)
                            else:
                                self._speedY *= -1
                                scoreBrick, powerup = self._bricks[k][i][j].reduceStrength(self._speedX, self._speedY)

                            flag = 1
                            score += scoreBrick
                            
                        elif self._x == xval and self._y == yval - 1:
                            if self._thru:
                                flag = 1
                                scoreBrick, powerup = self._bricks[k][i][j].destroy(self._speedX, self._speedY)
                            else:
                                self._speedY *= -1
                                scoreBrick, powerup = self._bricks[k][i][j].reduceStrength(self._speedX, self._speedY)

                            flag = 1
                            score += scoreBrick

                        elif self._x == xval + 1 and self._y == yval + 1 and self._speedX < 0 and self._speedY < 0:
                            if (r >= bricklen or (r < bricklen and not(self._bricks[k][i][r].exists()))) and (t >= blocklen or (t < blocklen and not(self._bricks[k][t][j].exists()))):
                                if self._thru:
                                    flag = 1
                                    scoreBrick, powerup = self._bricks[k][i][j].destroy(self._speedX, self._speedY)
                                else:
                                    self._speedY *= -1
                                    self._speedX *= -1
                                    scoreBrick, powerup = self._bricks[k][i][j].reduceStrength(self._speedX, self._speedY)

                                flag = 1
                                score += scoreBrick
                        
                        elif self._x == xval + 1 and self._y == yval - 1 and self._speedX < 0 and self._speedY > 0:
                            if (r >= bricklen or (r < bricklen and not(self._bricks[k][i][r].exists())) ) and (i == 0 or (b >= 0 and not(self._bricks[k][b][j].exists()))):
                                if self._thru:
                                    flag = 1
                                    scoreBrick, powerup = self._bricks[k][i][j].destroy(self._speedX, self._speedY)
                                else:
                                    self._speedY *= -1
                                    self._speedX *= -1
                                    scoreBrick, powerup = self._bricks[k][i][j].reduceStrength(self._speedX, self._speedY)

                                flag = 1
                                score += scoreBrick
                        
                        elif self._x == xval - 1 and self._y == yval + 1 and self._speedX > 0 and self._speedY < 0:
                            if ((l >= 0 and not(self._bricks[k][i][l].exists())) or l<0) and ((t < blocklen and not(self._bricks[k][t][j].exists())) or t >= blocklen):
                                if self._thru:
                                    flag = 1
                                    scoreBrick, powerup = self._bricks[k][i][j].destroy(self._speedX, self._speedY)
                                else:
                                    self._speedY *= -1
                                    self._speedX *= -1
                                    scoreBrick, powerup = self._bricks[k][i][j].reduceStrength(self._speedX, self._speedY)

                                flag = 1
                                score += scoreBrick

                        elif self._x == xval - 1 and self._y == yval - 1 and self._speedX > 0 and self._speedY > 0:
                            if ((l >= 0 and not(self._bricks[k][i][l].exists())) or l<0) and ((b >= 0 and not(self._bricks[k][b][j].exists())) or b < 0):
                                if self._thru:
                                    flag = 1
                                    scoreBrick, powerup = self._bricks[k][i][j].destroy(self._speedX, self._speedY)
                                else:
                                    self._speedY *= -1
                                    self._speedX *= -1
                                    scoreBrick, powerup = self._bricks[k][i][j].reduceStrength(self._speedX, self._speedY)

                                flag = 1
                                score += scoreBrick

                        if self._bricks[k][i][j].isExploding() or self._fire:
                            if flag == 1:
                                os.system('aplay -q music/Explosion.wav &')
                                self.explode(k, i, j, self._fire)

                        if flag:
                            os.system('aplay -q ./music/Ice.wav &')

        return score, powerup

    def changePosition(self, text):
        ypos = self._y + self._speedY
        xpos = self._x + self._speedX
        if ypos < 0 or xpos < 0 or xpos > self._columns - 1:
            if xpos < 0:
                self._x = 1
                self._y += self._speedY//2
                self._speedX *= -1

            if xpos > self._columns - 1:
                self._x = self._columns - 2
                self._y += self._speedY//2
                self._speedX *= -1

            if ypos < 0:
                self._y = 1
                self._x += self._speedX//2
                self._speedY *= -1

            if ypos > self._rows - 1:
                os.system('aplay -q music/Death.wav &')
                self._isPresent = 0

        else:
                
            if self._start == 0:
                pass
            else:
                values = abs(self._speedX) * abs(self._speedY)
                result, powerup = self.collision()

            if result == 2:
                self._x = self._speedX + self._x
                self._y = self._speedY + self._y
                return result, powerup

            if values <= 1:
                self._x = self._speedX + self._x 
                self._y = self._speedY + self._y
                return result, powerup
            elif abs(self._speedX) > 1:
                    speedlen = abs(self._speedX)
                    self._y += self._speedY
                    for i in range(0, speedlen):
                        val = i + 1
                        self._x += val if self._speedX > 0 else -1 * val
                        if self.checkCollide():
                            break
                    return result, powerup
        return 0, None

    def fire(self):
        self._fire = 1
    
    def removeFire(self):
        self._fire = 0
    
    def setLastChange(self, time):
        self._lastChange = time

    def getLastChange(self):
        return self._lastChange