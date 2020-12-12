import cv2 as cv
import numpy as np

from lines import *
from corners import *
from testConnected import *


# mouse callback function
def line_drawing(event, x, y, flags, param):
    global pt1_x, pt1_y
    if event == cv.EVENT_LBUTTONDOWN:
        pt1_x, pt1_y = x, y
        cv.circle(sketch, (x, y), 3, [0, 0, 255], 5, cv.FILLED)
    elif event == cv.EVENT_LBUTTONUP:
        cv.line(sketch, (pt1_x, pt1_y), (x, y),
                color=(255, 255, 255), thickness=2)
        cv.circle(sketch, (x, y), 3, [0, 0, 255], 5, cv.FILLED)


# Create a black image, a window and bind the function to window
sketch = np.zeros((1024, 1024, 3), np.uint8)
cv.namedWindow('canvas')
cv.setMouseCallback('canvas', line_drawing)


while(1):
    # displays sketch in window canvas
    cv.imshow('canvas', sketch)

    # finds edges in sketch and return map
    edges = cv.Canny(sketch, 150, 300)

    # finds lines in edges and returns map
    lines = cv.HoughLinesP(edges, rho=1.0, theta=np.pi/180,
                           threshold=40, minLineLength=10, maxLineGap=10)

    # draw lines and stores endpoints coords in lines_array
    line_img = DrawLines()
    line_img, lines_array = line_img.Draw(sketch, [0, 255, 0], 2, lines)

    # draw corners and stores coords in corners_array
    corners_img = DrawCorners()
    corners_img, corners_array = corners_img.Draw(sketch, line_img,
                                                  100, 0.5, 30)

    # display corners in new window corners
    cv.imshow('corners & lines', corners_img)

    # moves windows to specific coordinates on screen
    cv.moveWindow('corners & lines', 1350, 1100)
    cv.moveWindow('canvas', 300, 1100)

    k = cv.waitKey(1) & 0xFF
    if k == ord('m'):
        sketch = np.zeros((1024, 1024, 3), np.uint8)
    elif k == 27:
        break

cv.destroyAllWindows()

corners_comparison_array = corners_array

j = 0
k = 0

for corner in corners_array:
    test_connections_init = TestConnections()
    for corner_comparison in corners_comparison_array:
        connected = test_connections_init.TestCornersConnected(corner, corner_comparison, lines_array, 35)
        if(connected):
            print(f"corner {j} and {k} are connected")
            print(corner, corner_comparison)
        k += 1
    k = 0
    j += 1
