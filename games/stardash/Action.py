class Action:

    def __init__(self, p, g):
        self.player = p
        self.game = g

    def transfer_goods(self, transport):
        for unit in self.player.units:
            if (transport.x-unit.x)**2+(transport.y-unit.y)**2 <= transport.job.range:
                if unit.mythicite>0 and transport.mythicite+transport.legendarium+transport.rarium+transport.genarium<transport.job.carry_limit:
                    transport.transfer(unit,-1,'mythicite')
                if unit.legendarium>0 and transport.mythicite+transport.legendarium+transport.rarium+transport.genarium<transport.job.carry_limit:
                    transport.transfer(unit,-1,'legendarium')
                if unit.rarium>0 and transport.mythicite+transport.legendarium+transport.rarium+transport.genarium<transport.job.carry_limit:
                    transport.transfer(unit,-1,'rarium')
                if unit.genarium>0 and transport.mythicite+transport.legendarium+transport.rarium+transport.genarium<transport.job.carry_limit:
                    transport.transfer(unit,-1,'genarium')

    def mine_neighbors(self, unit):
        if unit.mythicite+unit.legendarium+unit.rarium+unit.genarium<unit.job.carry_limit:
            neighbors=[]
            for body in self.game.bodies:
                if body.body_type=='asteroid':
                    if (body.x-unit.x)**2+(body.y-unit.y)**2 <= unit.job.range:
                        neighbors.append(body)
            myths=[]
            legends=[]
            rares=[]
            genes=[]
            nones=[]
            for neighbor in neighbors:
                if neighbor.material_type=='mythicite':
                    myths.append(neighbor)
                elif neighbor.material_type=='legendarium':
                    legends.append(neighbor)
                elif neighbor.material_type=='rarium':
                    rares.append(neighbor)
                elif neighbor.material_type=='genarium':
                    genes.append(neighbor)
                else:
                    nones.append(neighbor)
            if len(myths)>0:
                unit.mine(myths[0])
            elif len(legends)>0:
                unit.mine(legends[0])
            elif len(rares)>0:
                unit.mine(rares[0])
            elif len(genes)>0:
                unit.mine(genes[0])

    def do_miner(self, miner):
        self.mine_neighbors(miner)

    def do_transport(self, transport):
        self.transfer_goods(transport)

    def do_actions(self):
        for unit in self.player.units:
            if not unit.acted:
                if unit.job.title=='miner':
                    self.do_miner(unit)
                elif unit.job.title=='transport':
                    self.do_transport(unit)