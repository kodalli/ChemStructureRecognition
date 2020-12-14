import numpy as np
from math import hypot
from detectCycle import Graph


def test_corners_connected(corner1, corner2, lines_array, threshold):
    if np.array_equal(corner1, corner2):
        return False

    connected = False

    corner1_x, corner1_y = corner1.ravel()
    corner2_x, corner2_y = corner2.ravel()

    for line in lines_array:
        line_x1, line_y1, line_x2, line_y2 = line.ravel()

        if (hypot(corner1_x - line_x1, corner1_y - line_y1) < threshold
                and hypot(corner2_x - line_x2, corner2_y - line_y2) < threshold
                or hypot(corner2_x - line_x1, corner2_y - line_y1) < threshold
                and hypot(corner1_x - line_x2, corner1_y - line_y2) < threshold):
            connected = True

    return connected


def find_connected_corners(corners_array, lines_array, thresh):
    corners_comparison_array = corners_array

    j = 0
    k = 0

    graph = Graph(len(corners_array))
    for corner in corners_array:
        for corner_comparison in corners_comparison_array:
            connected = test_corners_connected(corner, corner_comparison, lines_array, threshold=thresh)
            if connected:
                # print(f"corner {j} and {k} are connected")
                # print(corner, corner_comparison)
                graph.add_edge(k, j)
            k += 1
        k = 0
        j += 1

    return graph
    # print(graph, end='\n\n')
