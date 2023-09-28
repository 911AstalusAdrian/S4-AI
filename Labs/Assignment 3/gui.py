from pygame.locals import *
import pygame
import time
from utils import WHITE, GREEN, BLUE, DIRECTIONS
from domain import *


def initPyGame(dimension):
    pygame.init()
    logo = pygame.image.load("logo32x32.png")
    pygame.display.set_icon(logo)
    pygame.display.set_caption("drone exploration with AE")
    screen = pygame.display.set_mode(dimension)
    screen.fill(WHITE)
    return screen


def closePyGame():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
    pygame.quit()


def movingDrone(currentMap, path, speed=1, markSeen=True):
    screen = initPyGame((currentMap.n * 20, currentMap.m * 20))
    drona = pygame.image.load("drona.png")
    for i in range(len(path)):
        screen.blit(image(currentMap), (0, 0))
        if markSeen:
            brick = pygame.Surface((20, 20))
            brick.fill(GREEN)
            for j in range(i + 1):
                for direction in DIRECTIONS:
                    x = path[j][0]
                    y = path[j][1]
                    while ((0 <= x + direction[0] < currentMap.n and
                            0 <= y + direction[1] < currentMap.m) and
                           currentMap.surface[x + direction[0]][y + direction[1]] != 1):
                        x = x + direction[0]
                        y = y + direction[1]
                        screen.blit(brick, (y * 20, x * 20))
        screen.blit(drona, (path[i][1] * 20, path[i][0] * 20))
        pygame.display.flip()
        time.sleep(speed)
    closePyGame()


def droneOnly(currentMap, dronePosition):
    screen = initPyGame((currentMap.n * 20, currentMap.m * 20))
    screen.blit(image(currentMap), (0,0))
    drone = pygame.image.load("drona.png")
    screen.blit(drone, (dronePosition[1] * 20, dronePosition[0] * 20))
    for _ in range(1000):
        pygame.display.flip()
    closePyGame()


def image(currentMap, colour=BLUE, background=WHITE):
    imagine = pygame.Surface((currentMap.n * 20, currentMap.m * 20))
    brick = pygame.Surface((20, 20))
    brick.fill(colour)
    imagine.fill(background)
    for i in range(currentMap.n):
        for j in range(currentMap.m):
            if currentMap.surface[i][j] == 1:
                imagine.blit(brick, (j * 20, i * 20))
    return imagine
