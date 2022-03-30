""""
	Script for having infos on noised point cloud

	Author: Corentin Lange
	Last review: 28/03/2022

"""

# Librairies
import numpy as np
import time
import sys
import logging
from label_comparator import label_comparator
from os import listdir
from os.path import isfile, join


input_original = sys.argv[1]
ply_folder = sys.argv[2]
logs_name = sys.argv[3]


datas = {}

ply_files = [f for f in listdir(ply_folder) if isfile(join(ply_folder, f))]

print(ply_files)


def header_writing(file_to_write):
    file_to_write.write("Input original: " + input_original + '\n')
    file_to_write.write("Files to test: ")
    for ply_file in ply_files:
        file_to_write.write("\n- " + ply_file)
    file_to_write.write("\n--------------------")


def comparator_writing(file_to_write, file_compared, data):
    file_to_write.write("\nComparison with: " + file_compared)
    file_to_write.write("\n---------")
    file_to_write.write("\nPlans original: " + str(data['plan_original']))
    file_to_write.write("\nPlans compared: " + str(data['plan_tested']))
    file_to_write.write("\nPoints misplaced: " + str(data['points_misplaced']))

    error_rate = data['points_misplaced'] / data['points_total']
    file_to_write.write("\nError rate: " + "{0:.2f}%".format(error_rate * 100))

    plan_difference = data['plan_tested'] - data['plan_original']
    file_to_write.write("\nPlans difference: " + str(plan_difference))
    if(plan_difference > 0):
        file_to_write.write(" (OVER-SEGMENTATION)")
    if(plan_difference < 0):
        file_to_write.write(" (SUB-SUGMENTATION)")

    file_to_write.write("\n--- DETAILS ---")
    file_to_write.write("\nPlan original color: ")
    for color in data['plan_original_color']:
        plan_id = str(list(data['plan_original_color']).index(color))
        file.write("\n- Plan " + plan_id + ' - Color: ' + color)

    file_to_write.write("\n\nPlan tested color: ")
    for color in data['plan_tested_color']:
        plan_id = str(list(data['plan_tested_color']).index(color))
        file.write("\n- Plan " + plan_id + ' - Color: ' + color)

    file_to_write.write("\n\nPlan correspondance:")
    for original_plan in data['plan_corresponding'].keys():
        tested_plan_corresponding = data['plan_corresponding'][original_plan]
        file.write("\n- Plan original: "
                   + str(original_plan)
                   + " - Plan tested: "
                   + str(tested_plan_corresponding))


with open("logs/" + logs_name + "_logs.txt", "w") as file:
    header_writing(file)
    for ply_file in ply_files:
        file.write('\n\n')
        file_to_open = ply_folder + '/' + ply_file
        datas = label_comparator(input_original, file_to_open)
        comparator_writing(file, ply_file, datas)
