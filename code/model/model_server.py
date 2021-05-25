"""
Preps the data from sensor2 to be trained or predicted
"""

from tensorflow import keras

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
def serve_prediction():
    """
    hit url with data and model_id parameters
    eg:

    http://127.0.0.1:5000/?model_id=sensor2&data=string_of_data_points
    """

    # takes data as string for now
    # will need to change to accept timestamps (probably?) also
    # look into passing json payload
    data = request.args.get("data")
    model_id = request.args.get("model_id")

    # cast and convert to correct dims
    data = data.split(",")
    data = [float(x) for x in data]
    data = np.array(data).reshape((1, len(data), 1))

    # make predictions
    model = keras.models.load_model(f"../../../models/{model_id}")
    x_test_pred = model.predict(data, verbose=0)

    # format predictions
    test_mae_loss = np.mean(np.abs(x_test_pred - data), axis=1)
    test_score_df = pd.DataFrame(test_mae_loss, columns=["loss"])
    test_score_df["threshold"] = THRESHOLD
    test_score_df["anomaly"] = test_score_df["loss"] > test_score_df["threshold"]

    # cast for json serialization
    data = [float(x) for x in data.flatten()]

    return {
        "version": "0.0.1",
        "data": list(data),
        "anomaly_status": str(test_score_df["anomaly"].values[0]),
        "model_id": model_id,
    }


print(__name__)
if __name__ == "__main__":
    app.run()
