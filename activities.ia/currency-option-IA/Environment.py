class Environment:
  def __init__(self, initialState=None):
    self.state = initialState
    self.objectsOnEnvironment = []
    self.agents = []

  def perception(self, agent):
    return None

  def addAgent(self,agent):
    self.agents.append(agent)