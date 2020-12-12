import numpy as np
from math import hypot


class TestConnections:
    def __init__(self):
        pass

    def TestCornersConnected(self, corner1, corner2, lines_array, threshold):
        connected = False

        corner1_x, corner1_y = corner1.ravel()
        corner2_x, corner2_y = corner2.ravel()

        for line in lines_array:
            line_x1, line_y1, line_x2, line_y2 = line.ravel()

            if(hypot(corner1_x - line_x1, corner1_y - line_y1) < threshold
               and hypot(corner2_x - line_x2, corner2_y - line_y2) < threshold
               or hypot(corner2_x - line_x1, corner2_y - line_y1) < threshold
               and hypot(corner1_x - line_x2, corner1_y - line_y2) < threshold
               and not np.array_equal(corner1, corner2)):

                connected = True

            # print(hypot(corner2_x - line_x2, corner2_y, - line_y2))
            # print(hypot(corner2_x - line_x1, corner2_y, - line_y1))
            # print(hypot(corner1_x - line_x2, corner1_y, - line_y2))
        return connected
