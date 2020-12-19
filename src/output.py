import cv2 as cv
import numpy as np
from scipy import stats
from collections import defaultdict
from detectCycle import Graph


def draw_molecule(corners_array, graph: Graph, img):
    # corners array has the coordinates of each node on the graph
    z = graph.get_all_cycles()

    if z is None:
        return

    cycles, connected_cycles = z

    bond_length = graph.get_average_bond_length(
        corners_array.reshape((corners_array.shape[0], 2)))

    connected_cycles_dict = defaultdict(set)
    for cy1, cy2 in list(connected_cycles):  # indexes in cycles
        z = list(set(cycles[cy1]).intersection(set(cycles[cy2])))
        i, j = z[0], z[1]  # connected nodes between two cycles
        cv.circle(img, (corners_array[i][0][0], corners_array[i][0][1]), 10, (255, 0, 0), -1)
        cv.circle(img, (corners_array[j][0][0], corners_array[j][0][1]), 10, (255, 0, 0), -1)
        connected_cycles_dict[cy1].add(cy2)
        connected_cycles_dict[cy2].add(cy1)

    img = np.zeros(img.shape)

    drawn = set()
    drawn_cycle_pts_dict = {}
    for index, cycle in enumerate(cycles):  # each cycle in cycles is a list with nodes [1,2,3,4...]
        cycles_connected_to_current_cycle = connected_cycles_dict[index]
        drawn_cycles_that_are_connected = cycles_connected_to_current_cycle.intersection(drawn)
        if len(drawn_cycles_that_are_connected) == 0:
            other_cycles = cycles.copy()
            other_cycles.pop(index)
            img, points = draw_first_cycle(
                cycle, [corners_array[i] for i in cycle], img, bond_length, other_cycles)
            drawn.add(index)
            drawn_cycle_pts_dict[index] = points
        else:
            # used to construct line to reflect shape across
            connected_nodes = list(set(cycles[list(drawn_cycles_that_are_connected)[0]]).intersection(set(cycle)))

            # !!! WHEN DRAWING 3 CONNECTED CYCLES, DETECTING AN EXTRA CYCLE THAT IS NOT A COMBINATION
            # OF THE SMALLER CYCLES, WHICH IS HOW WE DECIDE TO REMOVE THE LARGE CYCLE
            print("connected nodes", connected_nodes)
            print("connected cycles", connected_cycles)
            print("drawn cycles that are connected", drawn_cycles_that_are_connected)
            print("cycles", cycles)
            print("corner array values of connected", corners_array[connected_nodes[0]],
                  corners_array[connected_nodes[1]])
            print("connected cycles dictionary", connected_cycles_dict)

            # !! KEY ERROR IF > 2 CYCLES
            img = draw_connected_cycle_by_reflection(connected_nodes, drawn_cycle_pts_dict[
                list(drawn_cycles_that_are_connected)[0]], img)
            drawn.add(index)

    cv.imshow("drawn", img)


def draw_first_cycle(cycle, corners, img, bond_length, cycles_excluding_first):
    corners = np.array(corners)
    corners = corners.reshape((corners.shape[0], 2))
    x, y = np.mean(corners, axis=0)
    center = (int(x), int(y))

    cv.circle(img, center, 10, (0, 0, 255))

    # pair of nodes that are connected to another cycle should be drawn consecutively
    new_cycle = []
    for other_cycle in cycles_excluding_first:
        connected_nodes = list(cycle.intersection(other_cycle))
        if len(connected_nodes) != 0:
            new_cycle += connected_nodes
            cycle = cycle.difference(other_cycle)
    cycle = new_cycle + list(cycle)
    deg = 360 / len(cycle)
    points = []
    points_dict = {}

    for i in range(len(cycle)):
        x = bond_length * np.cos(np.deg2rad(deg * i + deg / 2)) + center[0]
        y = bond_length * np.sin(np.deg2rad(deg * i + deg / 2)) + center[1]

        points.append([int(x), int(y)])
        points_dict[cycle[i]] = points[i]

    points = np.array(points)
    img = cv.polylines(img, [points],
                       True, (0, 255, 0), 2)
    return img, points_dict


# The wrong shared nodes are being given, thus the line of reflection is incorrect
def draw_connected_cycle_by_reflection(connected_nodes, cycle_to_flip_points, img):
    """
        Given point P = (x, y)
        Reflection R = (u, v) = (u(x,y), v(x, y)), where
        Line L = {y = mx + b}
        u = ((1 - m**2)*x + 2*m*y - 2*m*b) / (m**2 + 1)
        v = ((m**2 - 1)*y + 2*m*x + 2*b) / (m**2 + 1)
    """
    # flip original coordinates across line of connected points
    # only works for identical cycles
    # make line equation
    pts = np.array([cycle_to_flip_points[connected_nodes[0]], cycle_to_flip_points[connected_nodes[1]]])

    cv.circle(img, tuple(pts[0]), 10, (255, 0, 0), -1)
    cv.circle(img, tuple(pts[1]), 10, (255, 0, 0), -1)

    m, b, _, _, _ = stats.linregress(pts[:, 0], pts[:, 1])

    reflected_points = []
    for key, val in cycle_to_flip_points.items():
        x, y = val
        u = ((1 - m ** 2) * x + 2 * m * y - 2 * m * b) / (m ** 2 + 1)
        v = ((m ** 2 - 1) * y + 2 * m * x + 2 * b) / (m ** 2 + 1)
        if np.isnan(u) or np.isnan(v):
            reflected_points.append((int(2 * pts[0, 0] - x), int(y)))
        else:
            reflected_points.append((int(u), int(v)))

    points = np.array(reflected_points)
    img = cv.polylines(img, [points],
                       True, (0, 255, 0), 2)
    return img


""" 
    find two closest points to connect
    translate center, and add degree offest to rotate 
    rotate and translate to achieve connection between two heterocycles
"""
