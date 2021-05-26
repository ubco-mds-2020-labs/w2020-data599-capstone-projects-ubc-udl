"""
passes predictions to the model server via flask request
"""

import json
import requests

import numpy as np
import pandas as pd

from sklearn.preprocessing import StandardScaler

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


FLASK_URL = "http://127.0.0.1:5000/"

if __name__ == "__main__":

    data_save_loc = "../../../data/"
    df1 = pd.read_csv(f"{data_save_loc}Campus Energy Centre_1.csv")

    df1.columns = ["Timestamp", "value"]

    df1 = df1.dropna()

    df1["value"] = df1["value"].apply(lambda x: float(x.strip("%")) / 100)

    train11 = df1.tail(5000).head(4000).copy(deep=True)
    test11 = df1.tail(5000).tail(1000).copy(deep=True)
    train1 = df1.tail(5000).head(4000)
    test1 = df1.tail(5000).tail(1000)

    scaler = StandardScaler()
    scaler1 = scaler.fit(train1[["value"]])

    train1["value"] = scaler.transform(train1[["value"]])
    test1["value"] = scaler.transform(test1[["value"]])

    x1_train, y1_train = create_sequences(train1[["value"]], train1["value"])
    x1_test, y1_test = create_sequences(test1[["value"]], test1["value"])

    time_stamps_to_pass = test1["Timestamp"][TIME_STEPS:].tolist()

    print(len(time_stamps_to_pass))
    print(x1_test.shape)

    data = {
        "model_id": "sensor1",
        "x_data": x1_test.tolist(),
        "time_stamps": time_stamps_to_pass,
    }

    response = requests.post(FLASK_URL, json=data)
    response_json = json.loads(response.content)
    print(response_json["data"])
    df = pd.DataFrame.from_dict(response_json["data"], orient="columns")
    print(df.head())
