import math
import numpy as np
from skimage import measure

from parameters import CONTOUR_THRESHOLD


def get_contour(img):
    contours = measure.find_contours(img, CONTOUR_THRESHOLD)
    contour = max(contours, key=lambda arr: len(arr))
    return np.rint(contour).astype("int")


def cycle_dist(cycle_max, a, b):
    return min(abs(a - b), min(a, b) + cycle_max - max(a, b))


def calc_angle(a, b, c):
    ang = math.degrees(
        math.atan2(c[1] - b[1], c[0] - b[0]) - math.atan2(a[1] - b[1], a[0] - b[0])
    )
    return ang + 360 if ang < 0 else ang
