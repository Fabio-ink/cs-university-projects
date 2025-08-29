from Environment import Environment
from VacuumC import VacuumC

environment = Environment()
vacuumC = VacuumC()

print("Original state")
environment.show()

for _ in range(4):
    vacuumC.act(environment)

print("Final state")
environment.show()
