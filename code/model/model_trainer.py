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


# def create_sequences(X, y, time_steps=TIME_STEPS):
#     """
#     creates time slices of the data

#     X : pandas column
#     y : pandas column

#     eg:
#     X_train, y_train = create_sequences(train[['value']], train['value'])
#     X_test, y_test = create_sequences(test[['value']], test['value'])
#     """
#     Xs, ys = [], []
#     for i in range(len(X) - time_steps):
#         Xs.append(X.iloc[i : (i + time_steps)].values)
#         ys.append(y.iloc[i + time_steps])

#     return np.array(Xs), np.array(ys)


def create_sequences(X, y, time_steps=30, window=1):
    Xs, ys = [], []
    for i in range(0, len(X) - time_steps, window):
        Xs.append(X.iloc[i : (i + time_steps)].values)
        ys.append(y.iloc[i + time_steps])
    return np.array(Xs), np.array(ys)


def save_loss_percentile(
    col1,
    sensor_name,
    percentile=0.995,
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


def fit_models(data_dict, model_save_loc, threshold_ratio=THRESHOLD):
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
        model, _ = fit_model(x_train, y_train)
        model.save(model_save_loc + key, save_format="h5")

        # # predict on train set
        x_train_pred = model.predict(x_train, verbose=0)
        train_mae_loss = np.mean(np.abs(x_train_pred - x_train), axis=1)
        # print(type(train_mae_loss))
        # print(train_mae_loss.shape)

        loss_percentile = save_loss_percentile(train_mae_loss, key, 99.5)

        # train_score_df = pd.DataFrame(data_dict[key]["train"][TIME_STEPS:]) # num rows - 15
        # train_score_df["loss"] = train_mae_loss # numrows / 15
        # train_score_df["threshold"] = threshold_ratio * loss_percentile
        # train_score_df["uniqueID"] = key
        # train_score_df["model_anomaly"] = (
        #     train_score_df["loss"] > train_score_df["threshold"]
        # )
        # train_score_df.rename(columns={"Datetime": "DateTime"}, inplace=True)
        # train_score_df["val_num"] = data_dict[key]["train"][TIME_STEPS:]["Value"]

        # if "manual_anomaly" not in set(train_score_df.columns):
        #     train_score_df["manual_anomaly"] = False
        # train_score_df.set_index("DateTime", drop=True, inplace=True)

        # # print("inside model trainer")
        # # print(train_score_df.head())
        # # print("inside model trainer")
        # data_dict[key]["train_score_df"] = train_score_df


if __name__ == "__main__":

    # for testing, format will chagne
    # example, will delete after demonstration is understood
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

    raw_train1 = df1.tail(5000).head(4000).copy(deep=True)
    raw_test1 = df1.tail(5000).tail(1000).copy(deep=True)
    raw_train2 = df2.tail(5000).head(4000).copy(deep=True)
    raw_test2 = df2.tail(5000).tail(1000).copy(deep=True)
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
            "train": raw_train1,
            "test": raw_test1,
        },
        "sensor2": {
            "x_train": x2_train,
            "x_test": x2_test,
            "y_train": y2_train,
            "y_test": y2_test,
            "train": raw_train2,
            "test": raw_test2,
        },
    }

    fit_models(data, path_to_models)

    print(data["sensor1"].keys())
    print(data["sensor1"]["train_score_df"].head())
