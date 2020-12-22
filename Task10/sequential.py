import os

from tensorflow import keras
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout


def get_sequential_instance(pictures_size):
    sequential = Sequential()
    sequential.add(Conv2D(
        64, (3, 3),
        input_shape=pictures_size,
        activation='relu'
    ))
    sequential.add(Conv2D(
        15, (3, 3), activation='relu')
    )
    sequential.add(MaxPooling2D(
        pool_size=(2, 2))
    )
    sequential.add(Dropout(0.5))
    sequential.add(Flatten())
    sequential.add(Dense(
        128, activation='relu')
    )
    sequential.add(Dropout(0.5))
    sequential.add(Dense(
        10, activation='softmax')
    )

    sequential.compile(
        loss='categorical_crossentropy', 
        optimizer='adam', 
        metrics=['accuracy']
    )
    return sequential


def train_sequential(sequential, pictures_size):
    (x_train, y_train), (x_test, y_test) = keras.datasets.mnist.load_data()

    trained_data = x_train.reshape(
        x_train.shape[0], 
        *pictures_size
    )
    test_data = x_test.reshape(
        x_test.shape[0], 
        *pictures_size
    )
    trained_categories = keras.utils.to_categorical(
        y_train, 
        num_classes=10
    )
    test_categories = keras.utils.to_categorical(
        y_test, 
        num_classes=10
    )
    trained_data = trained_data.astype('float32') / 255.0
    test_data = test_data.astype('float32') / 255.0

    sequential.fit(
        trained_data,
        trained_categories,
        epochs=5,
        batch_size=128,
        verbose=1,
        validation_data=(test_data, test_categories)
    )


os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"


pictures_size = 28, 28, 1
sequential = get_sequential_instance(pictures_size)
train_sequential(sequential, pictures_size)
sequential.save('sequential.h5')

