class VacuumC:
    def __init__(self):
        self.position = 0
        
    def perceive(self, environment):
        return environment.state[self.position]
    
    def act(self, environment):
        perceive = self.perceive(environment)
        if perceive == "dirty":
            environment.state[self.position] = "clean"
            print(f"Cleaning position {'A' if self.position == 0 else 'B'}")
        else:
            print(f"Nothing to clean on position {'A' if self.position == 0 else 'B'}.")
        self.move()

    def move(self):
        self.position = 1 if self.position == 0 else 0
        print(f"Moving to position {'A' if self.position == 0 else 'B'}")