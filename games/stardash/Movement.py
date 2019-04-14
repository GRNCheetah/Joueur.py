import math

from time import time

class Movement:

    def __init__(self, p, g):
        self.player = p
        self.game = g

        self.endgame = False

        sunX = self.game.bodies[2].x
        sunY = self.game.bodies[2].y
        sunR = self.game.bodies[2].radius + 250
        if self.player.home_base.x < sunX / 2:
            sunR = sunR * -1
        self.mine_spot_x = sunX + sunR
        self.mine_spot_y = sunY

        if sunR < 0:  # To the left
            self.home_x = self.player.home_base.x + self.player.home_base.radius - 10
        else:  # To the right
            self.home_x = self.player.home_base.x - self.player.home_base.radius + 10
        self.home_y = self.player.home_base.y



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
                if self.game.current_turn > 12:
                    self.endgame = True


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

            numDashes = math.ceil((self._distance(ship.x, ship.y, self.mine_spot_x, self.mine_spot_y) / self.game.dash_distance) * self.game.dash_cost)
            # Hail mary to the Mythicite
            if (self._inv(ship) < ship.job.carry_limit) and self.endgame:
                x = self.game.bodies[3].next_x
                y = self.game.bodies[3].next_y
                if (ship.safe(x,y)):
                    if ship.energy >= numDashes:  # Dash
                        ship.dash(x, y)
                    else:  # Something is not right
                        x, y = self._moveTo(ship.x, ship.y, x, y, moves)
                        ship.move(ship.x + x, ship.y + y)
            # Going to the belt
            elif (self._inv(ship) < ship.job.carry_limit) and ship.safe(self.mine_spot_x, self.mine_spot_y):
                if ship.energy >= numDashes: # Dash
                    ship.dash(self.mine_spot_x, self.mine_spot_y)
                else: # Something is not right
                    x, y = self._moveTo(ship.x, ship.y, self.mine_spot_x, self.mine_spot_y, moves)
                    ship.move(ship.x+x, ship.y+y)
            # Going home
            elif (self._inv(ship) >= ship.job.carry_limit) and ship.safe(self.home_x, self.home_y): # Go back home
                    #x, y = self._moveTo(ship.x, ship.y, self.player.home_base.x, self.player.home_base.y, moves)

                if ship.energy >= numDashes: # Dash
                    ship.dash(self.home_x, self.home_y)
                else: # Something is not right
                    x, y = self._moveTo(ship.x, ship.y, self.mine_spot_x, self.mine_spot_y, moves)
                    ship.move(ship.x+x, ship.y+y)

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








