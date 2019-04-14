from time import time

class Spawn:
    def __init__(self, p, g):
        self.player = p
        self.game = g
        self.runCnt = 0
        self.amtMiners = 3
        self.amtCorv = 0
        self.amtShield = 0
        self.amtTrans = 0

    #Find the closest point to b that is on the circle of my spawning range
    def findCX(self, aX, aY, bX, bY, r):
        return aX + r * ((bX - aX) / (((bX - aX) ** 2 + (bY - aY) ** 2)) ** 0.5)
    def findCY(self, aX, aY, bX, bY, r):
        return aY + r * ((bY - aY) / (((bX - aX) ** 2 + (bY - aY) ** 2)) ** 0.5)

    def spawn(self):
        t = time()

        #Get the closest of the miners, transporters, and asteroids
        closestMiner = [999999, 9999999]
        closestTrans = [999999, 9999999]
        closestRock = [999999, 9999999]

        t1 = time()
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
        print("init fors:", format(time() - t1, '.10f'))
        ###############################################

        #print("planet:", self.player.home_base.x, self.player.home_base.y, self.player.home_base.radius)

        #on first spawn, spawn transporters
        if self.runCnt == 0:
            t1 = time()
            if self.player.money < 75:
                return

            #print("trans:", closestMiner[0], closestMiner[1])
            if not self.player.home_base.spawn(closestMiner[0], closestMiner[1], "transport"):
                self.player.home_base.spawn(self.player.home_base.x, self.player.home_base.y, "transport")

            print("first run:", format(time() - t1, '.10f'))

        elif self.runCnt == 1: #spawn another transporter then the rest of the $ is miners
            #return it there isn't enough $ for one
            t1 = time()
            if self.player.money < 75:
                return

            #print("trans:", closestMiner[0], closestMiner[1])
            if not self.player.home_base.spawn(closestMiner[0], closestMiner[1], "transport"):
                self.player.home_base.spawn(self.player.home_base.x, self.player.home_base.y, "transport")


            if self.player.money < 150:
                return

            #spawn as many miners as possible
            while self.player.money >= 150:
                #print("miners:", closestRock[0], closestRock[1])
                if not self.player.home_base.spawn(closestRock[0], closestRock[1], "miner"):
                    self.player.home_base.spawn(self.player.home_base.x, self.player.home_base.y, "miner")
            print("2nd run:", format(time() - t1, '.10f'))

        elif self.runCnt == 2:
            t1 = time()
            if self.player.money < 150: #return if there isn't enough $ for one
                return

            #print("martyrs:", closestTrans[0], closestTrans[1])
            #spawn two
            if not self.player.home_base.spawn(closestTrans[0], closestTrans[1], "martyr"):
                self.player.home_base.spawn(self.player.home_base.x, self.player.home_base.y, "martyr")
            if not self.player.home_base.spawn(closestTrans[0], closestTrans[1], "martyr"):
                self.player.home_base.spawn(self.player.home_base.x, self.player.home_base.y, "martyr")

            print("3rd run:", format(time() - t1, '.10f'))

        elif self.runCnt > 2: #alternate spawning miners and corvettes
            t1 = time()
            if self.runCnt % 2 == 1: #miners
                if self.player.money < 150:
                    return

                breakout = 1 # breaks out of while after a couple iterations of not being decremented
                while self.player.money >= 150 and breakout < 5:
                    if self.amtMiners % 5 == 0: #make a transport every 5 miners

                        #print("trans:", closestMiner[0], closestMiner[1])
                        if not self.player.home_base.spawn(closestMiner[0], closestMiner[1], "transport"):
                            if not self.player.home_base.spawn(self.player.home_base.x, self.player.home_base.y, "transport"):
                                breakout += 1
                        continue

                    #print("miners:", closestRock[0], closestRock[1])
                    if not self.player.home_base.spawn(closestRock[0], closestRock[1], "miner"):
                        if not self.player.home_base.spawn(self.player.home_base.x, self.player.home_base.y, "miner"):
                            breakout += 1
                            continue
                    self.amtMiners += 1

                print("alternating:", format(time() - t1, '.10f'))
            else: #corvettes
                t1 = time()
                if self.player.money < 100:
                    return

                while self.player.money >= 100:
                    if self.amtCorv % 2 == 0: #spawn corvette up at 45 degrees
                        xCoord = self.player.home_base.x
                        yCoord = self.player.home_base.y - self.player.home_base.radius

                        #print("corvette:", xCoord, yCoord)
                        if not self.player.home_base.spawn(xCoord, yCoord, "corvette"):
                            self.player.home_base.spawn(xCoord, yCoord, "corvette")
                    elif self.amtCorv % 2 == 1: #spawn corvette down at 45 degrees (315 degrees)
                        xCoord = self.player.home_base.x
                        yCoord = self.player.home_base.y + self.player.home_base.radius

                        #print("corvette:", xCoord, yCoord)
                        if not self.player.home_base.spawn(xCoord, yCoord, "corvette"):
                            self.player.home_base.spawn(xCoord, yCoord, "corvette")
                    else:
                        break
                    self.amtCorv += 1
                print("corvettes:", format(time() - t1, '.10f'))

        self.runCnt += 1
        print("Spawn:", format(time() - t, '.10f'))
        return

