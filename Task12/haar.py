import os
import cv2


cascade_face = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
cascade_eye = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
cascade_smile = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_smile.xml')


def drow_eyes(eye, img_color):
    for (x_eye, y_eye, w_eye, h_eye) in eye:
        cv2.rectangle(
            img_color,
            (x_eye, y_eye),
            (x_eye + w_eye, y_eye + h_eye),
            (0, 180, 60), 2
        )


def drow_smile(smile, img_color):
    for (x_smile, y_smile, w_smile, h_smile) in smile:
        cv2.rectangle(
            img_color,
            (x_smile, y_smile),
            (x_smile + w_smile, y_smile + h_smile),
            (255, 0, 130), 2
        )


def detection(image_path):
    image = cv2.imread(image_path)
    grayscale = cv2.cvtColor(image, cv2.IMREAD_GRAYSCALE)

    face = cascade_face.detectMultiScale(grayscale, scaleFactor=1.15, minNeighbors=3, minSize=(30, 30))
    for (x_face, y_face, w_face, h_face) in face:
        cv2.rectangle(image, (x_face, y_face), (x_face + w_face, y_face + h_face), (255, 130, 0), 2)

        img_grayscale = grayscale[y_face:y_face + h_face, x_face:x_face + w_face]
        img_color = image[y_face:y_face + h_face, x_face:x_face + w_face]

        eye = cascade_eye.detectMultiScale(img_grayscale, 1.2, 18)
        drow_eyes(eye, img_color)

        smile = cascade_smile.detectMultiScale(img_grayscale, 1.7, 20)
        drow_smile(smile, img_color)

    return image


test_pictures_name = os.listdir('test_pictures')
for file_name in test_pictures_name:
    file_path = os.path.join(os.path.abspath('test_pictures'), file_name)
    result = detection(file_path)
    cv2.imwrite(f'result_{file_name}.png', result)
