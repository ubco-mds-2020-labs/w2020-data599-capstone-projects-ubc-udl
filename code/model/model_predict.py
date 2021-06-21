"""
makes prediction on one set of data with one model
"""

from tensorflow import keras

import pandas as pd
import numpy as np


def make_prediction(
    model_id,
    x_data,
    time_stamps,
    threshold,
    values,
    model_path,
    anomaly_type="anomaly",
    manual_anomaly=None,
):
    """
    model_id: string, name of the model to load
    x_data: np array of shape (num_rows, time_steps, 1)
    time_stamps: time_stamps: list, timestamps of prediction points,
    find this out before passing
    threshold: float, for flagging as anomalous
    values: unscaled values to be added back to the resulting dataframe
    model_path: string, path to saved model
    anomaly_type: string, what to name the
    anomaly column (eg manual_anomaly, model_anomaly, or realtime_anomaly)
    extra: pandas series, eg if passing in manual anomalies
    """
    # make predictions
    model = keras.models.load_model(model_path + model_id)
    x_test_pred = model.predict(x_data, verbose=0)

    # format predictions
    test_mae_loss = np.mean(np.abs(x_test_pred - x_data), axis=1)
    test_score_df = pd.DataFrame(time_stamps, columns=["DateTime"])
    test_score_df["loss"] = test_mae_loss
    test_score_df["threshold"] = threshold
    test_score_df[anomaly_type] = test_score_df["loss"] > test_score_df["threshold"]
    test_score_df["uniqueID"] = model_id
    test_score_df["val_num"] = values
    if manual_anomaly is not None:
        test_score_df["manual_anomaly"] = manual_anomaly
    test_score_df.set_index("DateTime", drop=True, inplace=True)

    return test_score_df
