from Entities.drone import Drone
from Entities.dronemap import DroneMap
from GUI.gui import GUI
from Service.service import Service
from random import randrange


def main():
    droneMap = DroneMap()
    droneMap.randomMap()
    n = droneMap.n
    m = droneMap.m
    sx = randrange(0, n)
    sy = randrange(0, m)
    while droneMap.surface[sx][sy] == 1:
        sx = randrange(0, n)
        sy = randrange(0, m)

    drone = Drone(sx, sy)
    fx = randrange(0, n)
    fy = randrange(0, m)
    # service = Service(drone, droneMap, sx, sy, fx, fy, 1)
    # service = Service(drone, droneMap, sx, sy, fx, fy, 2)
    service = Service(drone, droneMap, sx, sy, fx, fy, 3)
    gui = GUI([service])
    print("Start X: " + str(sx) + " Start Y: " + str(sy))
    print("Finish X: " + str(fx) + " Finish Y: " + str(fy))
    gui.startGUI()


if __name__ == "__main__":
    main()
