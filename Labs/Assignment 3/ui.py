import statistics

from gui import *
from controller import *
from repository import *
from domain import *
from matplotlib import pyplot


def main():
    repo = Repository()
    controller = Controller(repo)
    loadedMap = False
    parametersSetup = False
    programSolved = False
    populationSize = None
    individualSize = None
    nrRuns = None
    battery = None
    goingBack = None
    path = None
    fitnessAvg = None
    fitnessMax = None
    mutationProbability = None
    crossoverProbability = None
    speed = None

    while True:
        print("1. Map Options")
        print("2. EA Options")
        print("0. Exit")
        choice1 = input("> ")
        if choice1 == "1":
            print("1. Random Map")
            print("2. Load Map")
            print("3. Save Map")
            choice2 = input("> ")
            if choice2 == "1":
                loadedMap = True
                fill = input("Fill Factor: ")
                if len(fill) != 0:
                    fill = float(fill)
                else:
                    fill = 0.2
                controller.repository.loadRandomMap(fill)
            elif choice2 == "2":
                loadedMap = True
                controller.repository.loadMap()
            elif choice2 == "3":
                if loadedMap:
                    controller.repository.saveMap()
                else:
                    print("Map not yet loaded")
            else:
                print("Invalid choice\n")
        elif choice1 == "2":
            if not loadedMap:
                print("Map not yet loaded")
                continue
            print("1. Set up parameters")
            print("2. Run solver (once)")
            print("3. Run solver (+ mean and standard dev)")
            print("4. View stats")
            print("5. View drone path")
            choice2 = input("> ")
            if choice2 == "1":
                parametersSetup = True
                programSolved = False

                # battery
                battery = input("Battery (30): ")
                if len(battery) != 0:
                    battery = int(battery)
                else:
                    battery = 30

                # going back
                goingBack = input("Go Back? (y/n): ")
                goingBack = goingBack == "y"

                # population size
                populationSize = input("Population size (100): ")
                if len(populationSize) != 0:
                    populationSize = int(populationSize)
                else:
                    populationSize = 100

                # individual size
                individualSize = input(f"Individual size ({battery * 2}): ")
                if len(individualSize) != 0:
                    individualSize = int(individualSize)
                else:
                    individualSize = battery * 2

                # nr of runs
                nrRuns = input("Number of runs (100): ")
                if len(nrRuns) != 0:
                    nrRuns = int(nrRuns)
                else:
                    nrRuns = 100

                # mutation probability
                mutationProbability = input("Mutation probability (0.05): ")
                if len(mutationProbability) != 0:
                    mutationProbability = float(mutationProbability)
                else:
                    mutationProbability = 0.05

                # crossover probability
                crossoverProbability = input("Crossover probability (0.8)")
                if len(crossoverProbability) != 0:
                    crossoverProbability = float(crossoverProbability)
                else:
                    crossoverProbability = 0.8

                # drone speed
                speed = input("Drone speed (0.5): ")
                if len(speed) != 0:
                    speed = float(speed)
                else:
                    speed = 0.5
            elif choice2 == "2":
                if not parametersSetup:
                    print("Parameters are not set up")
                    continue

                if programSolved:
                    print("Program is solved")
                    continue

                start = time.time()
                path, fitnessAvg, fitnessMax, solFitness = controller.solver(populationSize, individualSize,
                                                                             nrRuns, battery, goingBack,
                                                                             mutationProbability, crossoverProbability)
                end = time.time()
                print(f"Evolutionary algorithm ran in {end - start} seconds")
                print(f"It found a run with {len(path) - 1} moves and discovered {solFitness} cells")
                programSolved = True
            elif choice2 == "3":
                if not parametersSetup:
                    print("Parameters are not set up")
                    continue

                values = []
                for i in range(30):
                    seed(i)
                    _, _, _, fitness = controller.solver(populationSize, individualSize,
                                                         nrRuns, battery, goingBack,
                                                         mutationProbability, crossoverProbability)
                    values.append(fitness)
                avg = statistics.mean(values)
                stdev = statistics.stdev(values)
                print(f"Average solution fitness was found to be {avg} with a stdev of {stdev}")
                pyplot.plot(values)
                pyplot.ylim([0, None])
                pyplot.savefig("checker.png")
                pyplot.close()
            elif choice2 == "4":
                if not programSolved:
                    print("Program not solved yet")
                    continue

                pyplot.plot(fitnessAvg)
                pyplot.plot(fitnessMax)
                pyplot.savefig("fitness.png")
                pyplot.close()
            elif choice2 == "5":
                movingDrone(controller.repository.droneMap, path, speed=speed)
            else:
                print("Invalid choice")

        elif choice1 == "0":
            break
        else:
            print("Invalid choice")


if __name__ == "__main__":
    main()

