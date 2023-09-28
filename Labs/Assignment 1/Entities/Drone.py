import pygame
from pygame.locals import *
from constants import *

class Drone:
    def __init__(self, x, y):
        self.visited = []
        self.x = x
        self.y = y

    def getDroneX(self):
        return self.x

    def getDroneY(self):
        return self.y

    def changeDirection(self, given_direction):
        self.x += given_direction[0]
        self.y += given_direction[1]

    def relocateDrone(self, coordinates):
        self.x = coordinates[0]
        self.y = coordinates[1]

    # def move(self, detectedMap):
    #     pressed_keys = pygame.key.get_pressed()
    #     if self.x > 0:
    #         if pressed_keys[K_UP] and detectedMap.surface[self.x - 1][self.y] == 0:
    #             self.x = self.x - 1
    #     if self.x < 19:
    #         if pressed_keys[K_DOWN] and detectedMap.surface[self.x + 1][self.y] == 0:
    #             self.x = self.x + 1
    #
    #     if self.y > 0:
    #         if pressed_keys[K_LEFT] and detectedMap.surface[self.x][self.y - 1] == 0:
    #             self.y = self.y - 1
    #     if self.y < 19:
    #         if pressed_keys[K_RIGHT] and detectedMap.surface[self.x][self.y + 1] == 0:
    #             self.y = self.y + 1
