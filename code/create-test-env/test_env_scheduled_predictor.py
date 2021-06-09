"""
simulates streaming predictions for the test env
"""

import time


import sys

sys.path.append("..")

import model.clean as cl
import model.model_trainer as mt
from model.influx_interact import influx_class
import model.model_predict as mp

import numpy as np
import pandas as pd

# unique thresholds for different IDs
THRESHOLDS = {
    "Campus Energy Centre Campus HW Main Meter Power": 0.09,
    "Campus Energy Centre Boiler B-1 Exhaust O2": 0.019,
    "Campus Energy Centre Boiler B-1 Gas Pressure": 0.0725,
    "Campus Energy Centre Campus HW Main Meter Entering Water Temperature": 0.02938,
    "Campus Energy Centre Campus HW Main Meter Flow": 0.043,
}
# END TIME FOR TRAINING SET BECOMES PREDICTING'S START TIME
START_TIME = 1613109600
END_TIME = 1613196000


if __name__ == "__main__":

    start = time.time()

    model_path = "./test_env_models/"
    scaler_path = "./test_env_standardizers/"

    # set up for influx
    token = "mytoken"
    org = "UBC"
    bucket = "MDS2021"
    url = "http://localhost:8086"

    influx_conn = influx_class(
        org=org,
        url=url,
        bucket=bucket,
        token=token,
    )

    # read from influx
    print("reading data from influx")
    influx_read_df = influx_conn.make_query(
        location="Campus Energy Centre",
        measurement="READINGS",
        start=START_TIME,
        end=END_TIME,
    )

    # split df based on id
    main_bucket = cl.split_sensors(influx_read_df)

    for key, df in main_bucket.items():
        main_bucket[key]["Stand_Val"] = cl.std_val_predict(
            main_bucket[key][["Value"]],
            main_bucket[key]["ID"].any(),
            scaler_path,
        )

        # creates arrays for sliding windows
        x_train, y_train = mt.create_sequences(
            main_bucket[key]["Stand_Val"], main_bucket[key]["Stand_Val"]
        )
        x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))
        timestamps = df["DateTime"].tail(len(df) - x_train.shape[1]).values
        threshold = THRESHOLDS[key]

        # predicting and prediction formatting
        pred = mp.make_prediction(
            key,
            x_train,
            timestamps,
            threshold,
            model_path,
        )
        ar_df = pd.DataFrame.from_dict(pred["data"])

        # prep for writing
        ar_df.rename(columns={"anomaly": "realtime_anomaly"}, inplace=True)
        ar_df.rename(columns={"Timestamp": "DateTime"}, inplace=True)
        ar_df["uniqueID"] = key
        ar_df.set_index("DateTime", drop=True, inplace=True)
        ar_df["val_num"] = df["Value"].tail(len(df) - x_train.shape[1]).values
        ar_df = ar_df[["uniqueID", "val_num", "realtime_anomaly"]]

        influx_conn.write_data(ar_df, "PREDICT_ANOMALY")

    influx_conn.client.close()
