import csv
import math
from random import randint, random, sample
from typing import List, Tuple

import matplotlib.pyplot as plt


class Point:
    def __init__(self, label, value_1, value_2):
        self.label = label
        self.value_1 = value_1
        self.value_2 = value_2

    def compute_distance(self, point):
        return math.sqrt((self.value_1 - point.value_1) ** 2 + (self.value_2 - point.value_2) ** 2)
        # maybe manhattan distance returns some interesting results
        # interesting, yes, useful no
        # return abs(self.value_1 - point.value_1) + abs(self.value_2 - point.value_2)


class Cluster:
    def __init__(self, centroid):
        self.centroid = centroid
        self.points = []

    def compute_all_distances_from_centroid(self, points):
        return self.compute_all_distances_from_point(points, self.centroid)

    def compute_all_distances_from_point(self, points, my_point):
        distances = {}
        for point in points:
            distances[point] = my_point.compute_distance(point)
        return distances

    def compute_new_centroid(self):
        center_1 = 0
        center_2 = 0
        for point in self.points:
            center_1 += point.value_1
            center_2 += point.value_2
        center_1 /= len(self.points)
        center_2 /= len(self.points)
        distances = self.compute_all_distances_from_point(self.points, Point("X", center_1, center_2))
        minimum = 999999
        point = None
        for key in distances.keys():
            if minimum > distances[key]:
                minimum = distances[key]
                point = key
        self.centroid = point

    def set_points(self, points):
        self.points = points


# after computing all the distances, I assign a point to the closest centroid

def choose_best_cluster(all_distances, point):
    best_cluster = -1
    min_distance = 999999
    for i in range(len(all_distances)):
        if all_distances[i][point] < min_distance:
            min_distance = all_distances[i][point]
            best_cluster = i
    return best_cluster


def iteration(clusters, points, labels):
    all_distances = []
    desired_cluster = [[] for i in range(len(clusters))]
    for cluster in clusters:
        all_distances.append(cluster.compute_all_distances_from_centroid(points))

    for point in points:
        desired_cluster[choose_best_cluster(all_distances, point)].append(point)

    for i in range(len(clusters)):
        clusters[i].set_points(desired_cluster[i])
        clusters[i].compute_new_centroid()
        for point in desired_cluster[i]:
            point.label = labels[i]


def run(number_of_clusters, number_of_iterations):
    labels = ["A", "B", "C", "D", "E", "F", "G"]
    points = read_from_file()
    clusters = []
    first_centroids = sample(points, number_of_clusters)
    for i in range(number_of_clusters):
        clusters.append(Cluster(first_centroids[i]))

    for i in range(number_of_iterations):
        iteration(clusters, points, labels)

    return clusters, points


def read_from_file():
    points = []
    not_first = False
    with open('dataset.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            if not_first:
                points.append(Point(row[0], float(row[1]), float(row[2])))
            not_first = True
    return points


def put_in_file(points):
    with open('updated.csv', 'w', encoding='UTF8') as f:
        writer = csv.writer(f)
        writer.writerow(["label", "val1", "val2"])
        for point in points:
            writer.writerow([point.label, point.value_1, point.value_2])


def main():
    number_of_clusters = 4
    clusters, points = run(number_of_clusters, 100)
    put_in_file(points)
    colors = ['pink', 'limegreen', 'cyan', 'orange', 'green', 'yellow']
    for i in range(number_of_clusters):
        value_1 = []
        value_2 = []
        for point in clusters[i].points:
            value_1.append(point.value_1)
            value_2.append(point.value_2)
        plt.scatter(value_1, value_2, color=colors[i])
    for i in range(number_of_clusters):
        plt.scatter(clusters[i].centroid.value_1, clusters[i].centroid.value_2, color='black', marker="s")
    plt.show()


main()
