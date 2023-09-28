from copy import deepcopy
from queue import Queue
from random import *
from utils import *
import numpy as np


class Individual:
    def __init__(self, droneMap, battery, size=0, chromosome=None, goingBack=False):
        self.droneMap = droneMap
        if chromosome is None:
            chromosome = [randrange(0, 4) for _ in range(size)]
        self.chromosome = chromosome
        self.battery = battery
        self.fitness = None
        self.goingBack = goingBack

    def pathOfChromosome(self):
        drone = [self.droneMap.x, self.droneMap.y]
        distances = None
        prev = None
        if self.goingBack:
            distances = [[None for _ in range(self.droneMap.m)] for _ in range(self.droneMap.n)]
            prev = [[None for _ in range(self.droneMap.m)] for _ in range(self.droneMap.n)]
            position = (drone[0], drone[1])
            distances[drone[0]][drone[1]] = 0
            queue = Queue()
            queue.put(position)
            while not queue.empty():
                current_position = queue.get()
                for i in range(len(DIRECTIONS)):
                    new_position = (
                        current_position[0] + DIRECTIONS[i][0], current_position[1] + DIRECTIONS[i][1])
                    if 0 <= new_position[0] < self.droneMap.n and 0 <= new_position[1] < self.droneMap.m:
                        if self.droneMap.surface[new_position[0]][new_position[1]] == 0:
                            if distances[new_position[0]][new_position[1]] is None:
                                queue.put(new_position)
                                distances[new_position[0]][new_position[1]] = distances[current_position[0]][
                                                                                  current_position[1]] + 1
                                prev[new_position[0]][new_position[1]] = OPPOSITE[i]
        path = [drone]
        going_back = False
        if self.goingBack and self.battery <= 1:
            going_back = True
        for i in range(len(self.chromosome)):
            if going_back:
                if prev[drone[0]][drone[1]] is None:
                    break
                new_drone = [drone[0] + DIRECTIONS[prev[drone[0]][drone[1]]][0],
                             drone[1] + DIRECTIONS[prev[drone[0]][drone[1]]][1]]
            else:
                new_drone = [drone[0] + DIRECTIONS[self.chromosome[i]][0],
                             drone[1] + DIRECTIONS[self.chromosome[i]][1]]
            if 0 <= new_drone[0] < self.droneMap.n and 0 <= new_drone[1] < self.droneMap.m:
                if self.droneMap.surface[new_drone[0]][new_drone[1]] != 1:
                    if self.battery >= len(path):
                        drone = new_drone
                        path.append(drone)
                        if self.goingBack and len(path) + distances[drone[0]][drone[1]] >= self.battery:
                            going_back = True
        return path

    def checkFitness(self):
        path = self.pathOfChromosome()
        marked = [[0 for _ in range(self.droneMap.m)] for _ in range(self.droneMap.n)]
        for position in path:
            marked[position[0]][position[1]] = 1
            for direction in DIRECTIONS:
                sight = deepcopy(position)
                while True:
                    sight[0] += direction[0]
                    sight[1] += direction[1]
                    valid = False
                    if 0 <= sight[0] < self.droneMap.n and 0 <= sight[1] < self.droneMap.m:
                        if self.droneMap.surface[sight[0]][sight[1]] != 1:
                            valid = True

                    if not valid:
                        break

                    marked[sight[0]][sight[1]] = 1

            self.fitness = sum([sum(row) for row in marked])

    def mutate(self, mutateProbability=0.04):  # swap mutation
        if random() < mutateProbability and len(self.chromosome) >= 2:
            i = 0
            j = 0
            while i == j:
                i = randrange(len(self.chromosome))
                j = randrange(len(self.chromosome))
            self.chromosome[i], self.chromosome[j] = self.chromosome[j], self.chromosome[i]

    @staticmethod
    def crossover(droneMap, firstParent, secondParent, crossoverProbability=0.8):
        size = len(firstParent.chromosome)
        if random() < crossoverProbability:
            cutting_point = randint(0, size)
            offspring1 = Individual(droneMap, firstParent.battery,
                                    chromosome=[
                                        firstParent.chromosome[i] if i < cutting_point else secondParent.chromosome[i]
                                        for i in range(size)], goingBack=firstParent.goingBack)
            offspring2 = Individual(droneMap, firstParent.battery,
                                    chromosome=[
                                        secondParent.chromosome[i] if i < cutting_point else firstParent.chromosome[i]
                                        for i in range(size)], goingBack=firstParent.goingBack)
        else:
            offspring1, offspring2 = Individual(droneMap, firstParent.battery, size,
                                                goingBack=firstParent.goingBack), Individual(droneMap,
                                                                                             firstParent.battery,
                                                                                             size,
                                                                                             goingBack=firstParent.goingBack)

        return offspring1, offspring2


class Population:
    def __init__(self, droneMap, battery=10, populationSize=10, individualSize=10, goBack=False, population=None):
        self.populationSize = populationSize
        if population is None:
            population = [Individual(droneMap, battery, individualSize, goingBack=goBack)
                          for _ in range(populationSize)]
        self.population = population
        self.evaluate()

    def evaluate(self):
        for x in self.population:
            x.checkFitness()

    def selection(self, k=2):
        return sorted(sample(self.population, k), key=lambda x: x.fitness, reverse=True)[0]


class DroneMap:
    def __init__(self, n=MAP_LENGTH, m=MAP_LENGTH, x=None, y=None):
        self.n = n
        self.m = m
        if x is None or y is None:
            x = randrange(n)
        self.x = x
        if y is None:
            y = randrange(m)
        self.y = y
        self.surface = [[0 for _ in range(m)] for _ in range(n)]

    def randomMap(self, fill=0.2):
        self.surface = [[0 for _ in range(self.m)] for _ in range(self.n)]
        for i in range(self.n):
            for j in range(self.m):
                if random() <= fill and (i != self.x or j != self.y):
                    self.surface[i][j] = 1
