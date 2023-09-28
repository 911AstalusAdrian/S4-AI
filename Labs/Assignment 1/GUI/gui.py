from time import sleep
import pygame
from pygame import KEYDOWN
from constants import *
from Service.serv import Service
from Entities.DMap import DMap
from Entities.Drone import Drone
from Entities.Environment import Environment


class GUI:
    def __init__(self, service):
        self.serv = service

    def envimage(self, colour=BLUE, background=WHITE):
        env = self.serv.getServEnv()
        rows = env.getEnvRows()
        cols = env.getEnvCols()
        surf = env.getEnvSurface()
        imagine = pygame.Surface((COLSIZE * cols, ROWSIZE * rows))
        brick = pygame.Surface((COLSIZE, ROWSIZE))
        brick.fill(colour)
        imagine.fill(background)
        for i in range(rows):
            for j in range(cols):
                if surf[i][j] == 1:
                    imagine.blit(brick, (j * COLSIZE, i * ROWSIZE))
        return imagine

    def dmapimage(self):
        dmap = self.serv.getServDMap()
        rows = dmap.getDMapRows()
        cols = dmap.getDMapCols()
        surf = dmap.getDMapSurface()
        imagine = pygame.Surface((COLSIZE * cols, ROWSIZE * rows))
        brick = pygame.Surface((COLSIZE, ROWSIZE))
        empty = pygame.Surface((COLSIZE, ROWSIZE))
        empty.fill(WHITE)
        brick.fill(BLACK)
        imagine.fill(GRAYBLUE)

        for i in range(rows):
            for j in range(cols):
                if surf[i][j] == 1:
                    imagine.blit(brick, (j * COLSIZE, i * ROWSIZE))
                elif surf[i][j] == 0:
                    imagine.blit(empty, (j * COLSIZE, i * ROWSIZE))

        drona = pygame.image.load("drona.png")
        drona = pygame.transform.scale(drona, (COLSIZE, ROWSIZE))
        d = self.serv.getServDrone()
        if d.getDroneX() is not None and d.getDroneY() is not None:
            imagine.blit(drona, (d.getDroneY() * COLSIZE, d.getDroneX() * ROWSIZE))
        return imagine

    def startGUI(self):
        pygame.init()
        logo = pygame.image.load("logo32x32.png")
        pygame.display.set_icon(logo)
        pygame.display.set_caption("Drone Exploration")
        rows = self.serv.getServEnv().getEnvRows()
        cols = self.serv.getServEnv().getEnvCols()

        screen = pygame.display.set_mode((cols * COLSIZE * 2, rows * ROWSIZE))
        screen.fill(WHITE)
        screen.blit(self.envimage(), (0, 0))
        screen.blit(self.dmapimage(), (cols * COLSIZE, 0))
        pygame.display.flip()

        notDone = True

        # while notDone:
        #     for event in pygame.event.get():
        #         if event.type == pygame.QUIT:
        #             notDone = False
        #             break
        #         self.serv.moveDFS()
        #         sleep(0.1)
        #         screen.blit(self.dmapimage(), (cols * COLSIZE, 0))
        #         pygame.display.flip()

        while notDone:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
            self.serv.moveDFS()
            sleep(0.75)
            screen.blit(self.dmapimage(), (cols * COLSIZE, 0))
            pygame.display.flip()

        pygame.quit()

