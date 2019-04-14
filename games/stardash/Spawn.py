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

        #spawn miner if I have the money and the amount of miners is less than 5(at the start)
        # or if i need to add a transport
        if self.player.money >= 150 and (amtMiners < 5 or amtMiners % 5 != 0):
            xClosestResource = 0
            yClosestResource = 0

            for b in range(4, len(self.game.bodies)):
                if self.game.bodies[b].x > xClosestResource and self.game.bodies[b].y > yClosestResource:
                    xClosestResource = self.findCX(self.player.home_base.x, self.player.home_base.y, self.game.bodies[b].x, self.game.bodies[b].y, self.player.home_base.radius)
                    yClosestResource = self.findCY(self.player.home_base.x, self.player.home_base.y, self.game.bodies[b].x, self.game.bodies[b].y, self.player.home_base.radius)

            print(xClosestResource, yClosestResource)

            self.player.home_base.spawn(xClosestResource, yClosestResource, "miner")
        elif self.player.money >= 75:
            xClosestTrans = 0
            yClosestTrans = 0

            for u in self.player.units:
                if u.job.title == "transport":
                    if u.x > xClosestTrans and u.y > yClosestTrans:
                        xClosestTrans = self.findCX(self.player.home_base.x, self.player.home_base.y, u.x, u.y, 1)
                        yClosestTrans = self.findCY(self.player.home_base.x, self.player.home_base.y, u.x, u.y, 1)

            self.player.home_base.spawn(xClosestTrans, yClosestTrans, "transport")
        #else nothing spawns


