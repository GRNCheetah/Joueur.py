import math
class Action:

    def __init__(self, p, g):
        self.player = p
        self.game = g

    def transfer_goods(self, transport):
        for unit in self.player.units:
            if ((transport.x-unit.x)**2+(transport.y-unit.y)**2)**.5 <= transport.job.range:
                if unit.mythicite>0 and transport.mythicite+transport.legendarium+transport.rarium+transport.genarium<transport.job.carry_limit:
                    transport.transfer(unit,-1,'mythicite')
                if unit.legendarium>0 and transport.mythicite+transport.legendarium+transport.rarium+transport.genarium<transport.job.carry_limit:
                    transport.transfer(unit,-1,'legendarium')
                if unit.rarium>0 and transport.mythicite+transport.legendarium+transport.rarium+transport.genarium<transport.job.carry_limit:
                    transport.transfer(unit,-1,'rarium')
                if unit.genarium>0 and transport.mythicite+transport.legendarium+transport.rarium+transport.genarium<transport.job.carry_limit:
                    transport.transfer(unit,-1,'genarium')

    def shootShieldies(self, missileboat):
        for unit in self.player.opponent.units:
            if unit.job.title=='martyr' and ((missileboat.x-unit.x)**2+(missileboat.y-unit.y)**2)**.5 <= missileboat.job.range:
                isAlreadyTargeted=False
                for missile in self.player.projectiles:
                    if missile.target==unit:
                        isAlreadyTargeted=True
                if not isAlreadyTargeted:
                    missileboat.attack(unit)
                    break
    
    def shootTransports(self, missileboat):
        for unit in self.player.opponent.units:
            if unit.job.title=='transport' and ((missileboat.x-unit.x)**2+(missileboat.y-unit.y)**2)**.5 <= missileboat.job.range:
                isAlreadyTargeted=False
                for missile in self.player.projectiles:
                    if missile.target==unit:
                        isAlreadyTargeted=True
                if not isAlreadyTargeted:
                    missileboat.attack(unit)
                    break
    
    def shootMiners(self, missileboat):
        for unit in self.player.opponent.units:
            if unit.job.title=='miner' and ((missileboat.x-unit.x)**2+(missileboat.y-unit.y)**2)**.5 <= missileboat.job.range:
                isAlreadyTargeted=False
                for missile in self.player.projectiles:
                    if missile.target==unit:
                        isAlreadyTargeted=True
                if not isAlreadyTargeted:
                    missileboat.attack(unit)
                    break
    
    def shootMissiles(self, missileboat):
        for unit in self.player.opponent.units:
            if unit.job.title=='missileboat' and ((missileboat.x-unit.x)**2+(missileboat.y-unit.y)**2)**.5 <= missileboat.job.range:
                isAlreadyTargeted=False
                for missile in self.player.projectiles:
                    if missile.target==unit:
                        isAlreadyTargeted=True
                if not isAlreadyTargeted:
                    missileboat.attack(unit)
                    break
    
    def shootCorvettes(self, missileboat):
        for unit in self.player.opponent.units:
            if unit.job.title=='corvette' and ((missileboat.x-unit.x)**2+(missileboat.y-unit.y)**2)**.5 <= missileboat.job.range:
                isAlreadyTargeted=False
                for missile in self.player.projectiles:
                    if missile.target==unit:
                        isAlreadyTargeted=True
                if not isAlreadyTargeted:
                    missileboat.attack(unit)
                    break
    
    def shootProjectiles(self, corvette):
        for missile in self.player.opponent.projectiles:
            if ((missile.x-corvette.x)**2+(missile.y-corvette.y)**2)**.5 <= corvette.job.range:
                corvette.shootdown(missile)
                break
                    
    def mine_neighbors(self, unit):
        if unit.mythicite+unit.legendarium+unit.rarium+unit.genarium<unit.job.carry_limit:
            neighbors=[]
            for body in self.game.bodies:
                if body.body_type=='asteroid' and body.amount>10:
                    if ((body.x-unit.x)**2+(body.y-unit.y)**2)**.5 <= unit.job.range:
                        neighbors.append(body)
            myths=[]
            legends=[]
            rares=[]
            genes=[]
            nones=[]
            for neighbor in neighbors:
                if neighbor.material_type=='mythicite' and self.game.current_turn > self.game.orbits_protected:
                    myths.append(neighbor)
                elif neighbor.material_type=='legendarium':
                    legends.append(neighbor)
                elif neighbor.material_type=='rarium':
                    rares.append(neighbor)
                elif neighbor.material_type=='genarium':
                    genes.append(neighbor)
                else:
                    nones.append(neighbor)
            if len(myths)>0 and self.game.current_turn > self.game.orbits_protected:
                if myths[0].amount >= 10:
                    unit.mine(myths[0])
                elif len(myths)>1:
                    unit.mine(myths[1])
            elif len(legends)>0:
                if legends[0].amount >= 10:
                    unit.mine(legends[0])
                elif len(legends)>1:
                    unit.mine(legends[1])
            elif len(rares)>0:
                if rares[0].amount >= 10:
                    unit.mine(rares[0])
                elif len(rares)>1:
                    unit.mine(rares[1])
            elif len(genes)>0:
                if genes[0].amount >= 10:
                    unit.mine(genes[0])
                elif len(genes)>1:
                    unit.mine(genes[1])

    def shootNonShielded(self, corvette):
        for unit in self.player.opponent.units:
            if ((corvette.x-unit.x)**2+(corvette.y-unit.y)**2)**.5 <= corvette.job.range:
                isAlreadyTargeted=False
                for missile in self.player.projectiles:
                    if missile.target==unit:
                        isAlreadyTargeted=True
                if not isAlreadyTargeted and unit.protector == None:
                    corvette.attack(unit)
                    break
    
    def do_miner(self, miner):
        self.mine_neighbors(miner)

    def do_transport(self, transport):
        self.transfer_goods(transport)
    
    def do_missiles(self, missileboat):
        self.moveToNearestEnemy(missileboat)
        self.shootShieldies(missileboat)
        if not missileboat.acted:
            self.shootTransports(missileboat)
        if not missileboat.acted:
            self.shootMiners(missileboat)
        if not missileboat.acted:
            self.shootMissiles(missileboat)
        if not missileboat.acted:
            self.shootCorvettes(missileboat)
    
    def do_corvettes(self, corvette):
        self.shootProjectiles(corvette)
        self.moveToNearestEnemy(corvette)
        if not corvette.acted:
            self.shootNonShielded(corvette)
            
    def go_to_friend_fighter(self, mar):
        if ((self.player.home_base.x-mar.x)**2+(self.player.home_base.y-mar.y)**2)**.5 <= 1400:
            (x,y)=self.find_move(mar, self.game.size_x/2, 30, mar.moves)
            mar.move(mar.x+x, mar.y+y)
        else:
            closestFighter=None
            minDistance=99999 #infinity
            for unit in self.player.units:
                if unit=='corvette' or unit=='missileboat':
                    if self.distance(unit.x, unit.y, mar.x, mar.y)<minDistance:
                        closestFighter=unit
                        minDistance=self.distance(unit.x, unit.y, mar.x, mar.y)
            (x,y)=self.find_move(mar, unit.x, unit.y, mar.moves)
            mar.move(mar.x+x,mar.y+y)
    
    
    def find_dash(self, unit, x, y):
        """ This is an EXTREMELY basic pathfinding function to move your ship until it can dash to your target.
            You REALLY should improve this functionality or make your own new one, since this is VERY basic and inefficient.
            Like, for real.
            Args:
                unit (unit): The unit that will be moving.
                x (int): The x coordinate of the destination.
                y (int): The y coordinate of the destination.
        """
        # Gets the sun from the list of bodies.
        sun = self.game.bodies[2]

        while unit.moves >= 1:
            if unit.safe(x, y) and unit.energy >= math.ceil((self.distance(unit.x, unit.y, x, y) / self.game.dash_distance) * self.game.dash_cost):
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
                    
    def find_move(self, unit, x, y, move):
        """Returns the x and y speed to get to target x and y.

        This is to take care of the positives and negatives.
        """
        dist = self.distance(unit.x, unit.y, x, y) + .1
        max_move = move / (2 ** .5)

        x = move * ((x - unit.x)/dist)
        y = move * ((y - unit.y)/dist)

        if x > max_move:
            x = max_move
        elif x < (-1 * max_move):
            x = -1 * max_move

        if y > max_move:
            y = max_move
        elif y < (-1 * max_move):
            y = -1 * max_move

        return x, y
       
       
    def distance(self, shipX, shipY, tarX, tarY):
        return ((shipX - tarX)**2 + (shipY - tarY)**2) ** .5
        
    
    
    def moveToNearestEnemy(self, unit):
        if ((self.player.home_base.x-unit.x)**2+(self.player.home_base.y-unit.y)**2)**.5 <= 1400:
            (x,y)=self.find_move(unit, self.game.size_x/2, 30, unit.moves)
            unit.move(unit.x+x, unit.y+y)
        else:
            minDistance=99999 #infinity
            minEnemy=None
            for enemy in self.player.opponent.units:
                if self.distance(unit.x,unit.y,enemy.x,enemy.y)<minDistance:
                    minDistance=self.distance(unit.x,unit.y,enemy.x,enemy.y)
                    minEnemy=enemy
            if self.distance(unit.x,unit.y,minEnemy.x,minEnemy.y)>unit.job.range:
                (x,y)=self.find_move(unit, enemy.x, enemy.y, unit.moves)
                unit.move(unit.x+x, unit.y+y)
        
    def do_actions(self):
        for unit in self.player.units:
            if not unit.acted:
                if unit.job.title=='miner':
                    self.do_miner(unit)
                elif unit.job.title=='transport':
                    self.do_transport(unit)
                elif unit.job.title=='missileboat':
                    self.do_missiles(unit)
                elif unit.job.title=='corvette':
                    self.do_corvettes(unit)
                elif unit.job.title=='martyr':
                    self.go_to_friend_fighter(unit)