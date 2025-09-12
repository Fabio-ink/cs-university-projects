class Environment:
	def __init__(self):
		self.state = ["Dirty", "Clean", "X", "Dirty", "X", "Dirty", "Dirty", "Clean", "X"]

	def show(self):
		print(f'Environment: {self.state}')