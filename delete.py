import numpy as np
import matplotlib.pylab as plt
step_size = 0.1


def best_way(h, x):
    if abs(x[0]) > abs(x[1]):
        if (x[0] < 0 and h[0] < 0) or (x[0] > 0 and h[0] > 0):
            return -1 * h
        else:
            return h
    else:
        if (x[1] < 0 and h[1] < 0) or (x[1] > 0 and h[1] > 0):
            return -1 * h
        else:
            return h


def calculate_slope(x1, x2):
    x = x2[0] - x1[0]
    y = x2[1] - x2[0]
    return np.asarray([x, y])


def progress(x_old):
    h1 = np.asarray([np.random.uniform(-1, 1), np.random.uniform(-1, 1)])
    h2 = np.asarray([np.random.uniform(-1, 1), np.random.uniform(-1, 1)])
    print(h1[0])
    while np.cross(h1, h2) == 0:
        h2 = np.asarray([np.random.uniform(-1, 1), np.random.uniform(-1, 1)])
    x1 = x_old + best_way(h1, x_old)
    x2 = x1 + best_way(h2, x1)
    h3 = calculate_slope(x_old, x2)

    x3 = x2 + step_size * best_way(h3, x2)
    x4 = x3 + step_size * best_way(h2, x3)
    x5 = x4 + step_size * best_way(h3, x4)
    return x5

randomx = np.asarray([90, -90])

for i in range(100):
    randomx = progress(randomx)
    print(randomx)