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

from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS

# how many rows to save for predicting
PREDICITON_HOLDOUT = 100
# if testing then use smaller training set for faster model training
TESTING = True
# unique thresholds for different IDs
THRESHOLDS = {
    "Campus Energy Centre Campus HW Main Meter Power": 0.15,
    "Campus Energy Centre Boiler B-1 Exhaust O2": 0.019,
}
# Used in simulating streaming
TIME_BETWEEN_PREDICTIONS = 60


if __name__ == "__main__":

    start = time.time()

    model_path = "./test_env_models/"
    scaler_path = "./test_env_standardizers/"

    # set up for influx
    token = "mytoken"
    org = "UBC"
    bucket = "MDS2021"
    url = "http://localhost:8086"

    test_query = influx_class(
        org=org,
        url=url,
        bucket=bucket,
        token=token,
    )

    # read from influx
    print("reading data from influx")
    influx_read_df = test_query.make_query(
        location="Campus Energy Centre", measurement="numeric"
    )
    print(influx_read_df.head())
    test_query.client.close()

    # set up influx for writing
    client = InfluxDBClient(url=url, token=token, timeout=30_000)
    write_api = client.write_api(write_options=SYNCHRONOUS)

    # split df based on id
    main_bucket = cl.split_sensors(influx_read_df)

    data_dicts = []
    # first loop to subset the data and processing
    for key, df in main_bucket.items():
        main_bucket[key] = df.tail(PREDICITON_HOLDOUT)
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
        data_dicts.append(cl.model_parser(main_bucket[key], x_train, y_train))

    # second loop to simulate steaming
    for i in range(0, 85):
        for data in data_dicts:

            # collect data for predicting
            data_name = list(data.keys())[0]
            x_for_pred = data[data_name]["x_train"][i]
            x_for_pred = np.reshape(x_for_pred, (1, x_for_pred.shape[0], 1))
            datetime_index = x_for_pred.shape[1] + i
            datetime = data[data_name]["train"].iloc[datetime_index]["DateTime"]
            threshold = THRESHOLDS[data_name]

            # predicting and prediction formatting
            pred = mp.make_prediction(
                data_name,
                x_for_pred,
                [datetime],
                threshold,
                model_path,
            )
            ar_df = pd.DataFrame.from_dict(pred["data"])

            # prep for writing
            ar_df.rename(columns={"anomaly": "val_bool"}, inplace=True)
            ar_df.rename(columns={"Timestamp": "DateTime"}, inplace=True)
            ar_df["uniqueID"] = data[data_name]["train"]["ID"].values[0]
            ar_df["navName"] = data[data_name]["train"]["navName"].values[0]
            ar_df["siteRef"] = "Campus Energy Centre"
            ar_df.set_index("DateTime", drop=True, inplace=True)
            ar_df = ar_df.drop(["loss", "threshold"], axis=1)

            # writing
            write_api.write(
                bucket,
                org,
                record=ar_df,
                data_frame_measurement_name="AR",
                data_frame_tag_columns=["uniqueID", "navName", "siteRef"],
            )
