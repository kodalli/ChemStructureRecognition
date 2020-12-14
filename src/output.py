import cv2 as cv
import numpy as np
from detectCycle import Graph
import math


def draw_molecule(corners_array, graph: Graph, img):
    cycles = graph.get_all_cycles()

    if cycles is not None:
        draw_first_cycle(cycles[0], corners_array, img)


def draw_first_cycle(cycle, corners, img):
    n = len(cycle)  # number of sides
    deg = 360/n
    center = (500, 500)
    bond_length = 200
    points = []
    for i in range(len(cycle)):
        x = bond_length*math.cos(np.deg2rad(deg*i)) + center[0]
        y = bond_length*math.sin(np.deg2rad(deg*i)) + center[0]

        points.append([int(x), int(y)])
        cv.circle(img, (points[i][0], points[i][1]), 10, (0, 0, 255))

    points = np.array(points)
    img = cv.polylines(img, [points],
                       True, (0, 255, 0), 2)
    cv.circle(img, center, bond_length, (255, 0, 0))
    return points
