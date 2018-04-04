import keras
from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten, Activation
from keras.layers import Conv2D, MaxPooling2D, ELU
from keras.optimizers import SGD
from keras import backend as K
from datetime import timedelta, date
import numpy as np
import pandas as pd

class Evaluator:
    """I am a coin evaluator"""

    def daterange(self, start_date, end_date, first_date):
        start = (start_date-first_date).days
        for i, n in enumerate(range(start, (end_date - start_date).days+start)):
            yield (n, start_date + timedelta(i))

    def split_samples(self, pt, daterange, day_block=60, days_future=1, pred_type='binary'):
        for t, _ in daterange:
            X = pt[:,t:t+day_block,:].copy()
            y = pt[:,t+day_block+days_future,3].copy() # 3 is the index of closing price in features
            
            # normalize prices with respect to the 'current' price. ie. the final closing price before our prediction
            # price features are open, high, low, close, with indices 0, 1, 2, 3
            current_prices = X[:,-1,3].copy()
            
            X[:, :, 0] = X[:,:,0] / current_prices[:] -1
            X[:, :, 1] = X[:,:,1] / current_prices[:] -1
            X[:, :, 2] = X[:,:,2] / current_prices[:] -1
            X[:, :, 3] = X[:,:,3] / current_prices[:] -1
            
            y = y / current_prices

            if pred_type == 'binary':
                # Convert to binary up or down movement
                y = (y > 1).astype(int)
            if pred_type == 'stochastic':
                # Convert to stochastic vector
                y = (y > 1).astype(int)
            
            yield (X, y)

    def processXY(self, price_tensor, train_start_date, train_end_date, first_date):
        train = np.array(list(self.split_samples(price_tensor, self.daterange(train_start_date, train_end_date, first_date))))
        train_X = np.stack([np.stack(x) for x in np.stack(train[:,0])])
        train_y = np.stack([np.stack(x) for x in np.stack(train[:,1])])
        return (train_X, train_y)

class CNN(Evaluator):
    """I am a CNN coin evaluator"""
    def __init__(self, activation='Sigmoid'):
        self.model = self.init_model()
        self.activation = activation
        if activation == 'Sigmoid':
            self.loss = 'binary_crossentroyp'
        else:
            self.loss = 'mean_squared_error'
        return

    def init_model(self):
        sgd = SGD(lr=0.1, decay=1e-6, momentum=1.9)

        model = Sequential()
        model.add(Conv2D(filters=4, kernel_size=(1, 3), input_shape=[100,60,8]))
        model.add(Activation('relu'))
        model.add(Conv2D(20, (1,58)))
        model.add(Activation('selu'))
        model.add(Conv2D(1, (1,1)))
        model.add(Flatten())
        model.add(Activation(self.activation))

        model.compile(optimizer=sgd,
              loss=self.loss,
              metrics=['accuracy'])
        return model
