import os


class Laser:

    """Class for all the Lasers."""

    def __init__(self, bricks, x, y):
        self._bricks = bricks
        self._speedY = -1
        self._x = x
        self._isAlive = 1
        self._y = y

    def create(self, grid):
        grid[self._y, self._x] = '*'

    def move(self):
        self._y += self._speedY

        flag = 1

        if self._y == 1:
            self._isAlive = 0

        numbricks = len(self._bricks)
        for k in range(numbricks):
            ydis = len(self._bricks[k])
            for i in range(ydis):
                xdis = len(self._bricks[k][i])
                for j in range(xdis):
                    if self._bricks[k][i][j].exists():
                        xpos = self._bricks[k][i][j].getPositionX()
                        ypos = self._bricks[k][i][j].getPositionY() + 1
                        if self._x == xpos and self._y == ypos:
                            flag = 1
                            scoreBrick, powerup = self._bricks[k][i][j].reduceStrength(0, self._speedY)
                            self._isAlive = 0
                            os.system('aplay -q music/Ice.wav &')
                            if self._bricks[k][i][j].isExploding():
                                self.explode(k, i, j, 1)
                                os.system('aplay -q music/Explosion.wav &')
                            return scoreBrick, powerup
        return 0, None

    def explode(self, k, i, j, fire):
        a = i + 1
        b = j + 1
        self._bricks[k][i][j].destroy(0, self._speedY)
        c = i - 1
        d = j - 1
        if self._bricks[k][i][j].isExploding() or fire == 1:
            if a < len(self._bricks[k]) and self._bricks[k][a][j].exists():
                self._bricks[k][a][j].destroy(0, self._speedY)
                self.explode(k, a, j, 0)

            if b < len(self._bricks[k][i]) and self._bricks[k][i][b].exists():
                self._bricks[k][i][b].destroy(0, self._speedY)
                self.explode(k, i, b, 0)

            if d >= 0 and self._bricks[k][i][d].exists():
                self._bricks[k][i][d].destroy(0, self._speedY)
                self.explode(k, i, d, 0)

            if c >= 0 and self._bricks[k][c][j].exists():
                self._bricks[k][c][j].destroy(0, self._speedY)
                self.explode(k, c, j, 0)

            if c >= 0 and d >= 0 and self._bricks[k][c][d].exists():
                self._bricks[k][c][d].destroy(0, self._speedY)
                self.explode(k, c, c, 0)

            if c >= 0 and b < len(self._bricks[k][i]) and self._bricks[k][c][b].exists():
                self._bricks[k][c][b].destroy(0, self._speedY)
                self.explode(k, c, b, 0)

            if a < len(self._bricks[k]) and d >= 0 and self._bricks[k][a][d].exists():
                self._bricks[k][a][d].destroy(0, self._speedY)
                self.explode(k, a, d, 0)

            if a < len(self._bricks[k]) and b < len(self._bricks[k][i]) and self._bricks[k][a][b].exists():
                self._bricks[k][a][b].destroy(0, self._speedY)
                self.explode(k, a, b, 0)

    def isAlive(self):
        return self._isAlive