""""
	Script for having infos on noised point cloud

	Author: Corentin Lange
	Last review: 30/03/2022

"""

# Librairies
from unittest.util import _count_diff_all_purpose
import numpy as np
import open3d as o3d
import time
import sys
import logging

from pyrsistent import b

treshold = 0.9


def points_color_classification(colors_list):
    '''
    Take a list of points color and
    Return a dictionnary as :
    plans_dict = {
                'color_1': [points_ids]
                ...
        }
    '''
    plans_dict = {str(colors_list[0]): [0]}
    for point_id in range(1, len(colors_list)):
        if(str(colors_list[point_id]) in plans_dict.keys()):
            plans_dict[str(colors_list[point_id])].append(point_id)
        else:
            plans_dict[str(colors_list[point_id])] = [point_id]
    return plans_dict


def display_color_points_dict(plans_dict):
    print("Layers: ", len(plans_dict.keys()))

    for key in plans_dict.keys():
        print("Plan: ", list(plans_dict.keys()).index(key),
              " - Color: ", key,
              " - Points: ", len(plans_dict[key]))


def compute_matrice_error(o_plans, t_plans):
    matrice_error = np.array()
    for key in o_plans.keys():
        o_plan = o_plans[key]
        row_error_rate = []
        for key in t_plans.keys():
            t_plan = t_plans[key]
            row_error_rate.append(compute_points_difference(o_plan, t_plan))

        matrice_error.vstack(row_error_rate)

    return matrice_error


def compute_plans_correspondance(o_plans, t_plans):
    '''
    '''
    plans_corresponding = {}
    for o_color in o_plans.keys():
        plans_corresponding[o_color] = list(t_plans.keys())[0]
        for t_color in t_plans.keys():
            if t_color != '[0. 0. 0.]':							# If the color is black, it's just error
                diff_curr = len(set(o_plans[o_color]) -
                                set(t_plans[plans_corresponding[o_color]]))
                diff_new = len(
                    set(o_plans[o_color]) - set(t_plans[t_color]))
                if(diff_new < diff_curr):
                    plans_corresponding[o_color] = t_color

    return plans_corresponding


def compute_points_difference(plan_a, plan_b):
    return set(plan_a).difference(set(plan_b))


def label_comparator(input_original_pcd, input_tested_pcd):

    original_pcd = o3d.io.read_point_cloud(input_original_pcd)
    tested_pcd = o3d.io.read_point_cloud(input_tested_pcd)

    print(f"Input original pcd: \"{input_original_pcd}\", {original_pcd}")
    print(f"Input noised pcd: \"{input_tested_pcd}\", {tested_pcd}")

    print("--- Computing original ---")
    # Points classified by their color - original
    o_colors_list = np.asarray(original_pcd.colors)
    o_plans = points_color_classification(o_colors_list)
    display_color_points_dict(o_plans)

    print("\n--- Computing tested ---")
    # Points classified by their color - tested
    t_colors_list = np.asarray(tested_pcd.colors)
    t_plans = points_color_classification(t_colors_list)
    display_color_points_dict(t_plans)

    print("\n--- Comparing ---")
    # Doing comparisons between two pcd
    points_error = set()
    plan_difference = len(o_plans.keys()) - len(t_plans.keys())
    plan_correspondance = {}

    print("Plans difference: ", plan_difference)

    black_key = '[0. 0. 0.]'						# Label for unlabelled points
    if black_key in o_plans.keys():
        points_error = compute_points_difference(
            t_plans[black_key], o_plans[black_key])
    else:
        points_error = points_error.union(set(t_plans[black_key]))

    # If only points no labeled

    if len(points_error) != len(t_colors_list):
        plan_correspondance = compute_plans_correspondance(o_plans, t_plans)

    difference_tab = []

    for key in plan_correspondance:
        o_plan = o_plans[key]
        t_plan = t_plans[plan_correspondance[key]]

        points_difference = compute_points_difference(o_plan, t_plan)
        difference_tab.append(len(points_difference))

        points_error = points_error.union(points_difference)

        o_plan_index = list(o_plans.keys()).index(key)
        t_plan_index = list(t_plans.keys()).index(plan_correspondance[key])
        print("Original plan: ", o_plan_index,
              "- New plan", t_plan_index,
              "- Points difference:", len(points_difference))

    print("\n TOTAL DIFF=", len(points_error))

    comparator = {
        'plan_original': len(o_plans.keys()),
        'plan_original_color': o_plans.keys(),
        'plan_tested': len(t_plans.keys()),
        'plan_tested_color': t_plans.keys(),
        'plan_corresponding': plan_correspondance,
        'diff_per_plan_tab': difference_tab,
        'points_misplaced': len(points_error),
        'points_total': len(original_pcd.colors)
    }
    return comparator


# input_original = sys.argv[1]
# input_tested = sys.argv[2]

# label_comparator(input_original, input_tested)
