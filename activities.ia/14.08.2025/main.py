from person import Person

people = []
value = 0

while value <= 0:
    value = int(input("Quantas pessoas você deseja calcular o IMC: "))

for i in range(value):
    print(f"\n----- Pessoa Nº{i+1} -----")
    name = str(input("Nome: "))
    height = float(input("Altura: "))
    age = int(input("Idade: "))
    weight = float(input("Peso: "))
    person = Person(name, height, age, weight)
    people.append(person)

print("\n-----IMCs-----")
for p in people:
    print(f"Nome: {p.name}, É maior de idade: {p.is_legal_age()},  IMC: {p.get_imc():.1f}")