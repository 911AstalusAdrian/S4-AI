import pickle
from domain import *


class Repository:
    def __init__(self):
        self.population = None
        self.droneMap = DroneMap()

    def createPopulation(self, battery, population_size, individual_size, going_back):
        self.population = Population(self.droneMap, battery, population_size, individual_size, going_back)

    def setNewPopulation(self, new_population):
        self.population = Population(self.droneMap, population=new_population)

    def loadRandomMap(self, fill_factor):
        self.droneMap.randomMap(fill_factor)

    def saveMap(self):
        with open("file.map", "wb") as file:
            pickle.dump(self.droneMap, file)

    def loadMap(self):
        with open("file.map", "rb") as file:
            self.droneMap = pickle.load(file)
