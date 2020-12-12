import numpy as np
from math import hypot


def TestCornersConnected(corner1, corner2, lines_array, threshold):
    if np.array_equal(corner1, corner2):
        return False

    connected = False

    corner1_x, corner1_y = corner1.ravel()
    corner2_x, corner2_y = corner2.ravel()

    for line in lines_array:
        line_x1, line_y1, line_x2, line_y2 = line.ravel()

        if(hypot(corner1_x - line_x1, corner1_y - line_y1) < threshold
            and hypot(corner2_x - line_x2, corner2_y - line_y2) < threshold
            or hypot(corner2_x - line_x1, corner2_y - line_y1) < threshold
            and hypot(corner1_x - line_x2, corner1_y - line_y2) < threshold):

            connected = True

        # print(hypot(corner2_x - line_x2, corner2_y, - line_y2))
        # print(hypot(corner2_x - line_x1, corner2_y, - line_y1))
        # print(hypot(corner1_x - line_x2, corner1_y, - line_y2))
    return connected


def find_connected_corners(corners_array, lines_array, img):
    corners_comparison_array = corners_array

    j = 0
    k = 0

    graph = {i: set() for i in range(len(corners_array))}
    for corner in corners_array:
        # cv.circle(img, (corner[0], corner[1]), radius=100)
        for corner_comparison in corners_comparison_array:
            connected = TestCornersConnected(corner, corner_comparison, lines_array, threshold=100)
            if connected:
                # print(f"corner {j} and {k} are connected")
                graph[j].add(k)
                graph[k].add(j)
                # print(corner, corner_comparison)
            k += 1
        k = 0
        j += 1

    print(graph, end='\n\n')