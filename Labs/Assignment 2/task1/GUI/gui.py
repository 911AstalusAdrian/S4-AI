import pickle, pygame, time
from pygame.locals import *
from random import random, randint
import numpy as np
from constants import *


class GUI:
    def __init__(self, service):
        self.service = service

    def startGUI(self):
        pygame.init()
        logo = pygame.image.load("logo32x32.png")
        pygame.display.set_icon(logo)
        pygame.display.set_caption("Path in simple environment")
        screen = pygame.display.set_mode((self.service[0].dMap.m * COL_SIZE, self.service[0].dMap.n * ROW_SIZE))
        screen.fill(WHITE)
        while any(not service.finished for service in self.service):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

            for service in self.service:
                if not service.finished:
                    service.droneNextMove()
            screen.blit(self.droneMapImage(), (0, 0))
            pygame.display.flip()
            time.sleep(0.1)
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                    running = False
        pygame.quit()

    def droneMapImage(self, colour=BLUE, background=WHITE):
        n = self.service[0].dMap.n
        m = self.service[0].dMap.m

        imagine = pygame.Surface((m * COL_SIZE, n * ROW_SIZE))
        brick = pygame.Surface((COL_SIZE, ROW_SIZE))
        brick.fill(colour)
        imagine.fill(background)
        for i in range(n):
            for j in range(m):
                if self.service[0].dMap.surface[i][j] == 1:
                    imagine.blit(brick, (j * COL_SIZE, i * ROW_SIZE))

        for path in self.service[0].mode:
            mark = pygame.Surface((COL_SIZE, ROW_SIZE))
            mark.fill(BLACK)
            imagine.blit(mark, (path[1] * COL_SIZE, path[0] * ROW_SIZE))

        start = pygame.Surface((COL_SIZE, ROW_SIZE))
        start.fill(GREEN)
        imagine.blit(start, (self.service[0].inY * COL_SIZE, self.service[0].inX * ROW_SIZE))

        end = pygame.Surface((COL_SIZE, ROW_SIZE))
        end.fill(RED)
        imagine.blit(end, (self.service[0].finY * COL_SIZE, self.service[0].finX * ROW_SIZE))

        drone = pygame.image.load("drona.png")
        imagine.blit(drone, (self.service[0].drone.getDroneY() * COL_SIZE, self.service[0].drone.getDroneX() * ROW_SIZE))

        return imagine
