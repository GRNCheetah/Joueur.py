class Spawn:

    def __init__(self, p, g):
        self.player = p
        self.game = g

    #Find the closest point to b that is on the circle of my movement range
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

        #save up for miners
        if self.player.money < 150 and amtMiners < 5:
            return

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

                self.player.home_base.spawn(xClosestResource, yClosestResource, "miner")
            else:
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

                self.player.home_base.spawn(xClosestTrans, yClosestTrans, "martyr")

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

            self.player.home_base.spawn(xClosestMiner, yClosestMiner, "transport")
        #else nothing spawns


