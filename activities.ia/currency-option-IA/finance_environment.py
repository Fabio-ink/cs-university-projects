from environment import Environment

class FinanceEnvironment(Environment):
    def __init__(self, estado):
        super().__init__(estado)

    def executaAmbiente(self):
        for est in self.state:
            for ag in self.agents:
                ag.percepcao(est)
                acaoComprar = ag.saida()
                if isinstance(acaoComprar, tuple) and len(acaoComprar) > 0:
                    comprar_flag = acaoComprar[0]
                else:
                    comprar_flag = bool(acaoComprar)
                if comprar_flag:
                    if hasattr(ag, "comprar"):
                        ag.comprar()
                else:
                    if hasattr(ag, "vender"):
                        ag.vender()
                
    def desempenhoAgentes(self):
        desempenhos = []
        for i, ag in enumerate(self.agents):
            if hasattr(ag, "desempenho"):
                desempenhos.append((i, ag.desempenho()))
            else:
                desempenhos.append((i, None))
        return desempenhos
