"""
Preps the data from sensor2 to be trained or predicted
"""
from tensorflow import keras

import pandas as pd
import numpy as np

from flask import Flask, request

app = Flask(__name__)

THRESHOLD = 1.5


# serve predictions from root, pass item string in qs
@app.route("/", methods=["POST"])
def serve_prediction():
    """
    request to flask server to make predictions on passed data

    call like:

    ```
    data = {
        "model_id": sensor1,
        "x_data": x1_test.tolist(),
        "time_stamps": time_stamps_to_pass,
    }

    response = requests.post(FLASK_URL, json=data)
    ```
    model_id: string, group model id

    x_data: list, to be cast to a np array of shape (num_rows, time_steps, 1)

    time_stamps: list, timestamps of prediction points, find this out before passing

    FLASK_URL: string, path to the flask local host server
        eg: `FLASK_URL = "http://127.0.0.1:5000/"`

    returns: dict
    ```
        return {
        "version": "0.0.1",
        "data": return_data,
        "model_id": model_id,
    }
    ```

    where return_data is a dataframe that has been decomposed into a dict
    ```
    return_data = {
        "Timestamp": test_score_df["Timestamp"].values.tolist(),
        "loss": test_score_df["loss"].values.tolist(),
        "threshold": test_score_df["threshold"].values.tolist(),
        "anomaly": test_score_df["anomaly"].values.tolist(),
    }
    ```
    where the anomaly column becomes the AR

    """

    # unpack request data
    data = request.json
    model_id = data["model_id"]
    x_data = np.array(data["x_data"])
    time_stamps = np.array(data["time_stamps"])

    # make predictions
    model = keras.models.load_model(f"../../../models/{model_id}")
    x_test_pred = model.predict(x_data, verbose=0)

    # format predictions
    test_mae_loss = np.mean(np.abs(x_test_pred - x_data), axis=1)
    test_score_df = pd.DataFrame(time_stamps, columns=["Timestamp"])
    test_score_df["loss"] = test_mae_loss
    test_score_df["threshold"] = THRESHOLD
    test_score_df["anomaly"] = test_score_df["loss"] > test_score_df["threshold"]

    return_data = {
        "Timestamp": test_score_df["Timestamp"].values.tolist(),
        "loss": test_score_df["loss"].values.tolist(),
        "threshold": test_score_df["threshold"].values.tolist(),
        "anomaly": test_score_df["anomaly"].values.tolist(),
    }

    return {
        "version": "0.0.1",
        "data": return_data,
        "model_id": model_id,
    }


print(__name__)
if __name__ == "__main__":
    app.run()
