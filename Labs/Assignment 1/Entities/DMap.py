import pygame
import numpy as np
from constants import *
from Entities.Environment import Environment
from constants import *

class DMap:
    def __init__(self):
        self.rows = ROWS
        self.cols = COLS
        self.surface = np.zeros((self.rows, self.cols))
        for i in range(self.rows):
            for j in range(self.cols):
                self.surface[i][j] = -1

    def getDMapRows(self):
        return self.rows

    def getDMapCols(self):
        return self.cols

    def getDMapSurface(self):
        return self.surface

    def markDetectedWalls(self, walls, x, y):
        for i in range(len(DIRECTIONS)):
            direction = DIRECTIONS[i]
            xi = x + direction[0]
            yi = y + direction[1]
            while 0 <= xi < self.rows and 0 <= yi < self.cols and (x - walls[UP] <= xi <= x+ walls[DOWN] and y - walls[LEFT] <= yi <= y + walls[RIGHT]):
                self.surface[xi][yi] = 0
                xi += direction[0]
                yi += direction[1]

            if 0 <= xi < self.rows and 0 <= yi < self.cols:
                self.surface[xi][yi] = 1