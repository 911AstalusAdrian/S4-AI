class Drone:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def moveDrone(self, nx, ny):
        self.x = nx
        self.y = ny

    def getDroneX(self):
        return self.x

    def getDroneY(self):
        return self.y
