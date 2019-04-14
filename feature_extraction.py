import numpy as np
from scipy.fftpack import fft
from collections import defaultdict
from itertools import combinations

from contour import get_contour
from base_detection import get_base
from cut_detection import get_cut
from cut_processing import get_cut_img, get_cut_indices, calc_rotation_parameters
from parameters import FFT_FEATURES, DIST_FUNCTION


def img_to_cut(img):
    contour = get_contour(img)
    base_a, base_b = get_base(contour)
    cut_a, cut_b = get_cut(contour, base_a, base_b)
    cut_indices = get_cut_indices(contour, base_a, base_b, cut_a, cut_b)
    rotation_angle, base_center = calc_rotation_parameters(
        contour, base_a, base_b, cut_a
    )
    return get_cut_img(img, contour, cut_indices, rotation_angle, base_center)


def crop_background(img):
    mask = img > 0
    return img[np.ix_(mask.any(1), mask.any(0))]


def cut_to_signals(cut_img):
    signal = np.argmax(cut_img, axis=0)
    cut_img_flipped = np.flipud(cut_img)
    cut_img_flipped = np.fliplr(cut_img_flipped)
    signal_flipped = np.argmax(cut_img_flipped, axis=0)

    signal = normalize_signal(signal)
    signal_flipped = normalize_signal(signal_flipped)
    return signal, signal_flipped


def normalize_signal(signal):
    signal = abs(fft(signal))[:FFT_FEATURES]
    return signal / signal.sum()


def calc_distances(images):
    results = defaultdict(dict)
    for a, b in combinations(images.keys(), 2):
        x1 = images[a]["features"]
        x2 = images[b]["features_flipped"]
        dist = DIST_FUNCTION(x1, x2)
        results[a][b] = dist
        results[b][a] = dist
    return results
