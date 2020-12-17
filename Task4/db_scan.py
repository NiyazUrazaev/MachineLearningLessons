from collections import defaultdict
from Task2.kmeans import create_random_dots, COUNT, show_clusters_picture


def get_neigh(dots, dot, dist):
    # Получаем соседей
    neighborhoods = set(
        d for d in dots if d.get_distance(dot) <= dist and d != dot
    )
    return neighborhoods


dots = create_random_dots(count=COUNT)
neigh_count, distance, cluster_number = 2, 10, 0
visited = {}
clusters = defaultdict(list)

for dot in dots:
    if dot not in visited:
        neighb = get_neigh(dots, dot, distance)
        if len(neighb) > neigh_count:
            visited[dot] = 'green'
            cluster_number += 1
            clusters[cluster_number].append(dot)
            dot.cluster = cluster_number
            while neighb:
                d = neighb.pop()
                if d not in visited:
                    n_neigh = get_neigh(dots, d, distance)
                    visited[d] = 'yellow'
                    clusters[cluster_number].append(d)
                    d.cluster = cluster_number
                    if len(n_neigh) > neigh_count:
                        neighb = neighb.union(n_neigh)
                if d not in clusters.values():
                    clusters[cluster_number].append(d)
                    d.cluster = cluster_number
        elif len(neighb) == 0:
            visited[dot] = 'red'
            clusters['red'].append(dot)
        else:
            visited[dot] = 'yellow'

for dot, color in visited.items():
    if not hasattr(dot, 'cluster') and dot.cluster is not None and color == 'yellow':
        min_v, neighbour = None, None
        neighb = get_neigh(dots, dot, distance)
        for n in neighb:
            if min_v is None or min_v > n.get_distance(dot):
                min_v = n.get_distance(dot)
                neighbour = n
        if neighbour and hasattr(neighbour, 'cluster') and neighbour.cluster is not None:
            clusters[neighbour.cluster].append(dot)

show_clusters_picture(clusters)
