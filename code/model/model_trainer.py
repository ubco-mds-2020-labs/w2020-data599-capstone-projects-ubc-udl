"""
Functions for training LSTM models
"""

from sklearn.preprocessing import StandardScaler

from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM, Dropout, RepeatVector, TimeDistributed

import pandas as pd
import numpy as np


TIME_STEPS = 15


def create_sequences(X, y, time_steps=TIME_STEPS):
    """
    creates time slices of the data

    X : pandas column
    y : pandas column

    eg:
    X_train, y_train = create_sequences(train[['value']], train['value'])
    X_test, y_test = create_sequences(test[['value']], test['value'])
    """
    Xs, ys = [], []
    for i in range(len(X) - time_steps):
        Xs.append(X.iloc[i : (i + time_steps)].values)
        ys.append(y.iloc[i + time_steps])

    return np.array(Xs), np.array(ys)


def create_general_lstm_model(shape1, shape2):
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


def fit_models(data_dict, model_save_loc):
    """
    takes the data_dict and trains and saves a model for each of the data

    data_dict: dict with {data_name: data}

    returns None
    """

    for key in data_dict:
        x_train = data_dict[key]["x_train"]
        y_train = data_dict[key]["y_train"]
        model, _ = fit_model(x_train, y_train)
        model.save(model_save_loc + key, save_format="h5")

        # TODO predict on train data and return predictions


if __name__ == "__main__":

    # for testing, format will chagne
    path_to_models = "../../../models/"
    data_save_loc = "../../../data/"
    df1 = pd.read_csv(f"{data_save_loc}Campus Energy Centre_1.csv")
    df2 = pd.read_csv(f"{data_save_loc}Campus Energy Centre_2.csv")

    df1.columns = ["Timestamp", "value"]
    df2.columns = ["Timestamp", "value"]

    df1 = df1.dropna()
    df2 = df2.dropna()

    df1["value"] = df1["value"].apply(lambda x: float(x.strip("%")) / 100)
    df2["value"] = df2["value"].apply(lambda x: float(x.strip("ppm")))

    train1 = df1.tail(5000).head(4000)
    test1 = df1.tail(5000).tail(1000)
    train2 = df2.tail(5000).head(4000)
    test2 = df2.tail(5000).tail(1000)

    scaler = StandardScaler()
    scaler1 = scaler.fit(train1[["value"]])
    scaler2 = scaler.fit(train2[["value"]])

    train1["value"] = scaler.transform(train1[["value"]])
    test1["value"] = scaler.transform(test1[["value"]])
    train2["value"] = scaler.transform(train2[["value"]])
    test2["value"] = scaler.transform(test2[["value"]])

    x1_train, y1_train = create_sequences(train1[["value"]], train1["value"])
    x2_train, y2_train = create_sequences(train2[["value"]], train2["value"])
    x1_test, y1_test = create_sequences(test1[["value"]], test1["value"])
    x2_test, y2_test = create_sequences(test2[["value"]], test2["value"])

    data = {
        "sensor1": {
            "x_train": x1_train,
            "x_test": x1_test,
            "y_train": y1_train,
            "y_test": y1_test,
        },
        "sensor2": {
            "x_train": x2_train,
            "x_test": x2_test,
            "y_train": y2_train,
            "y_test": y2_test,
        },
    }

    fit_models(data, path_to_models)
