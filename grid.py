from hashlib import new
from colorama import init, Back
init()
import numpy
import time
import os
from ball import *
from paddle import *
from brick import *

class Grid:

    def __init__(self, rows, columns):
        self._bricks = []
        self._columns = columns
        self._rows = rows
        self._paddle = Paddle(rows, columns)
        self._matrix = numpy.full((self._columns, self._rows), ' ', dtype='<U20')
        for k in range(0, 3):
            self._bricks.append([])
            ydis = 5
            for i in range(0, ydis):
                self._bricks[k].append([])
                xdis = 15
                for j in range(0, xdis):
                    if i==0 or i==2 or j==0 or j==14:
                        temp = Strength1(self._rows, self._columns)
                        self._bricks[k][i].append(temp)
                    elif i==1 or i==3 or j==1 or j==13:
                        temp = Strength2(self._rows, self._columns)
                        self._bricks[k][i].append(temp)
                    elif i==4 and k==0:
                        temp = Strength3(self._rows, self._columns)
                        self._bricks[k][i].append(temp)
                    elif i==4 and k==1:
                        temp = StrengthInf(self._rows, self._columns)
                        self._bricks[k][i].append(temp)
                    elif i==4 and k==2:
                        temp = StrengthExp(self._rows, self._columns)
                        self._bricks[k][i].append(temp)

        self._time = time.time()
        self._score = 0
        self._levelTime = time.time()
        self._gameOn = 1
        self._powerups = []
        self._lives = 3
        paddlewidth = self._paddle.getPositionX() + int(self._paddle.getWidth()/2)
        paddleheight = self._paddle.getPositionY() - 1
        self._balls = [Ball(rows, columns, self._paddle, self._bricks, paddlewidth, paddleheight, 0)]
        self._level = 1
        # self._lastChangesPowerUp = []
        # self._lastChanges = [time.time()]

        for k in range(len(self._bricks)):
            ydis = len(self._bricks[k])
            for i in range(ydis):
                xdis = len(self._bricks[k][i])
                for j in range(xdis):
                    if(self._bricks[k][i][j].exists()):
                        atemp = j + 10 + k * 22
                        btemp = j + 10 + k * 35
                        ctemp = j + 30
                        value = 5 + i
                        if self._level == 1:
                            self._bricks[k][i][j].setPosition(
                                atemp, value)
                        elif self._level == 2:
                            self._bricks[k][i][j].setPosition(
                                btemp, value)
                        elif self._level == 3:
                            self._bricks[k][i][j].setPosition(
                                ctemp, 5+i)

    def createBox(self):
        plus = "+"
        self._matrix[0:self._rows-1, self._columns-1] = '+'
        self._matrix[0:self._rows-1, 0] = '+'
        cross = "x"
        self._matrix[0, 0:self._columns] = '+'
        self._matrix[self._rows-1, 0:self._columns] = '+'
    
    def gameOn(self):
        return self._gameOn

    def createBricks(self):
        for k in range(len(self._bricks)):
            ydis = len(self._bricks[k])
            for i in range(0, ydis):
                xdis = len(self._bricks[k][i])
                for j in range(0, xdis):
                    if(self._bricks[k][i][j].exists()):
                        atemp = j + 10 + k * 22
                        btemp = 5 + i
                        # self._bricks[k][i][j].setPosition(atemp, btemp)
                        self._bricks[k][i][j].createBrick(self._matrix)

    def score(self):
        return self._score

    def time(self):
        return self._time

    def shiftBricks(self):
        changetime = time.time() - self._levelTime
        if changetime > 10:
            # os.system('clear')
            for k in range(len(self._bricks)):
                ydis = len(self._bricks[k])
                for i in range(ydis):
                    xdis = len(self._bricks[k][i])
                    for j in range(xdis):
                        if(self._bricks[k][i][j].exists()):
                            xpos = self._bricks[k][i][j].getPositionX()
                            if self._level == 1 or self._level == 2:
                                ypos = self._bricks[k][i][j].getPositionY() + 1
                                if(self._bricks[k][i][j].getPositionY() + 1) == 25:
                                    os.system('aplay -q music/Lose.wav &')
                                    self._gameOn = 0
                                self._bricks[k][i][j].setPosition(xpos, ypos)
                                self._bricks[k][i][j].createBrick(self._matrix)

    def applyPowerup(self, powerup):
        width = 2
        power = powerup.getPowerUp()
        if power == 'expand':
            self._paddle.changeWidth(width)
        elif power == 'shrink':
            self._paddle.changeWidth(-1 * width)
        elif power == 'laser':
            self._laserStartTime = time.time()
            self._paddle.laser()
            self._laser = 1
        elif power == 'multiply':
            numballs = len(self._balls)
            for i in range(0, numballs):
                if self._balls[i].isPresent():
                    timeofball = time.time()
                    # self._lastChanges.append(timeofball)
                    ballposx = self._balls[i].getPositionX()
                    ballposy = self._balls[i].getPositionY()
                    self._balls.append(Ball(self._rows, self._columns, self._paddle, self._bricks, ballposx, ballposy, 1))
        elif power == 'thru':
            numballs = len(self._balls)
            for i in range(0, numballs):
                self._balls[i].makeThru()
        elif power == 'fast':
            numballs = len(self._balls)
            for i in range(0, numballs):
                self._balls[i].increaseSpeed(2)
        elif power == 'grab':
            numballs = len(self._balls)
            for i in range(0, numballs):
                self._balls[i].grab()
        elif power == 'fireball':
            numballs = len(self._balls)
            for i in range(numballs):
                self._balls[i].fire()

    def removePowerup(self, powerup):
        width = 2
        power = powerup.getPowerUp()
        if power == 'expand':
            self._paddle.changeWidth(-1 * width)
        elif power == 'shrink':
            self._paddle.changeWidth(width)
        elif power == 'fast':
            numballs = len(self._balls)
            for i in range(0, numballs):
                self._balls[i].increaseSpeed(0.5)
        elif power == 'fireball':
            numballs = len(self._balls)
            for i in range(numballs):
                self._balls[i].removeFire()
        elif power == 'laser':
            numballs = len(self._balls)
            for i in range(numballs):
                self._paddle.removeLaser()
        elif power == 'thru':
            numballs = len(self._balls)
            for i in range(0, numballs):
                self._balls[i].removeThru()
        elif power == 'grab':
            numballs = len(self._balls)
            for i in range(0, numballs):
                self._balls[i].removeGrab()
        
    def lives(self):
        return self._lives

    def addBall(self):
        temp = Ball(self._rows, self._columns, self._paddle, self._bricks)
        self._balls.append(temp)

    def level(self):
        return self._level

    def printView(self, text):
        
        numballs = len(self._balls)
        self._matrix = numpy.full((self._rows, self._columns), ' ', dtype='<U20')

        level_changer = ['n', 'N']

        if text in level_changer:
            self._levelTime = time.time()
            self._level += 1
            newlevel = self._level
            if newlevel > 1 and newlevel < 4:
                if newlevel == 2:
                    blocks = 2
                elif newlevel == 3:
                    blocks = 1
                self._bricks = []
                for k in range(0, blocks):
                    self._bricks.append([])
                    for i in range(0, 5):
                        self._bricks[k].append([])
                        for j in range(0, 20):
                            if i == 0 or i == 2 or j == 0 or j == 19:
                                temp = Strength1(self._rows, self._columns)
                                self._bricks[k][i].append(temp)
                            elif i == 1 or i == 3 or j == 1 or j == 18:
                                temp = Strength2(self._rows, self._columns)
                                self._bricks[k][i].append(temp)
                            elif i == 4 and k == 0:
                                temp = Strength3(self._rows, self._columns)
                                self._bricks[k][i].append(temp)
                            elif i == 4 and k == 1:
                                temp = StrengthInf(self._rows, self._columns)
                                self._bricks[k][i].append(temp)
                for k in range(len(self._bricks)):
                    ydis = len(self._bricks[k])
                    for i in range(ydis):
                        xdis = len(self._bricks[k][i])
                        for j in range(ydis):
                            if(self._bricks[k][i][j].exists()):
                                value = 5 + i
                                atemp = j + 10 + k * 35
                                btemp = j + 30
                                if self._level == 2:
                                    self._bricks[k][i][j].setPosition(atemp, value)
                                elif self._level == 3:
                                    self._bricks[k][i][j].setPosition(btemp, value)

            if self._level == 4:
                os.system('aplay -q music/Lose.wav &')
                self._gameOn = 0
            self._powerups = []
            pwidth = self._paddle.getPositionY() - 1
            # self._lastChangesPowerUp = []
            self._paddle = Paddle(self._rows, self._columns)
            plength = self._paddle.getPositionX() + int(self._paddle.getWidth()/2)
            self._balls = [Ball(self._rows, self._columns, self._paddle, self._bricks, plength, pwidth, 0)]
        
        self._paddle.changePosition(text)
        self.createBricks()
        
        for i in range(0, numballs):
            if self._balls[i].isPresent():
                temp = self._matrix
                self._balls[i].createBall(temp)
                starter = 1
                if self._balls[i].getStart() == 0:
                    if text == 'A' or text == 'D' or text == 'a' or text == 'd':
                        self._balls[i].changePosWithPaddle(text)
                    elif text == ' ':
                        print(self._balls[i].getPosition())
                        self._balls[i].setStart(starter)
                        self._balls[i].changePosition(text)
                else:
                    timecheck = int((time.time() - self._balls[i].getLastChange())/0.1)
                    if timecheck > 0:
                        
                        score, powerup = self._balls[i].changePosition(text)

                        if score != 2:
                            self._score += score
                        else:
                            self.shiftBricks()

                        self._balls[i].setLastChange(time.time())

                        if powerup != None:
                            temp = powerup
                            timer = time.time()
                            self._powerups.append(temp)
                        #     self._lastChangesPowerUp.append(timer)
                        # self._score = score + self._score
                        # self._lastChanges[i] = time.time()

        ballsPresent = 0
        sol = 1
        numballs = len(self._balls)
        for i in range(0, numballs):
            if self._balls[i].isPresent():
                ballsPresent = sol
        
        if ballsPresent == 0:
            self._lives = self._lives - 1

            if self._lives == 0:
                os.system('aplay -q music/Lose.wav &')
                self._gameOn = 0

            else:
                self._paddle = Paddle(self._rows, self._columns)
                self._powerups = []
                paddlelength = self._paddle.getPositionX() + int(self._paddle.getWidth()/2)
                paddleheight = self._paddle.getPositionY() - 1
                self._balls = [Ball(self._rows, self._columns, self._paddle, self._bricks, paddlelength, paddleheight, 0)]
                # self._lastChanges = [time.time()]
                # self._lastChangesPowerUp = []
    
        temp = self._matrix
        self._paddle.createPaddle(temp)
        numpowerups = len(self._powerups)

        for i in range(0, numpowerups):
            if self._powerups[i].isActive():
                temp = self._matrix
                self._powerups[i].createPowerup(temp)
                timecheck = int((time.time() - self._powerups[i].getLastChange())/0.1)

                if timecheck > 0:
                    timer = time.time()
                    addtimecheck = timer - self._powerups[i].getCreateTime()
                    self._powerups[i].setLastChange(timer)
                    self._powerups[i].move()
                    check = self._powerups[i].isExecuted()
                    if self._powerups[i].checkPaddleCollision(self._paddle) and check == 0:
                        self.applyPowerup(self._powerups[i])
                        os.system('aplay -q music/Powerup.wav &')
                        self._powerups[i].executed()
                    elif addtimecheck  > 10 and self._powerups[i].isExecuted():
                        poweruptoberemoved = self._powerups[i]
                        self.removePowerup(poweruptoberemoved)
                        self._powerups[i].remove()
            
        playingtime = int(time.time() - self._time)   
        self.createBox()
        
        print('Lives:', self._lives)
        print('Time Played: ' +  str(playingtime) + ' secs')
        print('Level:', self._level)
        print('Score: ' +  str(self._score))

        rowlen = self._rows
        for i in range(0, rowlen):
            collen = self._columns
            for j in range(0, collen):
                print(self._matrix[i, j], end = '')
            print()