# This is where you build your AI for the Stardash game.

from joueur.base_ai import BaseAI

# <<-- Creer-Merge: imports -->> - Code you add between this comment and the end comment will be preserved between Creer re-runs.
# you can add additional import(s) here
from games.stardash.Movement import moveMiner
# <<-- /Creer-Merge: imports -->>

class AI(BaseAI):
    """ The AI you add and improve code inside to play Stardash. """

    @property
    def game(self):
        """The reference to the Game instance this AI is playing.

        :rtype: games.stardash.game.Game
        """
        return self._game # don't directly touch this "private" variable pls

    @property
    def player(self):
        """The reference to the Player this AI controls in the Game.

        :rtype: games.stardash.player.Player
        """
        return self._player # don't directly touch this "private" variable pls

    def get_name(self):
        """ This is the name you send to the server so your AI will control the
            player named this string.

        Returns
            str: The name of your Player.
        """
        # <<-- Creer-Merge: get-name -->> - Code you add between this comment and the end comment will be preserved between Creer re-runs.
        return "SethAndFriends" # REPLACE THIS WITH YOUR TEAM NAME
        # <<-- /Creer-Merge: get-name -->>

    def start(self):
        """ This is called once the game starts and your AI knows its player and
            game. You can initialize your AI here.
        """
        # <<-- Creer-Merge: start -->> - Code you add between this comment and the end comment will be preserved between Creer re-runs.

        #sunX = self.game.bodies[2].x
        #sunY = self.game.bodies[2].y
        #self.player.units[0].move(sunX, sunY)


        # <<-- /Creer-Merge: start -->>

    def game_updated(self):
        """ This is called every time the game's state updates, so if you are
        tracking anything you can update it here.
        """
        # <<-- Creer-Merge: game-updated -->> - Code you add between this comment and the end comment will be preserved between Creer re-runs.
        # replace with your game updated logic
        # <<-- /Creer-Merge: game-updated -->>

    def end(self, won, reason):
        """ This is called when the game ends, you can clean up your data and
            dump files here if need be.

        Args:
            won (bool): True means you won, False means you lost.
            reason (str): The human readable string explaining why your AI won
            or lost.
        """
        # <<-- Creer-Merge: end -->> - Code you add between this comment and the end comment will be preserved between Creer re-runs.
        # replace with your end logic
        # <<-- /Creer-Merge: end -->>
    def run_turn(self):
        """ This is called every time it is this AI.player's turn.

        Returns:
            bool: Represents if you want to end your turn. True means end your turn, False means to keep your turn going and re-call this function.
        """
        # <<-- Creer-Merge: runTurn -->> - Code you add between this comment and the end comment will be preserved between Creer re-runs.
        # Put your game logic here for runTurn
        sunX = self.game.bodies[2].x
        sunY = self.game.bodies[2].y
        #print(self.player.units)

        '''minerX = self.player.units[0].x
        minerY = self.player.units[0].y

        minDist = self.distance((0,0),(self.game.size_x, self.game.size_y))
        minAst = 0
        for astNum in range(4, len(self.game.bodies)):
            #dist = ((minerX - self.game.bodies[astNum].x) ** 2 + (minerY - self.game.bodies[astNum].y) ** 2) ** .5

            dist = self.distance((minerX, minerY), (self.game.bodies[astNum].x, self.game.bodies[astNum].y))
            if (dist < minDist):
                minDist = dist
                minAst = astNum

        target = self.game.bodies[minAst]

        if abs(minerX-target.x) >= 1:
            if minerX-target.x > 0:
                tarX = 64
            else:
                tarX = -64
        else:
            tarX = minerX - target.x

        if abs(minerY-target.y) >= 1:
            if minerY-target.y > 0:
                tarY = 64
            else:
                tarY = -64
        else:
            tarY = minerY - target.y

        self.player.units[0].move(minerX+tarX, minerY+tarY)

        # Loop for giving tasks based on unit type
        for ship in self.player.units:
            if ship.job.title == "miner":
                # For each asteroid, find the closest
                minerX = ship.x
                minerY = ship.y
                for astNum in range(4, len(self.game.bodies)):
                    # Find distance to current asteroid
                    if (self.game.bodies[astNum].material_type == "mythicite"):
                        dist = self.distance((minerX, minerY, (self.game.bodies[astNum].x, self.game.bodies[astNum].y)))
                        if (dist < minDist):
                            minDist = dist
                            minAst = astNum

                target = self.game.bodies[minAst]


                # This will move directly at the asteroid
                # We can make this faster if we can predict where the asteroid will be and move there.
                currDist = self.distance((minerX, minerY), (self.game.bodies[minAst].x, self.game.bodies[minAst].y))
                turns = 1
                nextX = self.game.bodies[minAst].next_x(turns)
                nextY = self.game.bodies[minAst].next_y(turns)
                nextDist = self.distance(((minerX + ship.job.moves * turns) if (minerX-nextX > 0) else (minerX - ship.job.moves * turns),
                                          (minerY + ship.job.moves * turns) if (minerY-nextY) > 0 else (minerY - ship.job.moves * turns)), (nextX, nextY))
                while nextDist < currDist:
                    currDist = nextDist
                    turns += 1
                    nextDist = self.distance(((minerX + ship.job.moves)*turns if (minerX - nextX > 0) else (
                                minerX - ship.job.moves)*turns, (minerY + ship.job.moves)*turns if (minerY - nextY) > 0 else (
                                minerY - ship.job.moves)*turns), (self.game.bodies[minAst].next_x(turns),
                                                            self.game.bodies[minAst].next_y(turns)))


                # Move toward where the asteroid will be in turns
                # These are the modifiers for where we need to move
                tarX, tarY = self.moveTo(ship.x, ship.y, self.game.bodies[minAst].next_x(turns), self.game.bodies[minAst].next_y[turns], ship.job.moves)

                ship.move(ship.x+tarX, ship.y+tarY)

            if ship.job.title == "martyr":
                pass
            if ship.job.title == "corvette":
                pass
            if ship.job.title == "transport":
                pass
            if ship.job.title == "missileboat":
                pass






        me()'''

        moveMiner(self.player.units[0], self.game, self.player, "myth", [])
        return True
        # <<-- /Creer-Merge: runTurn -->>

    # <<-- Creer-Merge: functions -->> - Code you add between this comment and the end comment will be preserved between Creer re-runs.
    # if you need additional functions for your AI you can add them here
    def distance(self, start, end):
        """Returns the distance between two points.

        Two tuples (x, y)
        """
        return ((start[0] - end[0])**2 + (start[1] - end[1])**2) ** .5

    def moveTo(self, shipX, shipY, tarX, tarY, move):
        """Returns the x and y speed to get to target x and y.

        This is to take care of the positives and negatives.
        """
        x = shipX - tarX
        if x > move: # greater than one move
            x = move
        elif x < (-1 * move):
            x = -1 * move

        y = shipY - tarY
        if y > move:
            y = move
        elif y < (-1 * move):
            y = -1 * move

        return x, y

    # <<-- /Creer-Merge: functions -->>
