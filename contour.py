import numpy as np
from skimage import measure

from parameters import CONTOUR_THRESHOLD


def get_contour(img):
    contours = measure.find_contours(img, CONTOUR_THRESHOLD)
    contour = max(contours, key=lambda arr: len(arr))
    return np.rint(contour).astype("int")
