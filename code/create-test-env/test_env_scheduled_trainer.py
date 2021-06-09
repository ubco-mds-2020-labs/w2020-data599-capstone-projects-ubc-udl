"""
retrains models for each id on a schedule.
"""

import sys
import time

import numpy as np
import pandas as pd

sys.path.append("..")

import model.clean as cl
import model.model_trainer as mt
from model.influx_interact import influx_class


# if testing then use smaller training set for faster model training
TESTING = True
# unique thresholds for different IDs
THRESHOLDS = {
    "Campus Energy Centre Campus HW Main Meter Power": 0.09,
    "Campus Energy Centre Boiler B-1 Exhaust O2": 0.019,
    "Campus Energy Centre Boiler B-1 Gas Pressure": 0.0725,
    "Campus Energy Centre Campus HW Main Meter Entering Water Temperature": 0.02938,
    "Campus Energy Centre Campus HW Main Meter Flow": 0.043,
}
# END TIME FOR TRAINING SET
END_TIME = 1613109600
#
REMOVE_ANOMALOUS = True
REMOVE_ANOMALOUS_DATA = [
    "Campus Energy Centre Campus HW Main Meter Entering Water Temperature"
]

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
        end=END_TIME,
    )

    # split df based on id
    main_bucket = cl.split_sensors(influx_read_df)

    for key, df in main_bucket.items():
        print("Training for : {}".format(key))

        # removes anomalies to only train on normal data
        if REMOVE_ANOMALOUS:
            if key in REMOVE_ANOMALOUS_DATA:
                PATH_TO_CSVS = "../../data/labelled-skyspark-data/"
                csv = "CEC_compiled_data_2b_updated.csv"
                df_with_manual_anomaly = pd.read_csv(
                    PATH_TO_CSVS + csv, parse_dates=["Datetime"]
                )
                df_with_manual_anomaly["Datetime"] = pd.to_datetime(
                    df_with_manual_anomaly["Datetime"], utc=True
                )
                df = df.merge(
                    df_with_manual_anomaly[["Datetime", "Anomaly"]],
                    how="left",
                    left_on="DateTime",
                    right_on="Datetime",
                )
                df = df.loc[df["Anomaly"] == False]
                df = df.drop(columns=["DateTime"], axis=1)
                am_df.rename(columns={"Anomaly": "manual_anomaly"}, inplace=True)

        # creates standardized column for each sensor in main bucket
        df["Stand_Val"] = cl.std_val_train(
            df[["Value"]],
            main_bucket[key]["ID"].any(),
            scaler_path,
        )

        if TESTING:
            df = df.tail(5000)

        # creates arrays for sliding windows
        x_train, y_train = mt.create_sequences(df["Stand_Val"], df["Stand_Val"])
        x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))

        normal_dict = cl.model_parser(df, x_train, y_train)

        threshold = THRESHOLDS[key]
        mt.fit_models(normal_dict, model_path, threshold)

        # for writing AM to influx
        am_df = normal_dict[key]["train_score_df"]
        am_df.rename(columns={"anomaly": "model_anomaly"}, inplace=True)
        am_df.rename(columns={"ID": "uniqueID"}, inplace=True)
        am_df.rename(columns={"Datetime": "DateTime"}, inplace=True)
        am_df["val_num"] = df["Value"].iloc[x_train.shape[1] :]
        # only if it hasnt already been created earlier
        if "manual_anomaly" not in set(am_df.columns):
            am_df["manual_anomaly"] = False
        am_df.set_index("DateTime", drop=True, inplace=True)
        am_df = am_df[["uniqueID", "model_anomaly", "val_num", "manual_anomaly"]]

        influx_conn.write_data(am_df, "TRAINING_ANOMALY")

    print("time taken {}".format(time.time() - start))
    influx_conn.client.close()
