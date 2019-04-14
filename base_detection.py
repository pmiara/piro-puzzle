from itertools import combinations
from skimage.draw import line
from collections import defaultdict

from contour import calc_angle, contour_to_int_array
from parameters import *

# TODO: sprawdź jak daleko są od siebie wierzchołki podstaw.
# Jeśli za blisko (mniej niż połowa wszystkich punktów), to odrzuć.


def get_base(contour):
    vertex_scores = score_vertices(contour)
    best_vertices = choose_best_vertices(vertex_scores)
    base_a, base_b = find_best_base_pair(contour, best_vertices)
    return base_a, base_b


def calc_right_angle_score(a, b, c):
    return abs(90 - calc_angle(a, b, c))


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
    contour_int = contour_to_int_array(contour)
    contour_set = {(y, x) for y, x in contour_int}
    best_score = 0
    for a, b in combinations(best_vertices, 2):
        score = score_vertex_pair(contour_set, contour_int[a], contour_int[b])
        if score > best_score:
            best_score = score
            base_a, base_b = a, b
    return base_a, base_b
