import math
import numpy as np


class Dot:
    """Класс точки"""

    def __init__(self, x, y, cluster=None):
        self.x = x
        self.y = y
        self.cluster = cluster

    def get_distance(self, other_dot):
        """Расчет расстояния между точками"""
        return math.sqrt(
           (self.x - other_dot.x) ** 2 + (self.y - other_dot.y) ** 2
        )

    def __eq__(self, other):
        if isinstance(other, list):
            return self in other
        else:
            return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))


def create_random_dot(min_v, max_v, cluster=None):
    """Создание рандомной точки"""

    return Dot(
        np.random.randint(min_v, max_v),
        np.random.randint(min_v, max_v),
        cluster
    )
