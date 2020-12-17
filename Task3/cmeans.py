from matplotlib import colors

from Task2.dot import Dot
from Task2.kmeans import create_random_dots, COUNT, show_dots_picture, get_dots_position_lists
import numpy as np
import matplotlib.pyplot as plt
import math

# Степень размытости
M = 2
# Число кластеров
C = 2


def calculate_distance(c, count, dots, dist_m, centers):
    for i in range(count):
        for j in range(c):
            dist_m[i][j] = dots[i].get_distance(centers[j])
    return dist_m


def calculate_fm(c, count, fm, dist, m):
    # Степень принадлежности
    for i in range(count):
        for k in range(c):
            d = 0
            for j in range(c):
                d += (dist[i][k] / dist[i][j]) ** (2 / (m - 1))
            fm[i][k] = 1 / d
    return fm


def end_condition(c, count, fm, fm_prev):
    max_v = 0
    for i in range(count):
        for k in range(c):
            s = math.fabs(fm[i][k] - fm_prev[i][k])
            if max_v < s:
                max_v = s
    return max_v


def show_cluster(f_m, dots, centers):
    fig, ax = plt.subplots()
    colors_list = list(colors.cnames.keys())
    all_colors = []
    for index, dot in enumerate(f_m):
        max_index = list(dot).index(max(dot))
        all_colors.append(colors_list[max_index + 10])
    x, y = get_dots_position_lists(dots)
    ax.scatter(x, y, edgecolors=all_colors)
    centers_x, centers_y = get_dots_position_lists(centers)
    ax.scatter(centers_x, centers_y, edgecolors=colors_list[len(centers) * 5 + 1], s=100)
    fig.savefig('clusters_picture.png')
    plt.show()


count, e = COUNT, 10 ** -5
max_v = e + 1
dots = create_random_dots(count=count)
fm = np.random.dirichlet([1] * C, size=len(dots))
fm_prev, centers = None, [None] * C
dist_m = [[0] * C for i in range(len(dots))]

while max_v > e:

    for i in range(C):
        fm_sum, sum_x, sum_y = 0, 0, 0
        for k in range(count):
            fm_sum += fm[k, i] ** M
            sum_x += fm[k, i] ** M * dots[k].x
            sum_y += fm[k, i] ** M * dots[k].y

        centers[i] = Dot(sum_x / fm_sum, sum_y / fm_sum)

    dist_m = calculate_distance(C, count, dots, dist_m, centers)

    fm_prev = fm.copy()
    f_m = calculate_fm(C, count, fm, dist_m, M)
    max_v = end_condition(C, count, fm, fm_prev)

show_dots_picture(dots, centers)
show_cluster(fm, dots, centers)
print(fm)
