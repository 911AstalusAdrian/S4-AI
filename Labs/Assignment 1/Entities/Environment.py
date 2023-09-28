import pickle
from random import random
import numpy as np
from constants import *


class Environment:
    def __init__(self):
        self.rows = ROWS
        self.cols = COLS
        self.surface = np.zeros((self.rows, self.cols))

    # @property
    # def rows(self):
    #     return self._rows
    #
    # @property
    # def cols(self):
    #     return self._cols
    #
    # @property
    # def surface(self):
    #     return self._surface
    #
    # @surface.setter
    # def surface(self, value):
    #     self._surface = value
    #
    # @cols.setter
    # def cols(self, value):
    #     self._cols = value
    #
    # @rows.setter
    # def rows(self, value):
    #     self._rows = value

    def getEnvRows(self):
        return self.rows

    def getEnvCols(self):
        return self.cols

    def getEnvSurface(self):
        return self.surface

    def randomMap(self, fill=0.2):
        for i in range(self.rows):
            for j in range(self.cols):
                if random() <= fill:
                    self.surface[i][j] = 1

    def __str__(self):
        string = ""
        for i in range(self.rows):
            for j in range(self.cols):
                string = string + str(int(self.surface[i][j]))
            string = string + "\n"
        return string

    def readUDMSensors(self, x, y):
        readings = [0, 0, 0, 0]
        for i in range(len(DIRECTIONS)):
            dir = DIRECTIONS[i]
            curr_dir = DIRECTIONS_ORDER[i]
            nx = x + dir[0]
            ny = y + dir[1]
            while 0 <= nx < self.rows and 0 <= ny < self.cols and self.surface[nx][ny] == 0:
                nx += dir[0]
                ny += dir[1]
                readings[curr_dir] += 1
        return readings

    def saveEnvironment(self, numFile):
        with open(numFile, 'wb') as f:
            pickle.dump(self, f)
            f.close()

    def loadEnvironment(self, numfile):
        with open(numfile, "rb") as f:
            dummy = pickle.load(f)
            self.rows = dummy.getEnvRows()
            self.cols = dummy.getEnvCols()
            self.surface = dummy.getEnvSurface()
            f.close()


