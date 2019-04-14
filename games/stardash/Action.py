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
        for missle in self.player.opponent.projectiles:
            if ((missile.x-corvette.x)**2+(missile.y-corvette.y)**2)**.5 <= corvette.job.range:
                corvette.shootdown(missle)
                break
                    
    def mine_neighbors(self, unit):
        if unit.mythicite+unit.legendarium+unit.rarium+unit.genarium<unit.job.carry_limit:
            neighbors=[]
            for body in self.game.bodies:
                if body.body_type=='asteroid':
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
        if not corvette.acted:
            self.shootNonShielded(corvette)
        
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