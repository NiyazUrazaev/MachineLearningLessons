import numpy as np
from plotly import graph_objects


LEARNING_RATE = 0.0001
ITERATION_COUNT = 1000


def get_coordinates(dots):
    return np.array(list(zip(*dots)))


def gradient(x, y, z):
    """
    Градиентный спуск
    :param x:
    :param y:
    :param z:
    :return: coefficients
    """
    a, b, c = 0, 0, 0
    n = float(len(x))

    for i in range(ITERATION_COUNT):
        z_predicted = a * x + b * y + c
        # (learning rate) * (derivative with respect to *)
        a -= LEARNING_RATE * ((-1 / n) * sum(x * (z - z_predicted)))
        b -= LEARNING_RATE * ((-1 / n) * sum(y * (z - z_predicted)))
        c -= LEARNING_RATE * ((-1 / n) * sum(z - z_predicted))

    return a, b, c


def create_random_dots(min_v=0, max_v=100, count=100, d=3):
    """
    Создаем рандомные точки
    :param min_v: int
    :param max_v: int
    :param count: int
    :param d: Размерность int
    :return: list of tuples (x, y, z)
    """
    dots = []
    for i in range(count):
        x, y, z = [np.random.randint(min_v, max_v) for i in range(d)]
        dots.append((x, y, z))
    return dots


dots = create_random_dots()
x, y, z = get_coordinates(dots)
a, b, c = gradient(x, y, z)

tmp = np.linspace(0, 100, 100)
x_coordinates, y_coorinates = np.meshgrid(tmp, tmp)

figure = graph_objects.Figure(
    data=[graph_objects.Scatter3d(x=x, y=y, z=z, mode='markers',)]
)
figure.add_trace(
    graph_objects.Surface(
        x=x_coordinates, y=y_coorinates, z=a * x_coordinates + b * y_coorinates + c
    )
)
figure.show()

