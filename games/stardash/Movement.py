#class Movement():

#    def __init__(self):
#        pass

from time import time

class Movement:

    def __init__(self, p, g):
        self.player = p
        self.game = g



    def move(self):

        c = 0
        for s in self.player.units:
            if s.job.title == "corvette":
                c += 1  # Indicates which position to go to

        attack = False

        for ship in self.player.units:
            if ship.job.title == "miner":
                self.moveMiner(ship)
            elif ship.job.title == "transport":
                self.moveTransport(ship)
            elif ship.job.title == "corvette" and c < 6:
                #self.moveCorvette(ship)
                pass
            elif ship.job.title == "missileboat" and c < 6:
                #self.moveMissileBoat(ship)
                pass
            elif ship.job.title == "martyr" and c < 6:
                #self.moveMartyr(ship)
                pass    
            elif c >= 6:
                attack = True

        return attack



    def moveTransport(self, ship):
        moves = ship.job.moves
        t = time()

        if not ship.acted:
            if (self._inv(ship) < ship.job.carry_limit): # Go towards the miners
                maxDist = 0

                # Finds the farthest miner from the home planet
                ships = self.player.units
                if len(ships) > 0:
                    maxShip = ships[0]
                    for shipNum in range(1, len(ships)):
                        if ships[shipNum] == "miner":
                            maxDist = self._distance(ship.x, ship.y, ships[shipNum].x, ships[shipNum].y)
                    if maxDist >= ship.job.range *.75:
                        x, y = self._moveTo(ship.x, ship.y, maxShip.x, maxShip.y, moves)
                        print(x, y)
                        ship.move(ship.x + x, ship.y + y)
                        if ship.energy > (ship.job.energy * .8) and self._distance(ship.x, ship.y, maxShip.x, maxShip.y) >= (moves * .5):
                            x, y = self._moveTo(ship.x, ship.y, maxShip.x, maxShip.y, moves)
                            ship.dash(ship.x + x, ship.y + y)
            else: # Go home to drop off
                x, y = self._moveTo(ship.x, ship.y, self.player.home_base.x, self.player.home_base.y, moves)
                ship.move(ship.x + x, ship.y + y)
                if ship.energy > (ship.job.energy * .3) and self._distance(ship.x, ship.y, self.player.home_base.x, self.player.home_base.y) >= (moves * .5):
                    x, y = self._moveTo(ship.x, ship.y, self.player.home_base.x, self.player.home_base.y, moves)
                    ship.dash(ship.x + x, ship.y + y)
        print("Transport: ", time() - t)

    def moveMartyr(self, ship):
        t = time()
        moves = ship.job.moves

        if not ship.acted:
            if (self._inv(ship) < ship.job.carry_limit): # Go towards the miners
                maxDist = 0

                # Finds the farthest miner from the home planet
                ships = self.player.units
                if len(ships) > 0:
                    maxShip = ships[0]
                    for shipNum in range(1, len(ships)):
                        dist2planet = self._distance(ship.x, ship.y, ships[shipNum].x, ships[shipNum].y)
                        if dist2planet > maxDist:
                            maxDist = dist2planet
                            maxShip = ships[shipNum]

                    x, y = self._moveTo(ship.x, ship.y, maxShip.x, maxShip.y, moves)
                    #print(x, y)
                    ship.move(ship.x + x, ship.y + y)
                    if ship.energy > (ship.job.energy * .8) and self._distance(ship.x, ship.y, maxShip.x, maxShip.y) >= (moves * .5):
                        x, y = self._moveTo(ship.x, ship.y, maxShip.x, maxShip.y, moves)
                        ship.dash(ship.x + x, ship.y + y)

        print("Martyr: ", time()-t)

    def moveCorvette(self, ship):
        """Two different """
        t = time()

        count = 0
        for s in self.player.units:
            if s.job.title == "corvette" and s != ship:
                count += 1  # Indicates which position to go to
        moves = ship.job.moves

        x_help = self.game.size_x/2
        y_help = self.game.size_y/2 - self.game.bodies[2].radius # The amount of space between sun and top
        # Top
        positions = [
            [None, (x_help, (y_help * .3))],
            [None, (x_help, (y_help * .6))],
            [None, (x_help, (y_help * .9))],
            [None, (x_help, y_help + (y_help * .3))],
            [None, (x_help, y_help + (y_help * .6))],
            [None, (x_help, y_help + (y_help * .9))]
        ]

        # Find empty position
        target = (0,0)
        for pos in positions:
            if not pos[0]: # Fill empty slot
                pos[0] = ship
                target = pos[1]
            else: # Found location
                target = pos[1]

        # No send this corvette to the correct position
        x, y = self._moveTo(ship.x, ship.y, target[0],  target[1], moves)
        ship.move(ship.x + x, ship.y + y)

        print("Corvette: ", time() - t)

    def moveMissileBoat(self, ship):
        pass


    def moveMiner(self, ship):
        """Gets passed a ship, the game and the player.

        Moves a Miner towards the nearest asteroid.
        """
        t = time()
        moves = ship.job.moves

        if not ship.acted:
            #ship.log('did not mine')
            if (self._inv(ship) < ship.job.carry_limit):
                #minDist = self._distance(0, 0, self.game.size_x, self.game.size_y)

                # Finds the closest asteroid and puts it in minAst
                '''asteroids = self.game.bodies
                minAst = asteroids[0]
                for astNum in range(4, len(asteroids)):
                    dist = self._distance(ship.x, ship.y, asteroids[astNum].x, asteroids[astNum].y)
                    if dist < minDist:
                        minDist = dist
                        minAst = asteroids[astNum]'''

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

                sunX = self.game.bodies[2].x
                sunY = self.game.bodies[2].y
                sunR = self.game.bodies[2].radius + 250
                if self.player.home_base.x < sunX / 2:
                    sunR = sunR * -1

                x, y = self._moveTo(ship.x, ship.y, sunX + sunR, minAst.y + sunR, moves)
                #print(x, y)
                ship.move(ship.x + x, ship.y + y)
                if ship.energy > (ship.job.energy * .8) and self._distance(ship.x, ship.y, sunX + sunR, minAst.y + sunR) >= (moves * .5):
                    x, y = self._moveTo(ship.x, ship.y, sunX + sunR, minAst.y + sunR, moves)
                    ship.dash(ship.x + x, ship.y + y)
            else:
                x, y = self._moveTo(ship.x, ship.y, self.player.home_base.x, self.player.home_base.y, moves)
                ship.move(ship.x + x, ship.y + y)
                if ship.energy > (ship.job.energy * .3) and self._distance(ship.x, ship.y, self.player.home_base.x, self.player.home_base.y) >= (moves * .5):
                    x, y = self._moveTo(ship.x, ship.y, self.player.home_base.x, self.player.home_base.y, moves)
                    ship.dash(ship.x + x, ship.y + y)

        print("Miner: ", time() - t)

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








