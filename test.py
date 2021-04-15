import cv2 as cv
import numpy as np
from lib.thinning import thinning

WINDOW_SIZE = (720, 1280, 3)
COLOR_RED = (0, 0, 255)
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
LINE_THICKNESS = 5

drawing = False


def line_drawing(event, x, y, flags, param):
    global px, py, drawing

    color = COLOR_BLACK

    if event == cv.EVENT_LBUTTONDOWN:
        drawing = True
        px, py = x, y

    elif event == cv.EVENT_MOUSEMOVE:
        if drawing:
            cv.line(sketch, (px, py), (x, y), color, LINE_THICKNESS)
            px = x
            py = y
            # print(x, y)

    elif event == cv.EVENT_LBUTTONUP:
        drawing = False
        cv.line(sketch, (px, py), (x, y), color, LINE_THICKNESS)

    return x, y


def shape_detect(src):
    # Convert to grayscale
    bw = cv.cvtColor(src, cv.COLOR_BGR2GRAY)

    # Binarize
    # _, bw2 = cv.threshold(bw, 10, 255, cv.THRESH_BINARY)
    _, bw2 = cv.threshold(bw, 127, 255, cv.THRESH_BINARY)

    # Perform thinning
    # bw2 = thinning(bw2)

    contours, hierarchy = cv.findContours(
        bw2, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)

    # img_contours = np.zeros(src.shape)
    # cv.drawContours(img_contours, contours, -1, (0, 255, 0), 3)

    hulls = []

    for contour in contours:
        # Creating convex hull object for each contour
        hull = cv.convexHull(contour, False)
        hulls.append(hull)

        # Compute circularity, used for shape classification
        area = cv.contourArea(hull)
        perimeter = cv.arcLength(hull, True)
        circularity = (4 * np.pi * area) / (perimeter * perimeter)
        print(circularity)

    drawing = np.zeros(src.shape, np.uint8)

    # draw contours and hull points
    for i in range(len(contours)):
        color_contours = (0, 255, 0)  # green - color for contours
        color = (255, 0, 0)  # blue - color for convex hull
        # draw ith contour
        cv.drawContours(drawing, contours, i, color_contours, 1, 8, hierarchy)
        # draw ith convex hull object
        cv.drawContours(drawing, hulls, i, color, 1, 8)

    cv.imshow("result", drawing)

    """
    // For each contour
    for (vector<Point>& contour : contours)
    {
        // Compute convex hull
        vector<Point> hull;
        convexHull(contour, hull);

        // Compute circularity, used for shape classification
        double area = contourArea(hull);
        double perimeter = arcLength(hull, true);
        double circularity = (4 * CV_PI * area) / (perimeter * perimeter);

        // Shape classification

        if (circularity > 0.9)
        {
            // CIRCLE

            //{
            //  // Fit an ellipse ...
            //  RotatedRect rect = fitEllipse(contour);
            //  Scalar color = Scalar(rng.uniform(0, 255), rng.uniform(0, 255), rng.uniform(0, 255));
            //  ellipse(res, rect, color, 5);
            //}
            {
                // ... or find min enclosing circle
                Point2f center;
                float radius;
                minEnclosingCircle(contour, center, radius);
                Scalar color = Scalar(rng.uniform(0, 255), rng.uniform(0, 255), rng.uniform(0, 255));
                circle(res, center, radius, color, 5);
            }
        }
        else if (circularity > 0.75)
        {
            // RECTANGLE

            //{
            //  // Minimum oriented bounding box ...
            //  RotatedRect rect = minAreaRect(contour);
            //  Point2f pts[4];
            //  rect.points(pts);

            //  Scalar color = Scalar(rng.uniform(0, 255), rng.uniform(0, 255), rng.uniform(0, 255));
            //  for (int i = 0; i < 4; ++i)
            //  {
            //      line(res, pts[i], pts[(i + 1) % 4], color, 5);
            //  }
            //}
            {
                // ... or bounding box
                Rect box = boundingRect(contour);
                Scalar color = Scalar(rng.uniform(0, 255), rng.uniform(0, 255), rng.uniform(0, 255));
                rectangle(res, box, color, 5);
            }
        }
        else if (circularity > 0.7)
        {
            // TRIANGLE

            // Select the portion of the image containing only the wanted contour
            Rect roi = boundingRect(contour);
            Mat1b maskRoi(bin.rows, bin.cols, uchar(0));
            rectangle(maskRoi, roi, Scalar(255), CV_FILLED);
            Mat1b triangle(roi.height, roi.height, uchar(0));
            bin.copyTo(triangle, maskRoi);

            // Find min encolsing circle on the contour
            Point2f center;
            float radius;
            minEnclosingCircle(contour, center, radius);

            // decrease the size of the enclosing circle until it intersects the contour
            // in at least 3 different points (i.e. the 3 vertices)
            vector<vector<Point>> vertices;
            do
            {
                vertices.clear();
                radius--;

                Mat1b maskCirc(bin.rows, bin.cols, uchar(0));
                circle(maskCirc, center, radius, Scalar(255), 5);

                maskCirc &= triangle;
                findContours(maskCirc.clone(), vertices, CV_RETR_LIST, CV_CHAIN_APPROX_NONE);

            } while (vertices.size() < 3);

            // Just get the first point in each vertex blob.
            // You could get the centroid for a little better accuracy

            Scalar color = Scalar(rng.uniform(0, 255), rng.uniform(0, 255), rng.uniform(0, 255));
            line(res, vertices[0][0], vertices[1][0], color, 5);
            line(res, vertices[1][0], vertices[2][0], color, 5);
            line(res, vertices[2][0], vertices[0][0], color, 5);

        }
        else
        {
            cout << "Some other shape..." << endl;
        }

    }
    """


if __name__ == "__main__":

    sketch = np.ones(WINDOW_SIZE, np.uint8) * 255
    cv.namedWindow('canvas')
    cv.setMouseCallback('canvas', line_drawing)

    while 1:
        # displays sketch in window canvas
        cv.imshow('canvas', sketch)

        k = cv.waitKey(1) & 0xFF
        if k == ord('m'):
            sketch = np.ones(WINDOW_SIZE, np.uint8) * 255
        elif k == ord('n'):
            shape_detect(sketch)
        elif k == 27:
            break
