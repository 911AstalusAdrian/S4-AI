# from __future__ import annotations
# from utils import *
# import operator
# import math
# from random import sample
# from typing import List, Tuple
#
# CONVERGENCE = 0.000001
#
#
# class Point:
#     def __init__(self, label, value_1, value_2):
#         self.label = label
#         self.value_1 = value_1
#         self.value_2 = value_2
#
#     def compute_distance(self, point):
#         return math.sqrt((self.value_1 - point.value_1) ** 2 + (self.value_2 - point.value_2) ** 2)
#         # maybe manhattan distance returns some interesting results
#         # interesting, yes, useful no
#         # return abs(self.value_1 - point.value_1) + abs(self.value_2 - point.value_2)
#
#
# class Cluster:
#     def __init__(self, centroid, label):
#         self.label = label
#         self.centroid = centroid
#         self.points = []
#
#     def compute_all_distances_from_centroid(self, points):
#         return self.compute_all_distances_from_point(points, self.centroid)
#
#     def compute_all_distances_from_point(self, points, my_point):
#         distances = {}
#         for point in points:
#             distances[point] = my_point.compute_distance(point)
#         return distances
#
#     def compute_new_centroid(self):
#         center_1 = 0
#         center_2 = 0
#         for point in self.points:
#             center_1 += point.value_1
#             center_2 += point.value_2
#         center_1 /= len(self.points)
#         center_2 /= len(self.points)
#         distances = self.compute_all_distances_from_point(self.points, Point("X", center_1, center_2))
#         minimum = 999999
#         point = None
#         for key in distances.keys():
#             if minimum > distances[key]:
#                 minimum = distances[key]
#                 point = key
#         self.centroid = point
#
#     def update_label(self) -> None:
#         freq = {'A': 0, 'B': 0, 'C': 0, 'D': 0}
#         for point in self.points:
#             freq[point.label] += 1
#         self.label = max(freq.items(), key=operator.itemgetter(1))[0]
#
#     def set_points(self, points):
#         self.points = points
#
#     def compute_statistics(self, points: List[Point]) -> Tuple[float, float, float, float]:
#         '''
#         TP is the number of true positives
#         TN is the number of true negatives
#         FP is the number of false positives
#         FN is the number of false negatives
#         '''
#         TP = FP = TN = FN = 0
#         for point in self.points:
#             if point.label == self.label:
#                 TP += 1
#             else:
#                 FP += 1
#         for point in points:
#             if point not in self.points:
#                 if point.cluster.label != self.label:
#                     if point.label != self.label:
#                         TN += 1
#                     else:
#                         FN += 1
#         accuracy = (TP + TN) / (TP + TN + FP + FN)
#         precision = TP / (TP + FP)
#         rappel = TP / (TP + FN)
#         score = 2 * precision * rappel / (precision + rappel)
#         return accuracy, precision, rappel, score
#
#
# if __name__ == '__main__':
#     clusters = []
#     points = read_points()
#     random_points = sample(points, 4)
#
#     clusters.append(Cluster(random_points[0], 'A'))
#     clusters.append(Cluster(random_points[1], 'B'))
#     clusters.append(Cluster(random_points[2], 'C'))
#     clusters.append(Cluster(random_points[3], 'D'))
#
#     ok = True
#     while ok:
#         ok = False
#         for p in points:
#             optimal_cluster = p.closest_cluster(clusters)
#             if optimal_cluster.addPoint(p):
#                 ok = True
#     for i in clusters:
#         i.update_label()
#
#     print_statistics(clusters, points)
#     plot(clusters)
