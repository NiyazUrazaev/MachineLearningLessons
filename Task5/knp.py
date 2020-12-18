from collections import defaultdict

from Task2.kmeans import COUNT, create_random_dots, show_clusters_picture


def get_minimums(matrix, visited=frozenset()):
    count, min_v, dots = len(matrix), None, {}
    unvisited, all_flag = {}, False
    if not visited:
        visited = tuple(range(count))
        all_flag = True
    else:
        unvisited = set(range(count)) - visited
    for i in visited:
        if all_flag:
            unvisited = range(i + 1, count)
        for j in unvisited:
            if j in visited and not all_flag:
                continue
            if min_v is None or matrix[i][j] < min_v:
                min_v = matrix[i][j]
                dots = i, j
    return dots, min_v


def delete_e(matrix, k):
    while k - 1:
        maxi = -1
        e = ()
        for i in range(len(matrix)):
            for j in range(i + 1, len(matrix)):
                if matrix[i][j] > maxi:
                    maxi = matrix[i][j]
                    e = i, j
        k -= 1
        matrix[e[0]][e[1]] = matrix[e[1]][e[0]] = 0


def get_clusters(matrix, dots):
    def _check_is_not_none(dot):
        return dot is not None
    clusters = defaultdict(list)
    cluster_num = 0
    for i in range(len(matrix)):
        for j in range(i + 1, len(matrix)):
            if matrix[i][j]:
                dot1 = dots[i].cluster
                dot2 = dots[j].cluster
                # Обрабатываем случаи когда у 2 точек уже есть кластер,
                # когда только у 1 точки кластер и когда его нет вообще
                if _check_is_not_none(dot1) and _check_is_not_none(dot2):
                    clusters[dot1].extend(clusters[dot2])
                    for dot in clusters[dot2]:
                        dot.cluster = dot1
                    del clusters[dot2]
                elif _check_is_not_none(dot1):
                    clusters[dot1].append(dots[j])
                    dots[j].cluster = dot1
                elif _check_is_not_none(dot2):
                    clusters[dot2].append(dots[i])
                    dots[i].cluster = dot2
                else:
                    clusters[cluster_num].extend((dots[i], dots[j]))
                    dots[i].cluster = cluster_num
                    dots[j].cluster = cluster_num
                    cluster_num += 1
    return clusters


k, visited = 3, set()
dots = create_random_dots(count=COUNT)
matrix = [
    [0 for i in range(COUNT)] for i in range(COUNT)
]
count = len(dots)
distances = [
    [0 for i in range(count)] for i in range(count)
]
for i in range(count):
    distances[i][i] = None
    for j in range(i + 1, count):
        distances[j][i] = distances[i][j] = dots[i].get_distance(dots[j])
while len(visited) != count:
    min_dots, min_v = get_minimums(distances, visited)
    matrix[min_dots[0]][min_dots[1]] = matrix[min_dots[1]][min_dots[0]] = min_v
    visited = visited.union(set(min_dots))
delete_e(matrix, k)
show_clusters_picture(get_clusters(matrix, dots))

