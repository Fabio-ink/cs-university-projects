from environment import Environment
from agent import Agent

def main():
    cities = {
        "Archeon": (0, 0),
        "Bravos": (1, 5),
        "Casterly": (2, 3),
        "Dorne": (5, 6),
        "Essos": (7, 1),
        "Falkreath": (8, 4)
    }

    env = Environment(cities)
    agent = Agent(env, population_size=100, generations=1000, mutation_rate=0.01)

    print("Executando o algoritmo genético para encontrar o caminho mais curto...")
    path, distance = agent.find_shortest_path()

    print(f"Melhor caminho encontrado: {path}")
    print(f"Distância: {distance}")

if __name__ == "__main__":
    main()