from agent import Agent

class AgentCambioDesempenho(Agent):

    def __init__(self, estadoInicial = None, funcaoAgent = None, saldoReal = 1000.0, saldoDolar = 0.0):
        super().__init__(estadoInicial, funcaoAgent)
        if self.state is None:
            self.state = []
        self.saldoReal = saldoReal
        self.saldoDolar = saldoDolar
        self.evolucaoReal = [self.saldoReal]

    def percepcao(self, valorAtual: float):
        self.state.append(valorAtual)
        portfolio_value = self.saldoReal + self.saldoDolar * valorAtual
        self.evolucaoReal.append(portfolio_value)
        
    def comprar(self):
        if self.saldoReal > 0:
            preco = self.state[-1]
            self.saldoDolar += self.saldoReal / preco
            self.saldoReal = 0.0
        
    def vender(self):
        if self.saldoDolar > 0:
            preco = self.state[-1]
            self.saldoReal += self.saldoDolar * preco
            self.saldoDolar = 0

    def desempenho(self):
        if not self.evolucaoReal or len(self.evolucaoReal) < 2:
            return 0.0
        return self.evolucaoReal[-1] - self.evolucaoReal[0]