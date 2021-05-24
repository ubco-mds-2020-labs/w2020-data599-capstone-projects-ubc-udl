"""
Preps the data from sensor2 to be trained or predicted
"""

from tensorflow import keras
from sklearn.preprocessing import StandardScaler

import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM, Dropout, RepeatVector, TimeDistributed

import pandas as pd
import numpy as np

from flask import Flask, request

app = Flask(__name__)

THRESHOLD = 1.5
TIME_STEPS = 15


def p2f(value):
    """
    data formatting for sensor2
    """
    return float(value.strip("ppm"))


# serve predictions from root, pass item string in qs
@app.route("/")
def hello():

    # takes data as string for now
    # will need to change to accept timestamps (probably?) also
    # look into passing json payload
    data = request.args.get("item")
    model_version = request.args.get("model_version")

    print("this is the data")
    data = data.split(",")
    data = [float(x) for x in data]
    print(data)
    print("this is the data")

    # cast to np array and the correct dims for predicting
    data = np.array(data).reshape(1, len(data), 1)

    # make predictions
    model = keras.models.load_model("../../../models/sensor2_model")
    X_test_pred = model.predict(data, verbose=0)

    # format predictions
    test_mae_loss = np.mean(np.abs(X_test_pred - data), axis=1)
    # test_score_df = pd.DataFrame(data[TIME_STEPS:])
    test_score_df = pd.DataFrame(test_mae_loss, columns=["loss"])
    # test_score_df["loss"] = test_mae_loss
    test_score_df["threshold"] = THRESHOLD
    test_score_df["anomaly"] = test_score_df["loss"] > test_score_df["threshold"]
    # test_score_df["value"] = data[TIME_STEPS:]["value"]

    print("this is the hook")
    print(test_score_df)
    print("list data", type(list(data)))
    print("anomaly columns", type(str(test_score_df["anomaly"].values[0])))
    print("this is the hook")

    data = [float(x) for x in data.flatten()]

    return {
        "version": "0.0.1",
        "data": list(data),
        "anomaly_status": str(test_score_df["anomaly"].values[0]),
        "model_version": model_version,
    }


print(__name__)
if __name__ == "__main__":
    app.run()
