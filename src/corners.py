import cv2 as cv
import numpy as np


def draw_corners(img_source, img_display, max_corners, quality_level, min_distance, thresh, color):

    grey = cv.cvtColor(img_source, cv.COLOR_BGR2GRAY)
    grey = np.float32(grey)

    corners_array = cv.goodFeaturesToTrack(grey, max_corners, quality_level, min_distance)
    corners_img = img_display

    if corners_array is not None:
        corners_array = np.int0(corners_array)
        for corner in corners_array:
            x, y = corner.ravel()
            cv.circle(corners_img, (x, y), 6, 255, -1)
            cv.circle(corners_img, center=(x, y), radius=thresh, color=color)

    return corners_img, corners_array
