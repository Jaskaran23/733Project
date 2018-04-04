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

    def __init__(self, pred_type='binary'):
        self.pred_type = pred_type

    def softmax(self, x):
        """Compute softmax values for each sets of scores in x."""
        e_x = np.exp(x - np.max(x))
        return e_x / e_x.sum(axis=0) 

    def daterange(self, start_date, end_date, first_date):
        start = (start_date-first_date).days
        for i, n in enumerate(range(start, (end_date - start_date).days+start)):
            yield (n, start_date + timedelta(i))

    def split_samples(self, pt, daterange, day_block=60, days_future=1):
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

            if self.pred_type == 'binary':
                # Convert to binary up or down movement
                y = (y > 1).astype(int)
            if self.pred_type == 'stochastic':
                # Convert to stochastic vector
                y = self.softmax(y.values.astype(float))
            
            yield (X, y)

    def processXY(self, price_tensor, train_start_date, train_end_date, first_date):
        train = np.array(list(self.split_samples(price_tensor, self.daterange(train_start_date, train_end_date, first_date))))
        train_X = np.stack([np.stack(x) for x in np.stack(train[:,0])])
        train_y = np.stack([np.stack(x) for x in np.stack(train[:,1])])
        return (train_X, train_y)

class CNN(Evaluator):
    """I am a CNN coin evaluator"""
    def __init__(self, pred_type='binary'):
        if pred_type == 'binary':
            self.pred_type = 'binary'
            self.activation = 'sigmoid'
            self.loss = 'binary_crossentropy'
        elif pred_type == 'stochastic':
            self.pred_type = 'stochastic'
            self.activation = 'softmax'
            self.loss = 'mean_squared_error'
        self.model = self.init_model()
        return

    def init_model(self):
        sgd = SGD(lr=0.1, decay=1e-6, momentum=1.9, nesterov=True)

        model = Sequential()
        model.add(Conv2D(filters=4, kernel_size=(1, 3), input_shape=[100,60,8]))
        model.add(Activation('relu'))
        model.add(MaxPooling2D(pool_size=(1,2)))
        model.add(Conv2D(20, (1,29)))
        model.add(Activation('selu'))
        model.add(Conv2D(1, (1,1)))
        model.add(Flatten())
        model.add(Activation(self.activation))

        model.compile(optimizer=sgd,
              loss=self.loss,
              metrics=['accuracy'])
        return model
