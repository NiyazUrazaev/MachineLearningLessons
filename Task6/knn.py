from collections import defaultdict, Counter
from Task2.kmeans import create_random_dots, COUNT, show_clusters_picture


def get_distance_dots(clusters, other_d):
    distances_to_dot = []
    for cluster, dots in clusters.items():
        for dot in dots:
            dist = dot.get_distance(other_d)
            distances_to_dot.append((dot, dist))
    return distances_to_dot


def get_distribution(default_clusters, random_dots, k):
    """Распределение точек"""
    clusters = default_clusters.copy()
    for dot in random_dots:
        distance = get_distance_dots(default_clusters, dot)
        neighbour = Counter()
        # Берём k ближайших соседей
        for neigh_dot, distance in sorted(distance, key=lambda dots: dots[1],)[:k]:
            neighbour[neigh_dot.cluster] += 1
        cluster = sorted(
            neighbour.items(),
            key=lambda item: item[1]
        )[-1]
        dot.cluster = cluster[0]
        clusters[cluster[0]].append(dot)
    return clusters


k, n = 10, 3
clusters, train_dots = defaultdict(list), []
for i in range(n):
    dots = create_random_dots(count=COUNT // n, cluster=i)
    clusters[i].extend(dots)
    train_dots.extend(dots)

show_clusters_picture(clusters, filename='train_clusters_picture.png')
random_dots = create_random_dots(count=COUNT)
clusters = get_distribution(clusters, random_dots, k)
show_clusters_picture(clusters)

