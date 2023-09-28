import numpy as np
from random import random
import pickle
from constants import ROWS, COLUMNS


class DroneMap:
    def __init__(self, n=ROWS, m=COLUMNS):
        self.n = n
        self.m = m
        self.surface = np.zeros((self.n, self.m))

    def getN(self):
        return self.n

    def getM(self):
        return self.m

    def __str__(self):
        string = ""
        for i in range(self.n):
            for j in range(self.m):
                string = string + str(int(self.surface[i][j]))
            string = string + "\n"
        return string

    def checkDroneFitting(self, droneX, droneY):
        return 0 <= droneX < self.n and 0 <= droneY < self.m and self.surface[droneX][droneY] == 0

    def randomMap(self, fill=0.2):
        for i in range(self.n):
            for j in range(self.m):
                if random() <= fill:
                    self.surface[i][j] = 1

    def saveMap(self, num_file="test.map"):
        with open(num_file, 'wb') as f:
            pickle.dump(self, f)
            f.close()

    def loadMap(self, num_file):
        with open(num_file, "rb") as f:
            dummy = pickle.load(f)
            self.n = dummy.n
            self.m = dummy.m
            self.surface = dummy.surface
            f.close()
