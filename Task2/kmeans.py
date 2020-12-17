import math
from collections import defaultdict
from itertools import chain

from matplotlib import colors
import matplotlib.pyplot as plt

from Task2.dot import Dot, create_random_dot

COUNT = 100
MAX = 100
MIN = 1


def create_random_dots(min_v=MIN, max_v=MAX, count=COUNT, cluster=None):
    dots = [create_random_dot(min_v, max_v, cluster) for i in range(count)]
    return dots


def init_centers(dots, count_center):

    if count_center < 2:
        return [dots[0]]

    max_distance = -1
    center_dots = []
    center1 = None
    center2 = None

    for i in range(len(dots)):
        start_dot = dots[i]
        for j in range(i + 1, len(dots)):
            dist = start_dot.get_distance(dots[j])
            if dist > max_distance:
                max_distance = dist
                center1 = start_dot
                center2 = dots[j]

    center_dots.extend((center1, center2))

    for i in range(count_center - len(center_dots)):
        max_distance = -1
        new_center = None

        for dot in dots:
            if dot in center_dots:
                continue
            distance = None
            for center_dot in center_dots:
                dist = center_dot.get_distance(dot)
                if distance is None or dist < distance:
                    distance = dist

            if max_distance < distance:
                max_distance = distance
                new_center = dot
        center_dots.append(new_center)
    return center_dots


def get_dots_position_lists(dots):
    x = []
    y = []
    for dot in dots:
        x.append(dot.x)
        y.append(dot.y)
    return x, y


def show_dots_picture(dots, centers=None, color=None):
    fig, ax = plt.subplots()
    x, y = get_dots_position_lists(dots)
    kw = {}
    if color:
        kw['edgecolors'] = color
    ax.scatter(x, y, **kw)
    if centers:
        x_center, y_center = get_dots_position_lists(centers)
        ax.scatter(x_center, y_center, edgecolors='g')
    fig.savefig('dots_picture.png')
    plt.show()


def show_clusters_picture(cluster, filename='clusters_picture.png'):
    fig, ax = plt.subplots()
    for index, (center, dots) in enumerate(cluster.items()):
        x, y = get_dots_position_lists(dots)
        ax.scatter(x, y, edgecolors=list(colors.cnames.keys())[index])
    fig.savefig(filename)
    plt.show()


def normalize_clusters(dots, centers):
    clusters = {}
    new_centers = []
    while centers != new_centers:
        new_centers = centers
        clusters = defaultdict(list)
        for dot in dots:
            min_dist = None
            t_dot = None
            for center_dot in new_centers:
                dist = center_dot.get_distance(dot)
                if min_dist is None or dist < min_dist:
                    min_dist = dist
                    t_dot = center_dot
            if t_dot is not None:
                clusters[t_dot].append(dot)

        updated_centers = []
        for center, points in clusters.items():
            sum_x = 0
            sum_y = 0
            for dot in points:
                sum_x += dot.x
                sum_y += dot.y
            center_x = sum_x / len(points)
            center_y = sum_y / len(points)
            updated_centers.append(Dot(center_x, center_y))

        centers = updated_centers

    return clusters


max_k = 10
min_k = 2

dots = create_random_dots()
dist_k = [0] * max_k
d_k = [-1.0] * max_k
clusters = [{}] * max_k
for k in range(min_k, max_k):
    centers = init_centers(dots, k)
    clusters[k] = normalize_clusters(dots, centers)
    dist = 0
    for center, points in clusters[k].items():
        for dot in points:
            dist += center.get_distance(dot)
    dist_k[k] = dist

    if dist_k[k - 2]:
        d_k[k - 1] = (
            math.fabs(dist_k[k - 1] - dist_k[k]) / math.fabs(dist_k[k - 2] - dist_k[k - 1])
        )
min_dist = min(filter(lambda x: x > 0, d_k))

index = d_k.index(min_dist)
print(f'Clusters count: {index}')

clusters = clusters[index]

show_dots_picture(list(chain.from_iterable(clusters.values())),clusters.keys())
show_clusters_picture(clusters)

