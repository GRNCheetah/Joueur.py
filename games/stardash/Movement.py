#class Movement():

#    def __init__(self):
#        pass


class Movement:

    def __init__(self, p, g):
        self.player = p
        self.game = g

        self.taken = [] # The taken asteroids


    def move(self):

        for ship in self.player.units:
            if ship.job.title == "miner":
                self.moveMiner(ship, "genarium")

    def moveMiner(self, ship, mineral):
        """Gets passed a ship, the game and the player.

        Moves a Miner towards the nearest asteroid.
        """
        moves = ship.job.moves

        if not ship.acted:
            if (self._inv(ship) < ship.job.carry_limit):
                minDist = self._distance(0, 0, self.game.size_x, self.game.size_y)

                # Finds the closest asteroid and puts it in minAst
                asteroids = self.game.bodies
                minAst = asteroids[0]
                for astNum in range(4, len(asteroids)):
                    if (asteroids[astNum].material_type == mineral):
                        dist = self._distance(ship.x, ship.y, asteroids[astNum].x, asteroids[astNum].y)
                        if dist < minDist:
                            minDist = dist
                            minAst = asteroids[astNum]

                '''currDist = minDist
                turns = 1 # to get to the asteroid
                nextX = minAst.next_x(turns)
                nextY = minAst.next_y(turns)
                nextDist = self._distance((ship.x + moves * turns) if (ship.x - nextX > 0) else (ship.x - moves * turns),
                                     (ship.y + moves * turns) if (ship.y - nextY > 0) else (ship.y - moves * turns),
                                     nextX,
                                     nextY)
                while nextDist < currDist:
                    currDist = nextDist
                    turns += 1
                    nextX = minAst.next_x(turns)
                    nextY = minAst.next_y(turns)
                    nextDist = self._distance((ship.x + moves * turns) if (ship.x - nextX > 0) else (ship.x - moves * turns),
                                         (ship.y + moves * turns) if (ship.y - nextY > 0) else (ship.y - moves * turns),
                                         nextX,
                                         nextY)'''

                x, y = self._moveTo(ship.x, ship.y, minAst.x, minAst.y, moves)
                print(x, y)
                ship.move(ship.x + x, ship.y + y)
                if ship.energy > (ship.job.energy * .8) and self._distance(ship.x, ship.y, minAst.x, minAst.y) >= 25:
                    x, y = self._moveTo(ship.x, ship.y, minAst.x, minAst.y, moves)
                    ship.dash(ship.x + x, ship.y + y)
            else:
                x, y = self._moveTo(ship.x, ship.y, self.player.home_base.x, self.player.home_base.y, moves)
                ship.move(ship.x + x, ship.y + y)
                if ship.energy > (ship.job.energy * .3) and self._distance(ship.x, ship.y, self.player.home_base.x, self.player.home_base.y) >= 25:
                    x, y = self._moveTo(ship.x, ship.y, self.player.home_base.x, self.player.home_base.y, moves)
                    ship.dash(ship.x + x, ship.y + y)

    def _inv(self, ship):
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








