import pygame as pg
from sklearn import svm

WHITE = (255, 255, 255)
RED = (225, 0, 50)
GREEN = (0, 225, 0)
BLUE = (0, 0, 225)

sc = pg.display.set_mode((600, 400))
sc.fill(WHITE)
pg.display.update()

dots = {}
colors = []

exit_flag = True


def update(colors, button):
    colors.append(button)
    pg.display.update()


def drow_lones(y1, y2, y3, k, end):
    pg.draw.line(sc, GREEN, [0, y1], [(end - y1) / k, end], 1)
    pg.draw.aaline(sc, GREEN, [0, y2], [(end - y2) / k, end])
    pg.draw.aaline(sc, GREEN, [0, y3], [(end - y3) / k, end])
    pg.display.update()


while exit_flag:
    for i in pg.event.get():
        if i.type == pg.QUIT:
            exit_flag = False
        elif i.type == pg.MOUSEBUTTONDOWN:
            if i.button == 1:
            # Левая кнопка - красная точка
                pg.draw.circle(sc, RED, i.pos, 5)
                dots[i.pos] = RED
                update(colors, i.button)
            elif i.button == 3:
                # Правая кнопка - синяя точка
                pg.draw.circle(sc, BLUE, i.pos, 5)
                dots[i.pos] = BLUE
                update(colors, i.button)

        elif i.type == pg.KEYDOWN:
            # Enter - рисуем линии
            if i.key == pg.K_RETURN:
                sc.fill(WHITE)
                for dot, dot_color in dots.items():
                    pg.draw.circle(sc, dot_color, dot, 5)
                clf = svm.SVC(kernel='linear', C=1.0)
                clf.fit(tuple(dots.keys()), colors)
                # Получаем коэффициенты
                w = clf.coef_[0]
                i = clf.intercept_
                n = -w[0] / w[1]
                m = i[0] / w[1]
                y1 = -m
                x1 = m / n
                reversed_coef = tuple(map(lambda x: 1 / x, w))
                y2, x2 = (reversed_coef[1] + y1,
                            reversed_coef[0] + x1)
                y3, x3 = (-reversed_coef[1] + y1,
                            -reversed_coef[0] + x1)
                k = - y1 / x1
                end = 0 if k < 0 else 400
                # Рисуем линии
                drow_lones(y1, y2, y3, k, end)

            elif i.key == pg.K_SPACE:
                # Пробел - очищаем поле
                sc.fill(WHITE)
                dots = {}
                colors = []
                pg.display.update()

    pg.time.delay(30)