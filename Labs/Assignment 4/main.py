from constants import ROWS, COLUMNS
from controller import Controller
from gui import moving_drone
from domain import DroneMap
from params import Params
from tqdm import trange

if __name__ == "__main__":
    params = Params()
    battery = params.battery
    sensors = params.sensors
    drone_map = DroneMap(ROWS, COLUMNS, battery)
    drone_map.initialize_map(sensors)
    controller = Controller(drone_map)
    solution = None
    for _ in trange(params.iterations):
        current_solution = controller.iterate()
        if solution is None or solution.coverage() < current_solution.coverage():
            solution = current_solution
    print(f"The identified solution sees {solution.coverage()} cells")
    moving_drone(controller.drone_map, solution.path, battery)
