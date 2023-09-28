import math
import random
from random import *
from queue import PriorityQueue
from constants import DIRECTIONS
from Entities.dronemap import *


class Service:
    def __init__(self, drone, drone_map, initialX, initialY, finalX, finalY, search_type):
        self.dMap = drone_map
        self.drone = drone
        self.inX = initialX
        self.inY = initialY
        self.finX = finalX
        self.finY = finalY
        self.mode = None
        if search_type == 1:
            self.mode = self.greedy()
        elif search_type == 2:
            self.mode = self.aStar()
        else:
            self.mode = self.simulatedAnnealing()

        self.iterator = iter(self.mode)
        self.incomplete_path = [next(self.iterator)]
        self.finished = False

    def bestFirstSeach(self, f):
        inf = self.dMap.getN() + self.dMap.getM()
        distances = [[inf for _ in range(self.dMap.m)] for _ in range(self.dMap.n)]
        value = [[0 for _ in range(self.dMap.m)] for _ in range(self.dMap.n)]
        prev = [[(i, j) for j in range(self.dMap.m)] for i in range(self.dMap.n)]
        visited = [[False for _ in range(self.dMap.m)] for _ in range(self.dMap.n)]

        distances[self.inX][self.inY] = 0
        visited[self.inX][self.inY] = True

        pQueue = PriorityQueue()
        pQueue.put((0, (self.inX, self.inY)))

        while not pQueue.empty():
            item = pQueue.get()
            if value[item[1][0]][item[1][1]] != item[0]:
                continue
            if item == (self.finX, self.finY):
                break
            for direction in DIRECTIONS:
                neighbour = (item[1][0] + direction[0], item[1][1] + direction[1])
                if self.dMap.checkDroneFitting(*neighbour) and not visited[neighbour[0]][neighbour[1]]:
                    prev[neighbour[0]][neighbour[1]] = item[1]
                    visited[neighbour[0]][neighbour[1]] = True

                    distances[neighbour[0]][neighbour[1]] = distances[item[1][0]][item[1][1]] + 1
                    value[neighbour[0]][neighbour[1]] = f(neighbour, distances, self.finX, self.finY)
                    pQueue.put((f(neighbour, distances, self.finX, self.finY), neighbour))
        if prev[self.finX][self.finY] == (self.finX, self.finY):
            return []

        self.path = []
        path = []
        now = self.finX, self.finY
        while now != (self.inX, self.inY):
            self.path.append(now)
            path.append(now)
            now = prev[now[0]][now[1]]
        path.append(now)
        self.path.append(now)
        return list(reversed(path))

    @staticmethod
    def __dist(p1, p2):
        return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

    def greedy(self):
        return self.bestFirstSeach(
            lambda neighbour, distances, fx, fy: self.__dist((fx, fy), neighbour)
        )

    def aStar(self):
        return self.bestFirstSeach(
            lambda neighbour, distances, fx, fy: distances[neighbour[0]][neighbour[1]] + self.__dist((fx, fy),
                                                                                                     neighbour)
        )

    def simulatedAnnealing(self, kmax=1000, initialTemp=20):
        pair = (self.drone.getDroneX(), self.drone.getDroneY())
        path = [pair]
        for k in range(kmax):
            if pair == (self.finX, self.finY):
                return path
            newTemp = initialTemp / (k + 1)
            neighbours = []
            for direction in DIRECTIONS:
                newPair = (pair[0] + direction[0], pair[1] + direction[1])
                if self.dMap.checkDroneFitting(*newPair):
                    neighbours.append(newPair)
            neighbour = choice(neighbours)
            delta = self.__dist(neighbour, (self.finX, self.finY)) - self.__dist(pair, (self.finX, self.finY))

            prob = math.exp(-delta / newTemp)
            # print(delta, prob, uniform(0, 1))
            if uniform(0, 1) < prob:
                pair = neighbour
                path.append(pair)
        return path

    def droneNextMove(self):
        try:
            self.incomplete_path.append(new_pos := next(self.iterator))
            self.drone.moveDrone(*new_pos)
        except StopIteration:
            self.finished = True
