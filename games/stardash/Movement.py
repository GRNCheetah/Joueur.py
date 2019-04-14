#class Movement():

#    def __init__(self):
#        pass


class Movement:

    def __init__(self, p, g):
        self.player = p
        self.game = g


    def move(self):

        for ship in self.player.units:
            if ship.job.title == "miner":

                pass


    def moveMiner(self, shipNum, mineral, taken):
        """Gets passed a ship, the game and the player.

        Moves a Miner towards the nearest asteroid.
        """
        moves = self.player.units[shipNum].job.moves

        if (self._inv(shipNum) < self.player.units[shipNum].job.carry_limit) :
            minDist = self._distance(0, 0, self.game.size_x, self.game.size_y)

            asteroids = self.game.bodies
            minAst = asteroids[0]
            for astNum in range(4, len(asteroids)):
                if (asteroids[astNum].material_type == mineral):
                    dist = self._distance(self.player.units[shipNum].x, self.player.units[shipNum].y, asteroids[astNum].x, asteroids[astNum].y)
                    if dist < minDist:
                        minDist = dist
                        minAst = asteroids[astNum]
            '''currDist = minDist
            turns = 1 # to get to the asteroid
            nextX = minAst.next_x(turns)
            nextY = minAst.next_y(turns)
            nextDist = self._distance((self.player.units[shipNum].x + moves * turns) if (self.player.units[shipNum].x - nextX > 0) else (self.player.units[shipNum].x - moves * turns),
                                 (self.player.units[shipNum].y + moves * turns) if (self.player.units[shipNum].y - nextY > 0) else (self.player.units[shipNum].y - moves * turns),
                                 nextX,
                                 nextY)
            while nextDist < currDist:
                currDist = nextDist
                turns += 1
                nextX = minAst.next_x(turns)
                nextY = minAst.next_y(turns)
                nextDist = self._distance((self.player.units[shipNum].x + moves * turns) if (self.player.units[shipNum].x - nextX > 0) else (self.player.units[shipNum].x - moves * turns),
                                     (self.player.units[shipNum].y + moves * turns) if (self.player.units[shipNum].y - nextY > 0) else (self.player.units[shipNum].y - moves * turns),
                                     nextX,
                                     nextY)
            '''
            x, y = self._moveTo(self.player.units[shipNum].x, self.player.units[shipNum].y, minAst.x, minAst.y, moves)
            print(x, y)
            self.player.units[shipNum].move(self.player.units[shipNum].x + x , self.player.units[shipNum].y + y)
        else:
            x, y = self._moveTo(self.player.units[shipNum].x, self.player.units[shipNum].y, self.player.home_base.x, self.player.home_base.y, moves)
            self.player.units[shipNum].move(self.player.units[shipNum].x + x, self.player.units[shipNum].y + y)

    def _inv(self, shipNum):
        ship = self.player.units[shipNum]
        return ship.genarium + ship.legendarium + ship.mythicite + ship.rarium

    def _moveTo(self, shipX, shipY, tarX, tarY, move):
        """Returns the x and y speed to get to target x and y.

        This is to take care of the positives and negatives.
        """
        dist = self._distance(shipX, shipY, tarX, tarY) + .1
        max_move = move / (2 ** .5)

        x = move * ((tarX - shipX)/dist)
        y = move * ((tarY - shipY)/dist)

        if x > max_move:
            x = max_move
        elif x < (-1 * max_move):
            x = -1 * max_move

        if y > max_move:
            y = max_move
        elif y < (-1 * max_move):
            y = -1 * max_move

        return x, y

    def _distance(self, shipX, shipY, tarX, tarY):
        return ((shipX - tarX)**2 + (shipY - tarY)**2) ** .5








