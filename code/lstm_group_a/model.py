"""
Trains a lstm for the group a cluster of sensors
"""

from sklearn.preprocessing import StandardScaler

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM, Dropout, RepeatVector, TimeDistributed

import pandas as pd
import numpy as np


def create_model(shape1, shape2):
    """
    Generate the LSTM model

    parameters:
    shape1: int, X_train.shape[1]
    shape2: int, X_train.shape[2]

    returns: keras model
    """
    model = Sequential()
    model.add(LSTM(128, input_shape=(shape1, shape2)))
    model.add(Dropout(rate=0.2))
    model.add(RepeatVector(shape1))
    model.add(LSTM(128, return_sequences=True))
    model.add(Dropout(rate=0.2))
    model.add(TimeDistributed(Dense(shape2)))
    model.compile(optimizer="adam", loss="mae")
    return model
