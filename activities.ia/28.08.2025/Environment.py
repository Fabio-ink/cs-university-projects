class Environment:
    def __init__(self):
        self.state = ["clean", "dirty"]

    def show(self):
        print(f"Environment: {self.state}")