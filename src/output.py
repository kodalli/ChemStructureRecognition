import cv2 as cv
import numpy as np
from detectCycle import Graph
import math


def draw_molecule(corners_array, graph: Graph, img):
    cycles = graph.get_all_cycles()
    bond_length = graph.get_average_bond_length(
        corners_array.reshape((corners_array.shape[0], 2)))

    img = np.zeros(img.shape)
    if cycles is not None:
        for cycle in cycles:
            img = draw_first_cycle(
                cycle, [corners_array[i] for i in cycle], img, bond_length)
    cv.imshow("drawn", img)


def draw_first_cycle(cycle, corners, img, bond_length):
    corners = np.array(corners)
    corners = corners.reshape((corners.shape[0], 2))
    x, y = np.mean(corners, axis=0)
    center = (int(x), int(y))

    cv.circle(img, center, 10, (0, 0, 255))

    # bond_length = int(math.hypot(
    #     corners[0][0] - center[0], corners[0][1] - center[1]))

    deg = 360/len(cycle)
    points = []
    for i in range(len(cycle)):
        x = bond_length*math.cos(np.deg2rad(deg*i + deg/2)) + center[0]
        y = bond_length*math.sin(np.deg2rad(deg*i + deg/2)) + center[1]

        points.append([int(x), int(y)])
        # cv.circle(img, (points[i][0], points[i][1]), 10, (0, 0, 255))

    points = np.array(points)
    img = cv.polylines(img, [points],
                       True, (0, 255, 0), 2)
    # cv.circle(img, center, bond_length, (255, 0, 0))
    return img


def find_center(corners):
    corners = corners.reshape(corners.shape[0], 2)
    x, y = np.mean(corners, axis=0)
    return (int(x), int(y))
