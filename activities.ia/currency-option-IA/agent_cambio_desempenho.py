class AgentCambioDesempenho():

    def __init__(self, estado = None, funcaoAgent = None, saldoR = 0, saldoD = 0):
        super().__init__(estado, funcaoAgent)
        self.saldoR = saldoR
        self.saldoD = saldoD
        self.evoulucaoReal = []
        
    def comprar(self):
        if self.saldoReal > 0:
            self.saldoD += self.saldoReal / self.estado[-1]
            self.saldoReal = 0
        
    def vender(self):
        if self.saldoDolar > 0:
            self.saldoR += self.saldoDolar * self.estado[-1]
            self.saldoDolar = 0
        self.evolucaoReal.append(self.saldoR)

    def desempenho(self):
        print("DESEMPENHO")
        return self.evolucaoReal[-1] - self.evolucaoReal[0]