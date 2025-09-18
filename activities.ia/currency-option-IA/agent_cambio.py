from agent import Agent
from typing import Optional

class AgentCambio(Agent):
    def __init__(self, estadoInicial=None, funcaoAgent=None):
        super().__init__(estadoInicial, funcaoAgent)
        if self.state is None:
            self.state = []
        self.observacao = 0
        self.mediaAtual = 0.0
        self.medias = []
        self.saldoReal = 1000.0
        self.saldoDolar = 0.0
        self.evolucaoReal = [self.saldoReal]

    def atualizarEstado(self, valor: float):
        self.observacao += 1
        if self.observacao == 1:
            self.mediaAtual = valor
        else:
            n = self.observacao
            self.mediaAtual = self.mediaAtual + (valor - self.mediaAtual) / n

        self.state.append(valor)
        self.medias.append(self.mediaAtual)

        portfolio_value = self.saldoReal + self.saldoDolar * valor
        self.evolucaoReal.append(portfolio_value)

    def percepcao(self, valorAtual: float):
        self.atualizarEstado(valorAtual)

    def saida(self):
        if not self.medias or not self.state:
            return (False, None, None)
        return self.functionAgent(self.medias[-1], self.state[-1])

    def comprar(self):
        if self.saldoReal > 0 and self.state:
            preco = self.state[-1]
            self.saldoDolar += self.saldoReal / preco
            self.saldoReal = 0.0

    def vender(self):
        if self.saldoDolar > 0 and self.state:
            preco = self.state[-1]
            self.saldoReal += self.saldoDolar * preco
            self.saldoDolar = 0.0

    def desempenho(self):
        if not self.evolucaoReal:
            return 0.0
        return self.evolucaoReal[-1] - self.evolucaoReal[0]