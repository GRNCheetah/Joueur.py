from math import cos
from math import sin

class Spawn:
    def __init__(self, p, g):
        self.player = p
        self.game = g
        self.runCnt = 0

    #Find the closest point to b that is on the circle of my spawning range
    def findCX(self, aX, aY, bX, bY, r):
        return aX + r * ((bX - aX) / (((bX - aX) ** 2 + (bY - aY) ** 2)) ** 0.5)
    def findCY(self, aX, aY, bX, bY, r):
        return aY + r * ((bY - aY) / (((bX - aX) ** 2 + (bY - aY) ** 2)) ** 0.5)

    def spawn(self):
        #get the amount of each unit, if it is somehow a missileboat, skip it
        amtCorv = 0
        amtShield = 0
        amtTrans = 0
        amtMiners = 0

        for u in self.player.units:
            if u.job.title == "corvette":
                amtCorv += 1
            elif u.job.title == "martyr":
                amtShield += 1
            elif u.job.title == "transport":
                amtTrans += 1
            elif u.job.title == "miner":
                amtMiners += 1
        #############################################

        #Get the closest of the miners, transporters, and asteroids
        closestMiner = [999999, 9999999]
        closestTrans = [999999, 9999999]
        closestRock = [999999, 9999999]

        for u in self.player.units:
            if u.job.title == "miner":
                if u.x < closestMiner[0] and u.y < closestMiner[1]:
                    closestMiner[0] = self.findCX(self.player.home_base.x, self.player.home_base.y, u.x, u.y, 1)
                    closestMiner[1] = self.findCY(self.player.home_base.x, self.player.home_base.y, u.x, u.y, 1)
            elif u.job.title == "transporter":
                if u.x < closestTrans[0] and u.y < closestTrans[1]:
                    closestTrans[0] = self.findCX(self.player.home_base.x, self.player.home_base.y, u.x, u.y, 1)
                    closestTrans[1] = self.findCY(self.player.home_base.x, self.player.home_base.y, u.x, u.y, 1)

        for b in range(4, len(self.game.bodies)):
            if self.game.bodies[b].x < closestRock[0] and self.game.bodies[b].y < closestRock[1]:
                closestRock[0] = self.findCX(self.player.home_base.x, self.player.home_base.y,
                                               self.game.bodies[b].x, self.game.bodies[b].y,
                                               self.player.home_base.radius)
                closestRock[1] = self.findCY(self.player.home_base.x, self.player.home_base.y,
                                               self.game.bodies[b].x, self.game.bodies[b].y,
                                               self.player.home_base.radius)
        ###############################################

        print("planet:", self.player.home_base.x, self.player.home_base.y, self.player.home_base.radius)

        #on first spawn, spawn transporters
        if self.runCnt == 0:
            if self.player.money < 75:
                return

            print("trans:", closestMiner[0], closestMiner[1])
            if not self.player.home_base.spawn(closestMiner[0], closestMiner[1], "transport"):
                self.player.home_base.spawn(self.player.home_base.x, self.player.home_base.y, "transport")

        elif self.runCnt == 1: #spawn another transporter then the rest of the $ is miners
            #return it there isn't enough $ for one
            if self.player.money < 75:
                return

            print("trans:", closestMiner[0], closestMiner[1])
            if not self.player.home_base.spawn(closestMiner[0], closestMiner[1], "transport"):
                self.player.home_base.spawn(self.player.home_base.x, self.player.home_base.y, "transport")


            if self.player.money < 150:
                return

            #spawn as many miners as possible
            while self.player.money >= 150:
                print("miners:", closestRock[0], closestRock[1])
                if not self.player.home_base.spawn(closestRock[0], closestRock[1], "miner"):
                    self.player.home_base.spawn(self.player.home_base.x, self.player.home_base.y, "miner")

        elif self.runCnt == 2:
            if self.player.money < 150: #return if there isn't enough $ for one
                return

            print("martyrs:", closestTrans[0], closestTrans[1])
            #spawn two
            if not self.player.home_base.spawn(closestTrans[0], closestTrans[1], "martyr"):
                self.player.home_base.spawn(self.player.home_base.x, self.player.home_base.y, "martyr")
            if not self.player.home_base.spawn(closestTrans[0], closestTrans[1], "martyr"):
                self.player.home_base.spawn(self.player.home_base.x, self.player.home_base.y, "martyr")

        elif self.runCnt > 2: #alternate spawning miners and corvettes
            if self.runCnt % 2 == 1: #miners
                if self.player.money < 150:
                    return

                breakout = 1 # breaks out of while after a couple iterations of not being decremented
                while self.player.money >= 150 and breakout < 5:
                    if amtMiners % 5 == 0: #make a transport every 5 miners

                        print("trans:", closestMiner[0], closestMiner[1])
                        if not self.player.home_base.spawn(closestMiner[0], closestMiner[1], "transport"):
                            if not self.player.home_base.spawn(self.player.home_base.x, self.player.home_base.y, "transport"):
                                breakout += 1
                        continue

                    print("miners:", closestRock[0], closestRock[1])
                    if not self.player.home_base.spawn(closestRock[0], closestRock[1], "miner"):
                        if not self.player.home_base.spawn(self.player.home_base.x, self.player.home_base.y, "miner"):
                            breakout += 1
                            continue
                    amtMiners += 1

            else: #corvettes
                if self.player.money < 100:
                    return

                while self.player.money >= 100:
                    if amtCorv % 2 == 0: #spawn corvette up at 45 degrees
                        xCoord = self.player.home_base.x
                        yCoord = self.player.home_base.y - self.player.home_base.radius

                        print("corvette:", xCoord, yCoord)
                        if not self.player.home_base.spawn(xCoord, yCoord, "corvette"):
                            self.player.home_base.spawn(xCoord, yCoord, "corvette")
                    elif amtCorv % 2 == 1: #spawn corvette down at 45 degrees (315 degrees)
                        xCoord = self.player.home_base.x
                        yCoord = self.player.home_base.y + self.player.home_base.radius

                        print("corvette:", xCoord, yCoord)
                        if not self.player.home_base.spawn(xCoord, yCoord, "corvette"):
                            self.player.home_base.spawn(xCoord, yCoord, "corvette")
                    else:
                        break
                    amtCorv += 1

        self.runCnt += 1
        return

