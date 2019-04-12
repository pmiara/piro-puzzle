import math
from itertools import combinations
from skimage.draw import line
from collections import defaultdict

from parameters import *


def get_base(contour):
    """
    The most important function in this file. Returns figure's base.
    """
    vertex_scores = score_vertices(contour)
    best_vertices = choose_best_vertices(vertex_scores)
    base_a, base_b = find_best_base_pair(contour, best_vertices)
    return base_a, base_b


def calc_right_angle_score(a, b, c):
    return abs(90 - calc_angle(a, b, c))


def calc_angle(a, b, c):
    ang = math.degrees(math.atan2(c[1]-b[1], c[0]-b[0]) - math.atan2(a[1]-b[1], a[0]-b[0]))
    return ang + 360 if ang < 0 else ang


def score_vertices(contour):
    vertex_scores = defaultdict(int)
    for delta in ANGLE_DELTAS:
        for i, point in enumerate(contour):
            point_prev = contour[(i - delta) % len(contour)]
            point_next = contour[(i + delta) % len(contour)]
            vertex_scores[i] += calc_right_angle_score(point_prev, point, point_next)
    return vertex_scores


def choose_best_vertices(vertices):
    """
    TODO: check if two best angles are too close to each other and merge them if they do
    """
    return sorted(vertices, key=vertices.get)[:TOP_K_BASE_VERTICES]


def score_vertex_pair(contour_set, point_a, point_b):
    y_a, x_a = point_a[0], point_a[1]
    y_b, x_b = point_b[0], point_b[1]
    rr, cc = line(y_a, x_a, y_b, x_b)
    score = 0
    for point in zip(rr, cc):
        if point in contour_set:
            score += 1
    return score


def find_best_base_pair(contour, best_vertices):
    contour_set = {(y, x) for y, x in contour}
    best_score = 0
    for a, b in combinations(best_vertices, 2):
        score = score_vertex_pair(contour_set, contour[a], contour[b])
        if score > best_score:
            best_score = score
            base_a, base_b = a, b
    return base_a, base_b
