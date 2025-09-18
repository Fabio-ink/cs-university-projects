class Agent:
  def __init__(self, estadoInicial=None, funcaoAgent=None):
    self.state = estadoInicial
    self.functionAgent = funcaoAgent

  def percepcao(self, ambiente_state):
    raise NotImplementedError("O método 'percepcao' deve ser implementado pela subclasse.")

  def saida(self):
    raise NotImplementedError("O método 'saida' deve ser implementado pela subclasse.")