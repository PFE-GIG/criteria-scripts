""""
	Script for having infos on noised point cloud

	Author: Corentin Lange
	Last review: 01/03/2022

"""

# Librairies
import numpy as np
import open3d as o3d
import time
import sys
import logging

input_original_pcd = sys.argv[1]
input_noised_pcd = sys.argv[2]


original_pcd = o3d.io.read_point_cloud(input_original_pcd)
noised_pcd = o3d.io.read_point_cloud(input_noised_pcd)

print(f"Input original pcd: \"{input_original_pcd}\", {original_pcd}")
print(f"Input noised pcd: \"{input_noised_pcd}\", {noised_pcd}")


def distance_points(p1, p2):
    distance = (p1[0] - p2[0])**2 + (p1[1] - p2[1])**2 + (p1[2] - p2[2])**2
    return distance


distances = []

for point in range(len(original_pcd.points)):
    distances.append(distance_points(
        original_pcd.points[point], noised_pcd.points[point]))

max_distance = max(distances)
min_distance = min(distances)
mean_distance = sum(distances)/len(distances)
var_distance = sum((distance-mean_distance) **
                   2 for distance in distances) / len(distances)

print(f"\nDistance error\n---")
print(f"Mean: {max_distance}")
print(f"Var: {var_distance}")
print(f"Min:  {min_distance}")
print(f"Max: {mean_distance}")
