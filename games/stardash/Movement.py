import math

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
                self.moveMiner(ship)
            elif ship.job.title == "martyr" and c < 6:
                self.moveMartyr(ship)
                pass
            elif c >= 6:
                attack = True
                if self.game.current_turn > 12:
                    self.endgame = True


        return attack



    def moveMartyr(self, ship):
        if not ship.acted:
            # Going to the belt
            if ship.x != self.mine_spot_x and ship.y != self.mine_spot_y:
                self._dashTo(ship, self.mine_spot_x, self.mine_spot_y)



    def moveCorvette(self, ship):
        """Two different """

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

    def moveMissileBoat(self, ship):
        pass


    def moveMiner(self, ship):
        """Gets passed a ship, the game and the player.

        Moves a Miner towards the nearest asteroid.
        """
        if not ship.acted:
            # Hail mary to the Mythicite
            if (self._inv(ship) < ship.job.carry_limit) and self.endgame and ship.energy > (ship.job.energy * .25):
                x = self.game.bodies[3].next_x(2)
                y = self.game.bodies[3].next_y(2)
                self._dashTo(ship, x, y)
            # Going to the belt
            elif (self._inv(ship) < ship.job.carry_limit and ship.energy > (ship.job.energy * .25)):
                self._dashTo(ship, self.mine_spot_x, self.mine_spot_y)
            # Going home
            elif (self._inv(ship) >= ship.job.carry_limit) and ship.safe(self.home_x, self.home_y): # Go back home
                self._dashTo(ship, self.home_x, self.home_y)

    def _inv(self, ship):
        return ship.genarium + ship.legendarium + ship.mythicite + ship.rarium

    def _dashTo(self, unit, x, y):


        sun = self.game.bodies[2]
        while unit.moves >= 1:

            if unit.safe(x, y) and unit.energy >= math.ceil (
                    (self._distance(unit.x, unit.y, x, y) / self.game.dash_distance) * self.game.dash_cost):
                # Dashes if it is safe to dash to the point and we have enough energy to dash there.
                unit.dash(x, y)

                # Breaks out of the loop since we can't do anything else now.
                break
            else:
                # Otherwise tries moving towards the target.

                # The x and y modifiers for movement.
                x_mod = 0
                y_mod = 0

                if unit.x < x or (y < sun.y and unit.y > sun.y or y > sun.y and unit.y < sun.y) and x > sun.x:
                    # Move to the right if the destination is to the right or on the other side of the sun on the right side.
                    x_mod = 1
                elif unit.x > x or (y < sun.y and unit.y > sun.y or y > sun.y and unit.y < sun.y) and x < sun.x:
                    # Move to the left if the destination is to the left or on the other side of the sun on the left side.
                    x_mod = -1

                if unit.y < y or (x < sun.x and unit.x > sun.x or x > sun.x and unit.x < sun.x) and y > sun.y:
                    # Move down if the destination is down or on the other side of the sun on the lower side.
                    y_mod = 1
                elif unit.y > y or (x < sun.x and unit.x > sun.x or x > sun.x and unit.x < sun.x) and y < sun.y:
                    # Move up if the destination is up or on the other side of the sun on the upper side.
                    y_mod = -1

                if x_mod != 0 and y_mod != 0 and not unit.safe(unit.x + x_mod, unit.y + y_mod):
                    # Special case if we cannot safely move diagonally.
                    if unit.safe(unit.x + x_mod, unit.y):
                        # Only move horizontally if it is safe.
                        y_mod = 0
                    elif unit.safe(unit.x, unit.y + y_mod):
                        # Only move vertically if it is safe.
                        x_mod = 0

                if unit.moves < math.sqrt(2) and x_mod != 0 and y_mod != 0:
                    # Special case if we only have 1 move left and are trying to move 2.
                    if unit.safe(unit.x + x_mod, unit.y):
                        y_mod = 0
                    elif unit.safe(unit.x, unit.y + y_mod):
                        x_mod = 0
                    else:
                        break

                if (x_mod != 0 or y_mod != 0) and (math.sqrt(math.pow(x_mod, 2) + math.pow(y_mod, 2)) >= unit.moves):
                    # Tries to move if either of the modifiers is not zero (we are actually moving somewhere).
                    unit.move(unit.x + x_mod, unit.y + y_mod)
                else:
                    # Breaks otherwise, since something probably went wrong.
                    break

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








