
import keras
from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten, Activation
from keras.layers import Conv2D, MaxPooling2D, ELU
from keras import backend as K


class Evaluator:
    """I am a coin evaluator"""
    def __init__(self):
        self.model = self.init_model()
        return

    def init_model(self):
        model = Sequential()
        model.add(Conv2D(filters=4,kernel_size=(1, 3), input_shape=[100,60,8]))
        model.add(Activation('elu'))
        model.add(Conv2D(20, (1,58)))
        model.add(Activation('elu'))
        model.add(Conv2D(1, (1,1)))
        model.add(Activation('sigmoid'))

        model.compile(optimizer='rmsprop',
              loss='binary_crossentropy',
              metrics=['accuracy'])
        return model


