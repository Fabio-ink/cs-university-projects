class Vacuum:
	def __init__(self):
		self.position = 0
		self.battery = 100

	def show_battery(self):
		print(f'Battery: {self.battery}%')

	def state_i_am(self, ambient):
		return ambient.state[self.position]

	def action(self, ambient):
		perception = self.state_i_am(ambient)
		if perception == "Dirty":
			self.battery -= 2
			ambient.state[self.position] = "Clean"
			self.show_battery()
			print(f'Cleaning position {self.position}')
		if perception == "X":
			self.battery -= 2
			self.show_battery()	
			print('Jumping over an obstacle')
		self.move(ambient)

	def move(self, ambient):
		if self.position < 8:
			self.position += 1
			self.battery -= 2
			self.show_battery()	
			print(f'Moving to position {self.position}')	