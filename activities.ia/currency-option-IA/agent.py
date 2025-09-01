class Agent:
  def __init__(self, state=None, functionAgent=None):
    self.state = state
    self.functionAgent = functionAgent
    self.perceptionHistory = []

  def showState(self):
    return str(self.state)

  def perception(self):
    iin = input("Enter some Value")
    self.perceptionHistory.append(iin)
    
    