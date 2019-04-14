from math import cos
from math import sin

class Spawn:
    def __init__(self, p, g):
        self.player = p
        self.game = g
        self.runCnt = 0

    #Find the closest point to b that is on the circle of my spawning range
    def findCX(self, aX, aY, bX, bY, r):
        return aX + r * ((bX - aX) / ((bX - aX) ** 2 + (bY - aY) ** 2) ** 0.5)
    def findCY(self, aX, aY, bX, bY, r):
        return aY + r * ((bY - aY) / ((bX - aX) ** 2 + (bY - aY) ** 2) ** 0.5)

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

        print("planet:", self.player.home_base.x, self.player.home_base.y, self.player.home_base.radius)

        #on first spawn, spawn transporters
        if self.runCnt == 0:
            if self.player.money >= 75:
                xClosestMiner = 9999999
                yClosestMiner = 9999999

                #find the closest miner to the transporter and do math to find the closest point on the edge of the circle
                for u in self.player.units:
                    if u.job.title == "miner":
                        if u.x < xClosestMiner and u.y < yClosestMiner:
                            xClosestMiner = self.findCX(self.player.home_base.x, self.player.home_base.y, u.x, u.y, 1)
                            yClosestMiner = self.findCY(self.player.home_base.x, self.player.home_base.y, u.x, u.y, 1)

                print("trans:", xClosestMiner, yClosestMiner)

                if not self.player.home_base.spawn(xClosestMiner, yClosestMiner, "transport"):
                    self.player.home_base.spawn(self.player.home_base.x, self.player.home_base.y, "transport")
            else:
                return
        elif self.runCnt == 1:
            #return it there isn't enough $ for one
            if self.player.money < 150:
                return

            #spawn as many miners as possible
            while self.player.money >= 150:
                xClosestResource = 9999999
                yClosestResource = 9999999

                # spawn closest to the closest asteroid
                for b in range(4, len(self.game.bodies)):
                    if self.game.bodies[b].x < xClosestResource and self.game.bodies[b].y < yClosestResource:
                        xClosestResource = self.findCX(self.player.home_base.x, self.player.home_base.y,
                                                       self.game.bodies[b].x, self.game.bodies[b].y,
                                                       self.player.home_base.radius)
                        yClosestResource = self.findCY(self.player.home_base.x, self.player.home_base.y,
                                                       self.game.bodies[b].x, self.game.bodies[b].y,
                                                       self.player.home_base.radius)

                print("miners:", xClosestResource, yClosestResource)

                if not self.player.home_base.spawn(xClosestResource, yClosestResource, "miner"):
                    self.player.home_base.spawn(self.player.home_base.x, self.player.home_base.y, "miner")
        elif self.runCnt == 2:
            if self.player.money < 150: #return if there isn't enough $ for one
                return

            #Spawn 2 shields
            xClosestTrans = 9999999
            yClosestTrans = 9999999

            #Spawn the martyr as close as possible to the closest transporter
            for u in self.player.units:
                if u.job.title == "transport":
                    if u.x < xClosestTrans and u.y < yClosestTrans:
                        xClosestTrans = self.findCX(self.player.home_base.x, self.player.home_base.y, u.x, u.y, 1)
                        yClosestTrans = self.findCY(self.player.home_base.x, self.player.home_base.y, u.x, u.y, 1)

            print("martyrs:", xClosestTrans, xClosestTrans)

            #spawn two
            if not self.player.home_base.spawn(xClosestTrans, yClosestTrans, "martyr"):
                self.player.home_base.spawn(self.player.home_base.x, self.player.home_base.y, "martyr")
            if not self.player.home_base.spawn(xClosestTrans, yClosestTrans, "martyr"):
                self.player.home_base.spawn(self.player.home_base.x, self.player.home_base.y, "martyr")
        elif self.runCnt > 2: #alternate spawning miners and corvettes
            if self.runCnt % 2 == 1: #miners
                if self.player.money < 150:
                    return

                breakout = 1 # breaks out of while after a couple iterations of not being decremented
                while self.player.money >= 150 and breakout < 5:
                    if amtMiners % 5 == 0: #make a transport every 5 miners
                        xClosestMiner = 9999999
                        yClosestMiner = 9999999

                        # find the closest miner to the transporter and do math to find the closest point on the edge of the circle
                        for u in self.player.units:
                            if u.job.title == "miner":
                                if u.x < xClosestMiner and u.y < yClosestMiner:
                                    xClosestMiner = self.findCX(self.player.home_base.x, self.player.home_base.y, u.x,
                                                                u.y, 1)
                                    yClosestMiner = self.findCY(self.player.home_base.x, self.player.home_base.y, u.x,
                                                                u.y, 1)

                        print("trans:", xClosestMiner, yClosestMiner)

                        if not self.player.home_base.spawn(xClosestMiner, yClosestMiner, "transport"):
                            if not self.player.home_base.spawn(self.player.home_base.x, self.player.home_base.y, "transport"):
                                breakout += 1

                        continue

                    xClosestResource = 9999999
                    yClosestResource = 9999999

                    # spawn closest to the closest asteroid
                    for b in range(4, len(self.game.bodies)):
                        if self.game.bodies[b].x < xClosestResource and self.game.bodies[b].y < yClosestResource:
                            xClosestResource = self.findCX(self.player.home_base.x, self.player.home_base.y,
                                                           self.game.bodies[b].x, self.game.bodies[b].y,
                                                           self.player.home_base.radius)
                            yClosestResource = self.findCY(self.player.home_base.x, self.player.home_base.y,
                                                           self.game.bodies[b].x, self.game.bodies[b].y,
                                                           self.player.home_base.radius)

                    print("miners:", xClosestResource, yClosestResource)

                    if not self.player.home_base.spawn(xClosestResource, yClosestResource, "miner"):
                        if not self.player.home_base.spawn(self.player.home_base.x, self.player.home_base.y, "miner"):
                            breakout += 1
                            continue

                    amtMiners += 1
            else: #corvettes
                if self.player.money < 100:
                    return

                while self.player.money >= 100:
                    if amtCorv % 2 == 0: #spawn corvette up at 45 degrees
                        xCoord = self.player.home_base.x + self.player.home_base.radius * cos(45)
                        yCoord = self.player.home_base.y + self.player.home_base.radius * sin(45)

                        print("corvette:", xCoord, yCoord)

                        if not self.player.home_base.spawn(xCoord, yCoord, "corvette"):
                            self.player.home_base.spawn(self.player.home_base.x, self.player.home_base.y, "corvette")
                    elif amtCorv % 2 == 1: #spawn corvette down at 45 degrees (315 degrees)
                        xCoord = self.player.home_base.x + self.player.home_base.radius * cos(315)
                        yCoord = self.player.home_base.y + self.player.home_base.radius * sin(315)

                        print("corvette:", xCoord, yCoord)

                        if not self.player.home_base.spawn(xCoord, yCoord, "corvette"):
                            self.player.home_base.spawn(self.player.home_base.x, self.player.home_base.y, "corvette")
                    else:
                        break

                    amtCorv += 1

        """loop = True
        while loop:
            #spawn miner if I have the money and the amount of miners is less than 5(at the start)
            # or if i need to add a transport
            makeMartyr = False
            print("planet:", self.player.home_base.x, self.player.home_base.y, self.player.home_base.radius)
            if self.player.money >= 150:
                if not makeMartyr and (amtMiners < 5 or amtMiners % 5 != 0):
                    xClosestResource = 9999999
                    yClosestResource = 9999999

                    #spawn closest to the closest asteroid
                    for b in range(4, len(self.game.bodies)):
                        if self.game.bodies[b].x < xClosestResource and self.game.bodies[b].y < yClosestResource:
                            xClosestResource = self.findCX(self.player.home_base.x, self.player.home_base.y,
                                                           self.game.bodies[b].x, self.game.bodies[b].y,
                                                           self.player.home_base.radius)
                            yClosestResource = self.findCY(self.player.home_base.x, self.player.home_base.y,
                                                           self.game.bodies[b].x, self.game.bodies[b].y,
                                                           self.player.home_base.radius)

                    print("miners:", xClosestResource, yClosestResource)

                    if not self.player.home_base.spawn(xClosestResource, yClosestResource, "miner"):
                        self.player.home_base.spawn(self.player.home_base.x, self.player.home_base.y, "miner")
                elif makeMartyr:
                    #spawn closest to the closest transport
                    makeMartyr = False
                    xClosestTrans = 9999999
                    yClosestTrans = 9999999

                    for u in self.player.units:
                        if u.job.title == "transport":
                            if u.x < xClosestTrans and u.y < yClosestTrans:
                                xClosestTrans = self.findCX(self.player.home_base.x, self.player.home_base.y, u.x, u.y, 1)
                                yClosestTrans = self.findCY(self.player.home_base.x, self.player.home_base.y, u.x, u.y, 1)

                    print("martyrs:", xClosestTrans, xClosestTrans)

                    if not self.player.home_base.spawn(xClosestTrans, yClosestTrans, "martyr"):
                        self.player.home_base.spawn(self.player.home_base.x, self.player.home_base.y, "martyr")
            elif self.player.money >= 75:
                #spawn closest to the closest miner
                makeMartyr = True
                xClosestMiner = 9999999
                yClosestMiner = 9999999

                for u in self.player.units:
                    if u.job.title == "miner":
                        if u.x < xClosestMiner and u.y < yClosestMiner:
                            xClosestMiner = self.findCX(self.player.home_base.x, self.player.home_base.y, u.x, u.y, 1)
                            yClosestMiner = self.findCY(self.player.home_base.x, self.player.home_base.y, u.x, u.y, 1)

                print("trans:", xClosestMiner, yClosestMiner)

                if not self.player.home_base.spawn(xClosestMiner, yClosestMiner, "transport"):
                    self.player.home_base.spawn(self.player.home_base.x, self.player.home_base.y, "transport")
            else:
                loop = False"""

        self.runCnt += 1
        return

