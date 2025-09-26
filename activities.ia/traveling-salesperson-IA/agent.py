import random

class Agent:
    def __init__(self, env, population_size=50, mutation_rate=0.01, generations=500):
        self.env = env
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.generations = generations

    def find_shortest_path(self):
        population = self._create_initial_population()

        for _ in range(self.generations):
            population = self._create_next_generation(population)

        best_path = min(population, key=self._calculate_path_distance)
        return best_path, self._calculate_path_distance(best_path)

    def _create_initial_population(self):
        cities = list(self.env.cities.keys())
        population = []
        for _ in range(self.population_size):
            path = random.sample(cities, len(cities))
            population.append(path)
        return population

    def _calculate_path_distance(self, path):
        total_distance = 0
        for i in range(len(path) - 1):
            total_distance += self.env.distance(path[i], path[i+1])
        total_distance += self.env.distance(path[-1], path[0])  # Return to start
        return total_distance

    def _calculate_fitness(self, path):
        return 1 / self._calculate_path_distance(path)

    def _perform_selection(self, population):
        fitness_scores = [self._calculate_fitness(path) for path in population]
        total_fitness = sum(fitness_scores)
        probabilities = [score / total_fitness for score in fitness_scores]
        
        selected_population = []
        for _ in range(len(population)):
            selected_population.append(population[random.choices(range(len(population)), probabilities)[0]])
        return selected_population

    def _perform_crossover(self, parent1, parent2):
        start_index = random.randint(0, len(parent1) - 1)
        end_index = random.randint(start_index, len(parent1) - 1)
        
        child_segment = parent1[start_index:end_index+1]
        
        remaining_cities = [city for city in parent2 if city not in child_segment]

        return child_segment + remaining_cities

    def _perform_mutation(self, path):
        if random.random() < self.mutation_rate:
            index1, index2 = random.sample(range(len(path)), 2)
            path[index1], path[index2] = path[index2], path[index1]
        return path

    def _create_next_generation(self, population):
        selected_population = self._perform_selection(population)
        next_generation = []
        
        for i in range(0, len(selected_population), 2):
            parent1 = selected_population[i]
            parent2 = selected_population[i+1] if (i+1) < len(selected_population) else selected_population[0]

            child1 = self._perform_crossover(parent1, parent2)
            child2 = self._perform_crossover(parent2, parent1)

            next_generation.append(self._perform_mutation(child1))
            next_generation.append(self._perform_mutation(child2))
            
        return next_generation
