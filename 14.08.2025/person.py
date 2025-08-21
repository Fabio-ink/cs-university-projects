class Person:
    def __init__(self, name, height, age, weight):
        self.name = name
        self.age = age
        self.height = height
        self.weight = weight

    def get_imc(self):
        return self.weight / (self.height * self.height)

    def is_legal_age(self):
        return self.age >= 18