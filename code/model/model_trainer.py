"""
Functions for training LSTM models
"""
from pickle import dump
from sklearn.preprocessing import StandardScaler

from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM, Dropout, RepeatVector, TimeDistributed

import pandas as pd
import numpy as np


# A point with a MAE larger than this threshold is labeled anomalous
THRESHOLD = 1.5

TIME_STEPS = 15


def create_sequences(X, y, time_steps=15, window=1):
    Xs, ys = [], []
    for i in range(0, len(X) - time_steps + 1, window):
        Xs.append(X.iloc[i : (i + time_steps)].values)
        ys.append(y.iloc[i + time_steps - 1])
    return np.array(Xs), np.array(ys)


def save_loss_percentile(
    col1,
    sensor_name,
    percentile=99.5,
    file_path="./test_env_loss_percentiles/",
):
    """
    saves the percentile to a file during training to be read for prediction
    to be multiplied with the threshold multiplier

    col1 : pandas column
    sensor_name : string
    percentile : float
    """

    file_name = sensor_name + "_loss_percentile.pkl"

    loss_percentile = np.percentile(col1, percentile)

    dump(loss_percentile, open(file_path + file_name, "wb"))

    return loss_percentile


def create_general_lstm_model(shape1, shape2, num_units=128, dropout_rate=0.2):
    """
    Generate the LSTM model
    Currently hard coded to two LSTM layers

    parameters:
    shape1: int, X_train.shape[1]
    shape2: int, X_train.shape[2]

    returns: keras model
    """
    model = Sequential()
    model.add(LSTM(num_units, input_shape=(shape1, shape2)))
    model.add(Dropout(rate=dropout_rate))
    model.add(RepeatVector(shape1))
    model.add(LSTM(num_units, return_sequences=True))
    model.add(Dropout(rate=dropout_rate))
    model.add(TimeDistributed(Dense(shape2)))
    model.compile(optimizer="adam", loss="mae")
    return model


def fit_model(x_train, y_train, model=None):
    """
    fits a lstm model to the data

    x_train : np array with shape (num_rows, length_of_time_slice, 1)
    y_train : np array with shape (num_rows,)

    returns keras model, model history
    """
    if not model:
        model = create_general_lstm_model(x_train.shape[1], x_train.shape[2])

    history = model.fit(
        x_train,
        y_train,
        epochs=100,
        batch_size=32,
        validation_split=0.1,
        callbacks=[
            keras.callbacks.EarlyStopping(monitor="val_loss", patience=10, mode="min")
        ],
        shuffle=False,
    )

    return model, history


def fit_models(
    data_dict,
    model_save_loc,
    percentile_save_loc="./test_env_loss_percentiles/",
):
    """
    takes the data_dict and trains and saves a model for each of the data
    modifies the input data_dict to have a train predictions dataframe

    data_dict: dict with {sensor_id: data}
    where data is a dict with keys :
        dict_keys(['x_train', 'x_test', 'y_train', 'y_test', 'raw_train', 'raw_test'])

    where x_train, x_test, y_train, y_test are the train/test subsets that have been windowed

    and raw_train and raw_test are dataframes with columns at least ["Timestamp", "value"]
    where value is un-scaled/un-standardized

    data_dict is modified to have a new key value pair
    key = `train_score_df`
    value = `df with columns [Timestamp, value, loss, threshold, anomaly]`
    where anomaly will be AM

    returns None
    """

    for key in data_dict:

        # train model
        x_train = data_dict[key]["x_train"]
        y_train = data_dict[key]["y_train"]
        x_eval = data_dict[key]["x_eval"]
        model, _ = fit_model(x_train, y_train)
        model.save(model_save_loc + key, save_format="h5")

        x_eval_pred = model.predict(x_eval, verbose=0)
        train_mae_loss = np.mean(np.abs(x_eval_pred - x_eval), axis=1)

        save_loss_percentile(train_mae_loss, key, 99.5, percentile_save_loc)
