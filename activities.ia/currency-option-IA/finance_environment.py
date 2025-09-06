from environment import Environment

class FinanceEnvironment(Environment):
    def __init__(self, estado):
        super().__init__(estado)
    
    def adicionaAgente(self, agent):
        # compatibilidade com main.py (nome em português)
        self.addAgent(agent)

    def executaAmbiente(self):
        # percorre a série temporal armazenada em self.state (classe base)
        for est in self.state:
            for ag in self.agents:
                # pede ao agente que perceba o valor (ag.percepcao deve atualizar estado interno)
                ag.percepcao(est)
                # obtém ação do agente; espera tupla (comprar_bool, valor, media) ou similar
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

