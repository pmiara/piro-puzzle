import sys
import os
from skimage import io

from feature_extraction import (
    img_to_cut,
    crop_background,
    cut_to_signals,
    calc_distances,
)


def main(dir, n):
    images = {i: {"data": io.imread("{}/{}.png".format(dir, i))} for i in range(n)}

    for i, image in images.items():
        img = image["data"]
        cut_img = img_to_cut(img)
        cut_img = crop_background(cut_img)
        signal, signal_flipped = cut_to_signals(cut_img)
        images[i]["features"] = signal
        images[i]["features_flipped"] = signal_flipped

    results = calc_distances(images)

    for i in range(n):
        print(" ".join([str(x) for x in sorted(results[i], key=results[i].get)]))


if __name__ == "__main__":
    dir = sys.argv[1]
    n = int(sys.argv[2])
    main(dir, n)
