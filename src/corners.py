import cv2 as cv
import numpy as np


class DrawCorners:
    def __init__(self):
        pass

    def Draw(self, img_source, img_display,
             max_corners, quality_level, min_distance):

        grey = cv.cvtColor(img_source, cv.COLOR_BGR2GRAY)
        grey = np.float32(grey)

        corners_array = cv.goodFeaturesToTrack(grey, max_corners,
                                               quality_level, min_distance)
        corners_img = img_display

        if corners_array is not None:
            corners_array = np.int0(corners_array)
            for corner in corners_array:
                x, y = corner.ravel()
                cv.circle(corners_img, (x, y), 6, 255, -1)

        return corners_img, corners_array
