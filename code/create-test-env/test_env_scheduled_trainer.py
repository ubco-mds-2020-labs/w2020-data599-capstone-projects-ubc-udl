"""
retrains models for each id on a schedule.
"""

import time

import sys

sys.path.append("..")

import model.clean as cl
import model.model_trainer as mt
from model.influx_interact import influx_class

import numpy as np

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

    for key, df in main_bucket.items():
        # creates standardized column for each sensor in main bucket
        main_bucket[key]["Stand_Val"] = cl.std_val_train(
            df[["Value"]],
            main_bucket[key]["ID"].any(),
            scaler_path,
        )

        # save 1000 rows for prediction testing
        df_subset = df.head(len(df) - PREDICITON_HOLDOUT)

        if TESTING:
            df_subset = df_subset.tail(5000)

        # creates arrays for sliding windows
        x_train, y_train = mt.create_sequences(
            df_subset["Stand_Val"], df_subset["Stand_Val"]
        )
        x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))

        # format needed for fit model

        normal_dict = cl.model_parser(df_subset, x_train, y_train)

        threshold = THRESHOLDS[key]
        mt.fit_models(normal_dict, model_path, threshold)

        # for writing AM to influx
        am_df = normal_dict[key]["train_score_df"]
        am_df.rename(columns={"anomaly": "val_bool"}, inplace=True)
        am_df.rename(columns={"ID": "uniqueID"}, inplace=True)
        am_df.rename(columns={"Datetime": "DateTime"}, inplace=True)
        am_df["navName"] = "Energy"
        am_df["siteRef"] = "Campus Energy Centre"
        am_df.set_index("DateTime", drop=True, inplace=True)
        am_df = am_df.drop(["Value", "Stand_Val", "loss", "threshold", "value"], axis=1)

        write_api.write(
            bucket,
            org,
            record=am_df,
            data_frame_measurement_name="AM",
            data_frame_tag_columns=["uniqueID", "navName", "siteRef"],
        )

    print("time taken {}".format(time.time() - start))
