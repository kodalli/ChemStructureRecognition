import cv2 as cv
import numpy as np


def draw_lines(img, line_color, line_thickness, lines_array):
    line_img = np.zeros((img.shape[0], img.shape[1], 3), dtype=np.uint8)

    if lines_array is not None:
        for line in lines_array:
            for points in line:
                x1, y1, x2, y2 = points
                cv.line(line_img, (x1, y1), (x2, y2), line_color, line_thickness)
                # cv.circle(line_img, (x1, y1), 3, [255, 0, 0], 1)
                # cv.circle(line_img, (x2, y2), 3, [255, 0, 0], 1)

    return line_img, lines_array
