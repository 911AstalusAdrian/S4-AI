from Entities.DMap import DMap
from Entities.Drone import Drone
from Entities.Environment import Environment
from constants import *


class Service:
    def __init__(self, env, dmap, drone):
        self.environment = env
        self.dronemap = dmap
        self.drone = drone
        self.markWalls()
        self.gen = None
        self.visited = []

    def getServEnv(self):
        return self.environment

    def getServDMap(self):
        return self.dronemap

    def getServDrone(self):
        return self.drone

    def markWalls(self):
        walls = self.environment.readUDMSensors(self.drone.x, self.drone.y)
        self.dronemap.markDetectedWalls(walls, self.drone.x, self.drone.y)

    def generateMovements(self, x, y):
        self.visited.append([x, y])
        surf = self.environment.getEnvSurface()
        for dir in DIRECTIONS:
            nx = x + dir[0]
            ny = y + dir[1]
            if 0 <= nx < self.environment.getEnvRows() and 0 <= ny < self.environment.getEnvCols() and [nx,
                                                                                                        ny] not in self.visited and \
                    surf[nx][ny] != 1:
                yield nx, ny
                yield from self.generateMovements(nx, ny)
                yield x, y

    def moveDFS(self):
        if self.gen is None:
            self.gen = self.generateMovements(self.drone.getDroneX(), self.drone.getDroneY())
        try:
            positions = next(self.gen)
            self.drone.relocateDrone(positions)
            self.markWalls()
            return True
        except StopIteration:
            self.markWalls()
            return False
