from agent import Agent
from typing import Optional

class AgentCambio(Agent):
    def __init__(self, estadoInicial=None, funcaoAgent=None):
        # repassa state e functionAgent para a classe base Agent
        super().__init__(estadoInicial, funcaoAgent)
        # garante que state seja uma lista mutável
        if self.state is None:
            self.state = []
        self.observacao = 0
        self.mediaAtual = 0.0
        self.medias = []
        # saldo para simulação de compra/venda
        self.saldoReal = 1000.0   # moeda local (BRL)
        self.saldoDolar = 0.0     # moeda estrangeira (USD)
        self.evolucaoReal = [self.saldoReal]

    def atualizarEstado(self, valor: float):
        self.observacao += 1
        if self.observacao == 1:
            self.mediaAtual = valor
        else:
            # atualização incremental da média (n = número de observações)
            n = self.observacao
            self.mediaAtual = self.mediaAtual + (valor - self.mediaAtual) / n

        # armazena valor e média
        self.state.append(valor)
        self.medias.append(self.mediaAtual)

        # registra o valor atual do portfólio em reais (saldoReal + saldoDolar * preço atual)
        portfolio_value = self.saldoReal + self.saldoDolar * valor
        self.evolucaoReal.append(portfolio_value)

    def percepcao(self, valorAtual: float):
        self.atualizarEstado(valorAtual)

    def saida(self):
        # usa a função associada ao agente (functionAgent) com ordem (media, valor)
        if not self.medias or not self.state:
            return (False, None, None)
        return self.functionAgent(self.medias[-1], self.state[-1])

    # métodos de trading simples
    def comprar(self):
        # compra todo saldoReal em dólares ao preço atual (último valor de state)
        if self.saldoReal > 0 and self.state:
            preco = self.state[-1]
            self.saldoDolar += self.saldoReal / preco
            self.saldoReal = 0.0
            # registra pós-compra
            self.evolucaoReal.append(self.saldoReal)

    def vender(self):
        # vende todo saldoDolar ao preço atual
        if self.saldoDolar > 0 and self.state:
            preco = self.state[-1]
            self.saldoReal += self.saldoDolar * preco
            self.saldoDolar = 0.0
            # registra pós-venda
            self.evolucaoReal.append(self.saldoReal)

    def desempenho(self):
        # retorno em reais: diferença entre o último e o primeiro registro de evolução
        if not self.evolucaoReal:
            return 0.0
        return self.evolucaoReal[-1] - self.evolucaoReal[0]