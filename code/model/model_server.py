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
    hit url with data and model_id parameters
    eg:

    http://127.0.0.1:5000/?model_id=sensor2&data=string_of_data_points
    """

    data = request.json
    params = data["params"]
    x_data = np.array(data["x_data"])
    time_stamps = np.array(data["time_stamps"])
    print("these are the params", params)
    print(params, x_data.shape)

    # takes data as string for now
    # will need to change to accept timestamps (probably?) also
    # look into passing json payload
    # data = request.args.get("data")
    model_id = data["params"]["model_id"]

    # cast and convert to correct dims
    # data = data.split(",")
    # data = [float(x) for x in data]
    # data = np.array(data).reshape((1, len(data), 1))

    # make predictions
    model = keras.models.load_model(f"../../../models/{model_id}")
    x_test_pred = model.predict(x_data, verbose=0)

    # format predictions
    time_steps = x_data.shape[1]
    test_mae_loss = np.mean(np.abs(x_test_pred - x_data), axis=1)
    # test_score_df = pd.DataFrame(x_data[time_steps:])
    test_score_df = pd.DataFrame(time_stamps[time_steps:])

    # test_score_df["Timestamp"] = time_stamps[time_steps:]
    test_score_df["loss"] = test_mae_loss
    test_score_df["threshold"] = THRESHOLD
    test_score_df["anomaly"] = test_score_df["loss"] > test_score_df["threshold"]

    # test_score_df = pd.DataFrame(test_mae_loss, columns=["loss"])
    # test_score_df["threshold"] = threshold
    # test_score_df["anomaly"] = test_score_df["loss"] > test_score_df["threshold"]
    # test_score_df["FiringRate"] = test[TIME_STEPS:]["FiringRate"]

    print("this is the hook")
    print(test_score_df)
    print(test_score_df.shape)
    print("this is the hook")

    # cast for json serialization
    # data = [float(x) for x in data.flatten()]

    return {
        "version": "0.0.1",
        "data": test_score_df.to_json(orient="columns"),
        "model_id": model_id,
    }


print(__name__)
if __name__ == "__main__":
    app.run()
