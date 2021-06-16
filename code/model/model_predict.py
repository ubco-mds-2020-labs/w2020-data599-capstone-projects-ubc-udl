"""
makes prediction on one set of data with one model
"""

from tensorflow import keras

import pandas as pd
import numpy as np


def make_prediction(
    model_id, x_data, time_stamps, threshold, model_path, anomaly_type="anomaly"
):
    """
    model_id: string, name of the model to load
    x_data: np array of shape (num_rows, time_steps, 1)
    time_stamps: time_stamps: list, timestamps of prediction points,
    find this out before passing
    threshold: float, for flagging as anomalous
    model_path: string, path to saved model
    anomaly_type: string, what to name the anomaly column (eg manual_anomaly, model_anomaly, or realtime_anomaly)
    """
    # make predictions
    model = keras.models.load_model(model_path + model_id)
    x_test_pred = model.predict(x_data, verbose=0)

    # format predictions
    test_mae_loss = np.mean(np.abs(x_test_pred - x_data), axis=1)
    test_score_df = pd.DataFrame(time_stamps, columns=["Timestamp"])
    test_score_df["loss"] = test_mae_loss
    test_score_df["DateTime"] = threshold
    test_score_df[anomaly_type] = test_score_df["loss"] > test_score_df["threshold"]

    return_data = {
        "DateTime": test_score_df["DateTime"].values.tolist(),
        "loss": test_score_df["loss"].values.tolist(),
        "threshold": test_score_df["threshold"].values.tolist(),
        anomaly_type: test_score_df["anomaly"].values.tolist(),
    }

    return {
        "version": "0.0.1",
        "data": return_data,
        "model_id": model_id,
    }
