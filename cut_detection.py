from contour import calc_angle, cycle_dist
from parameters import *


def get_cut(contour, base_a, base_b):
    if base_a > base_b:
        base_a, base_b = base_b, base_a
    if cycle_dist(len(contour), base_a, base_b) == abs(base_a - base_b):
        step_a = -1 * CUT_DETECTION_DELTA
        step_b = CUT_DETECTION_DELTA
    else:
        step_a = CUT_DETECTION_DELTA
        step_b = -1 * CUT_DETECTION_DELTA
    return (
        get_cut_start(contour, base_a, step_a),
        get_cut_start(contour, base_b, step_b),
    )


def get_cut_start(contour, base, step):
    indexes = [base, (base + step) % len(contour)]
    vertices = [contour[idx] for idx in indexes]
    cut_start = base

    for i in range(len(contour)):
        indexes.append((indexes[-1] + step) % len(contour))
        vertices.append(contour[indexes[-1]])
        if i >= CUT_DETECTION_START_IDX:
            angle = calc_angle(vertices[-5], vertices[-3], vertices[-1])
            if abs(180 - angle) > CUT_DETECTION_THRESHOLD:
                cut_start = indexes[-1]
                break

    return cut_start
