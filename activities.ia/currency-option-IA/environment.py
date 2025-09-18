class Environment:
  def __init__(self, estado=None):
    self.state = estado if estado is not None else []
    self.agents = []

  def adicionaAgente(self, agent):
    self.agents.append(agent)

  def executaAmbiente(self):
    raise NotImplementedError("O método 'executaAmbiente' deve ser implementado pela subclasse.")