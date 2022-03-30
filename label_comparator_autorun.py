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

    plan_difference = data['plan_original'] - data['plan_tested']
    file_to_write.write("\nPlans difference: " + plan_difference)


with open("logs/logs.txt", "w") as file:
    header_writing(file)
    for ply_file in ply_files:
        file.write('\n\n')
        file_to_open = ply_folder + '/' + ply_file
        datas = label_comparator(input_original, file_to_open)
        comparator_writing(file, ply_file, datas)
