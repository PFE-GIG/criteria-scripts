""""
	Script for having infos on noised point cloud

	Author: Corentin Lange
	Last review: 28/03/2022

"""

# Librairies
import numpy as np
import open3d as o3d
import time
import sys
import logging

input_original_pcd = sys.argv[1]
input_tested_pcd = sys.argv[2]


original_pcd = o3d.io.read_point_cloud(input_original_pcd)
tested_pcd = o3d.io.read_point_cloud(input_tested_pcd)


print(f"Input original pcd: \"{input_original_pcd}\", {original_pcd}")
print(f"Input noised pcd: \"{input_tested_pcd}\", {tested_pcd}")


print("--- Computing original ---")
o_colors_list = np.asarray(original_pcd.colors)


o_layers = {str(o_colors_list[0]): [0]}

# Dictionnary of points classified by their color - original
for i in range(len(o_colors_list)):
    if(str(o_colors_list[i]) in o_layers.keys()):
        o_layers[str(o_colors_list[i])].append(i)
    else:
        o_layers[str(o_colors_list[i])] = [i]


print("Layers: ", len(o_layers.keys()))

for key in o_layers.keys():
    print("Color: ", key, "- Points: ", len(o_layers[key]))

print("\n--- Computing tested ---")

t_colors_list = np.asarray(tested_pcd.colors)

t_layers = {str(o_colors_list[0]): [0]}

# Dictionnary of points classified by their color - tested
for i in range(len(t_colors_list)):
    if(str(t_colors_list[i]) in t_layers.keys()):
        t_layers[str(t_colors_list[i])].append(i)
    else:
        t_layers[str(t_colors_list[i])] = [i]

print("Layers: ", len(t_layers.keys()))

for key in t_layers.keys():
    print("Color: ", key, "- Points: ", len(t_layers[key]))

# Doing comparisons betwen two models
print("\n--- Comparing ---")

layer_difference = len(o_layers.keys()) - len(t_layers.keys())

print("Layers difference: ", layer_difference)

layers_corresponding = {}

for o_key in o_layers.keys():
    layers_corresponding[o_key] = list(t_layers.keys())[0]
    for t_key in t_layers.keys():
        diff_curr = len(set(o_layers[o_key]) -
                        set(o_layers[layers_corresponding[o_key]]))
        diff_new = len(set(o_layers[o_key]) - set(t_layers[t_key]))
        if(diff_new < diff_curr):
            layers_corresponding[o_key] = t_key

total_diff = 0

for key in layers_corresponding:
    difference = len(set(o_layers[key]) -
                     set(t_layers[layers_corresponding[key]]))
    total_diff += difference
    print("Original color: ", key,
          "- New color", layers_corresponding[key],
          "- Points difference:", difference)

print("\n TOTAL DIFF=", total_diff)

o3d.visualization.draw_geometries([original_pcd])
