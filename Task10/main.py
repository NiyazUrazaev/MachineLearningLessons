import pygame as pg

import numpy as np
import cv2
from tensorflow import keras


maxx = 0
maxy = 0
minx = 401
miny = 401


def get_result(size, sequential):
    picture = cv2.imread(
        'test_picture.png',
        cv2.IMREAD_GRAYSCALE
    )
    (t, picture) = cv2.threshold(
        picture, 128, 255,
        cv2.THRESH_BINARY | cv2.THRESH_OTSU
    )
    picture = cv2.threshold(
        picture, 127, 255, cv2.THRESH_BINARY
    )[1]

    minx, miny, maxx, maxy = size
    minx = max(0, minx - 20)
    miny = max(0, miny - 20)
    maxx = min(400, maxx + 20)
    maxy = min(400, maxy + 20)
    picture = picture[miny:maxy, minx:maxx]

    picture = cv2.resize(picture, dsize=(28, 28))
    picture = np.array(picture).reshape(1, 28, 28, 1)

    prediction = sequential.predict(picture)
    return np.argmax(prediction, axis=1)[0]


pg.init()
sc = pg.display.set_mode((400, 400))
sc.fill(pg.Color('black'))
pg.display.update()
f1 = pg.font.Font(None, 36)

not_exit_flag, mouse_button_flag = True, False
sequential = keras.models.load_model('sequential.h5')

while not_exit_flag:
    pos = pg.mouse.get_pos()
    for i in pg.event.get():
        if i.type == pg.QUIT:
            pg.quit()
            not_exit_flag = False
        if i.type == pg.MOUSEBUTTONDOWN:
            # Нажимаем ЛКМ - рисуем
            mouse_button_flag = True
        if i.type == pg.MOUSEBUTTONUP:
            # Отпускаем ЛКМ - перестаем рисовать
            mouse_button_flag = False
        if i.type == pg.KEYDOWN:
            if i.key == pg.K_RETURN:
                # Нажимаем Enter - выводим результат
                pg.image.save(sc, 'test_picture.png')
                size = minx, miny, maxx, maxy
                num = get_result(size, sequential)
                text1 = f1.render(f'Result: {num}', True, pg.Color('red'))
                sc.blit(text1, (10, 10))
                pg.display.update()
            elif i.key == pg.K_SPACE:
                # Нажимаем SPACE - стираем рисунок
                sc.fill(pg.Color('black'))
                pg.display.update()
                maxx, maxy, minx, miny = 0, 0, 401, 401
    if mouse_button_flag:
        new_pos = pg.mouse.get_pos()
        pg.draw.line(sc, pg.Color('white'), pos, new_pos, 10)
        maxx = max(maxx, pos[0], new_pos[0])
        minx = min(minx, pos[0], new_pos[0])
        maxy = max(maxy, pos[1], new_pos[1])
        miny = min(miny, pos[1], new_pos[1])
        pg.display.update()
