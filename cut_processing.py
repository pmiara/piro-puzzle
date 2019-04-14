from skimage.transform import rotate
import numpy as np

from contour import calc_angle, contour_to_int_array


def get_cut_indices(contour, base_a, base_b, cut_a, cut_b):
    if (
        base_a < cut_a < cut_b < base_b
        or cut_a < cut_b < base_b < base_a
        or cut_b < base_b < base_a < cut_a
        or base_b < base_a < cut_a < cut_b
    ):
        cut_start = cut_a
        cut_end = cut_b
    else:
        cut_start = cut_b
        cut_end = cut_a
    if cut_start < cut_end:
        cut_indices = list(range(cut_start, cut_end + 1))
    else:
        cut_indices = list(range(cut_start, len(contour))) + list(range(cut_end + 1))
    return cut_indices


def calc_rotation_parameters(contour, base_a, base_b, cut_a):
    a = contour[base_a]
    b = contour[base_b]
    c = (a[0], b[1])
    angle = calc_angle(c, a, b)
    base_center = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
    if contour[cut_a][0] > contour[base_a][0]:
        rotation_angle = 180 - angle
    else:
        rotation_angle = 360 - angle
    return rotation_angle, base_center


def get_cut_img(img, contour, cut_indices, rotation_angle, base_center):
    cut_img = np.zeros_like(img)
    contour_cut = contour_to_int_array(contour)[cut_indices]
    cut_img[contour_cut[:, 0], contour_cut[:, 1]] = 1
    cut_img = rotate(cut_img, rotation_angle, center=base_center, resize=True)
    cut_img[cut_img > 0] = 1
    return cut_img
