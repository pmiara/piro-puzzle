import sys
import os
from skimage import io


def main(dir, n):
    images = [io.imread("{}/{}.png".format(dir, i)) for i in range(n)]
    for i in range(n):
        print(n - i - 1)


if __name__ == "__main__":
    dir = sys.argv[1]
    n = int(sys.argv[2])
    main(dir, n)
