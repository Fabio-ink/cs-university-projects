from vacuumC import Vacuum
from environment import Environment

environment = Environment()
vacuum = Vacuum()

print('Initial state')
environment.show()

for _ in range(9):
	vacuum.action(environment)

environment.show()