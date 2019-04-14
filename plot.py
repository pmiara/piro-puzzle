import matplotlib.pyplot as plt


def plot_vertices_on_contour(contour, vertices):
    plt.gca().set_aspect("equal")
    plt.plot(contour[:, 1], contour[:, 0], linewidth=2)
    for vertex in vertices:
        plt.scatter(contour[vertex, 1], contour[vertex, 0], s=100)
    plt.show()


def plot_img(img):
    plt.gca().set_aspect("equal")
    plt.imshow(img, cmap="gray")
    plt.show()
