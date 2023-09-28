from random import randint
from Entities.Environment import Environment
from Entities.Drone import Drone
from Entities.DMap import DMap
from GUI.gui import GUI
from Service.serv import Service
from constants import *

if __name__ == "__main__":
    env = Environment()
    env.randomMap()
    # env.loadEnvironment("test2.map")

    dmap = DMap()

    x = randint(0, ROWS)
    y = randint(0, COLS)
    drone = Drone(x, y)

    serv = Service(env, dmap, drone)
    gui = GUI(serv)
    gui.startGUI()