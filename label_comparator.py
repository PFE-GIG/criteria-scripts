""""
	Script for having infos on noised point cloud

	Author: Corentin Lange
	Last review: 30/03/2022

"""

# Librairies
import numpy as np
import open3d as o3d
import time
import sys
import logging


def label_comparator(input_original_pcd, input_tested_pcd):

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
        print("Plan: ", list(o_layers.keys()).index(key),
              " - Color: ",
              key,
              " - Points: ", len(o_layers[key]))

    print("\n--- Computing tested ---")

    # Dictionnary of points classified by their color - tested

    t_colors_list = np.asarray(tested_pcd.colors)

    t_layers = {str(t_colors_list[0]): [0]}

    for i in range(len(t_colors_list)):
        if(str(t_colors_list[i]) in t_layers.keys()):
            t_layers[str(t_colors_list[i])].append(i)
        else:
            t_layers[str(t_colors_list[i])] = [i]

    print("Layers: ", len(t_layers.keys()))

    for key in t_layers.keys():
        print("Plan: ", list(t_layers.keys()).index(key),
              " - Color: ",
              key,
              " - Points: ", len(t_layers[key]))

    # Doing comparisons between two models
    print("\n--- Comparing ---")

    layer_difference = len(o_layers.keys()) - len(t_layers.keys())

    print("Layers difference: ", layer_difference)

    layers_corresponding = {}

    for o_key in o_layers.keys():
        layers_corresponding[o_key] = list(t_layers.keys())[0]
        for t_key in t_layers.keys():
            diff_curr = len(set(o_layers[o_key]) -
                            set(t_layers[layers_corresponding[o_key]]))
            diff_new = len(set(o_layers[o_key]) - set(t_layers[t_key]))
            if(diff_new < diff_curr):
                layers_corresponding[o_key] = t_key

    plan_correspondance = {}

    for o_key in o_layers.keys():
        plan_correspondance[list(o_layers.keys()).index(
            o_key)] = list(t_layers.keys()).index(layers_corresponding[o_key])

    total_diff = 0
    diff_tab = []

    for key in layers_corresponding:
        difference = len(set(o_layers[key]) -
                         set(t_layers[layers_corresponding[key]]))
        diff_tab.append(difference)
        total_diff += difference
        print("Original color: ", key,
              "- New color", layers_corresponding[key],
              "- Points difference:", difference)

    print("\n TOTAL DIFF=", total_diff)

    comparator = {
        'plan_original': len(o_layers.keys()),
        'plan_original_color': o_layers.keys(),
        'plan_tested': len(t_layers.keys()),
        'plan_tested_color': t_layers.keys(),
        'plan_corresponding': plan_correspondance,
        'diff_per_plan_tab': diff_tab,
        'points_misplaced': total_diff,
        'points_total': len(original_pcd.colors)
    }
    return comparator


# input_original = sys.argv[1]
# input_tested = sys.argv[2]

# label_comparator(input_original, input_tested)
