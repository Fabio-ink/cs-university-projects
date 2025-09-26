import math

class Environment:
    def __init__(self, cities):
        self.cities = cities

    def distance(self, city1, city2):
        x1, y1 = self.cities[city1]
        x2, y2 = self.cities[city2]
        return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)
