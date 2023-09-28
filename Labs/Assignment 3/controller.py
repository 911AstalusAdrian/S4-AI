from repository import *
import statistics
from repository import Individual
from copy import deepcopy


class Controller:
    def __init__(self, repo):
        self.repository = repo

    def iteration(self, population_size, mutation_probability, crossover_probability):
        new_population = []
        for _ in range(population_size):
            parent1 = self.repository.population.selection()
            parent2 = self.repository.population.selection()
            offspring, _ = Individual.crossover(self.repository.droneMap, parent1, parent2, crossover_probability)
            offspring.mutate(mutation_probability)
            new_population.append(offspring)

        self.repository.setNewPopulation(new_population)

    def run(self, population_size, nr_runs, mutation_probability, crossover_probability):
        fitnessAvgList = []
        fitnessMaxList = []
        bestSol = None
        for _ in range(nr_runs):
            self.iteration(population_size, mutation_probability, crossover_probability)
            fitnessAvgList.append(statistics.mean([individual.fitness for individual in self.repository.population.population]))
            fitnessMaxList.append(max([individual.fitness for individual in self.repository.population.population]))
            for individual in self.repository.population.population:
                if bestSol is None or bestSol.fitness < individual.fitness:
                    bestSol = deepcopy(individual)

        path = bestSol.pathOfChromosome()
        return path, fitnessAvgList, fitnessMaxList, bestSol.fitness

    def solver(self, population_size, individual_size, nr_runs, battery, going_back, mutation_probability,
               crossover_probability):
        self.repository.createPopulation(battery, population_size, individual_size, going_back)
        return self.run(population_size, nr_runs, mutation_probability, crossover_probability)
