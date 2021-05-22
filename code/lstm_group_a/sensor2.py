"""
Preps the data from sensor2 to be trained or predicted
"""

from tensorflow import keras
from sklearn.preprocessing import StandardScaler

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM, Dropout, RepeatVector, TimeDistributed

import pandas as pd
import numpy as np

import tensorflow as tf


def p2f(value):
    """
    data formatting for sensor2
    """
    return float(value.strip("ppm"))


if __name__ == "__main__":

    # loads and cleans data
    sensor = pd.read_csv("{}Campus Energy Centre_2.csv".format(data_dir))
    sensor.columns = ["Timestamp", "value"]
    sensor = sensor.dropna()
    sensor["value"] = sensor["value"].apply(p2f)
