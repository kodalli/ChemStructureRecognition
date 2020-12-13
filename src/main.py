import cv2 as cv
import numpy as np
from lines import draw_lines
from corners import draw_corners
from testConnected import find_connected_corners

WINDOW_SIZE = (1024, 1024, 3)
COLOR_WHITE = (255, 255, 255)
COLOR_RED = (0, 0, 255)
COLOR_GREEN = (0, 255, 0)


# mouse callback function
def line_drawing(event, x, y, flags, param):
    global px, py
    if event == cv.EVENT_LBUTTONDOWN:
        px, py = x, y
        cv.circle(sketch, (x, y), 3, COLOR_RED, 5, cv.FILLED)
    elif event == cv.EVENT_LBUTTONUP:
        cv.line(sketch, (px, py), (x, y),
                color=COLOR_WHITE, thickness=2)
        cv.circle(sketch, (x, y), 3, COLOR_RED, 5, cv.FILLED)


# Create a black image, a window and bind the function to window
sketch = np.zeros(WINDOW_SIZE, np.uint8)
cv.namedWindow('canvas')
cv.setMouseCallback('canvas', line_drawing)

while (1):
    # displays sketch in window canvas
    cv.imshow('canvas', sketch)

    # finds edges in sketch and return map
    edges = cv.Canny(sketch, 150, 300)

    # finds lines in edges and returns map
    lines = cv.HoughLinesP(edges, rho=1.0, theta=np.pi / 180,
                           threshold=40, minLineLength=10, maxLineGap=10)

    # draw lines and stores endpoints coordinates in lines_array
    line_img, lines_array = draw_lines(sketch, COLOR_GREEN, 2, lines)

    # draw corners and stores coordinates in corners_array
    corners_img, corners_array = draw_corners(sketch, line_img,
                                                  100, 0.5, 30)

    # display corners in new window corners
    cv.imshow('corners & lines', corners_img)

    # moves windows to specific coordinates on screen
    # cv.moveWindow('corners & lines', 1350, 1100)
    # cv.moveWindow('canvas', 300, 1100)

    k = cv.waitKey(1) & 0xFF
    if k == ord('m'):
        sketch = np.zeros(WINDOW_SIZE, np.uint8)
    elif k == 27:
        break
    elif k == ord('n'):
        find_connected_corners(corners_array, lines_array)

cv.destroyAllWindows()
