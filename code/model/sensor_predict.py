import os
import json
from datetime import datetime
import numpy as np
import clean as cl
import influx_interact as ii
import model_trainer as mt
import model_predict as mp

# loads setting json files
with open("./threshold_ratios.json") as f:
    threshold_ratios = json.load(f)
with open("./time_step_sizes.json") as f:
    time_step_sizes = json.load(f)

MODEL_SAVE_LOC = None
PERCENTILE_SAVE_LOC = None
SCALER_SAVE_LOC = None

# To be populated with buildings being evaluated
building_list = "Campus Energy Centre"

# Define a few variables with the name of your bucket, organization, and token.
bucket = "MDS2021"
org = "UBC"
# UDL provides public users READ access to the InfluxDB 2.0 instance via this token
token = os.getenv("MDS2021")
url = "http://206.12.92.81:8086"

# Set up time window
# in this case its one day
# can be adjustsed
end_date = datetime.now()
start_date = datetime.timedelta(day=-1)

# create class for
influxdb = ii.influx_class(org, url, bucket, token)

# provides main bucket data, no anomaly labelling
# Readings looks like it coule be Number instead
influx_read_df_for_pred = influxdb.make_query(
    building_list, measurement="READINGS", start=start_date, end=end_date
)

# creates a dictionary of dataframes for each sensor in main_bucket
dfs_for_pred = cl.split_sensors(influx_read_df_for_pred)


for key, df in dfs_for_pred.items():
    dfs_for_pred[key]["Stand_Val"] = cl.std_val_predict(
        dfs_for_pred[key][["Value"]],
        dfs_for_pred[key]["ID"].any(),
        SCALER_SAVE_LOC,
    )

    # creates arrays for sliding windows
    time_steps = time_step_sizes[key]
    window_size = 1
    x_train, y_train = mt.create_sequences(
        df["Stand_Val"], df["Stand_Val"], time_steps, window_size
    )
    x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))

    # set up lists for passing to predict
    timestamps = df["DateTime"].tail(len(df) - x_train.shape[1]).values
    val_nums = df["Value"].tail(len(df) - x_train.shape[1]).values

    loss_percentile = cl.load_loss_percentile(key, file_path=PERCENTILE_SAVE_LOC)
    threshold = threshold_ratios[key] * loss_percentile

    # predicting and prediction formatting
    pred_df = mp.make_prediction(
        key,
        x_train,
        timestamps,
        threshold,
        val_nums,
        MODEL_SAVE_LOC,
        anomaly_type="realtime_anomaly",
    )
    pred_df = pred_df[["uniqueID", "val_num", "realtime_anomaly"]]

    influxdb.write_data(
        pred_df, "PREDICT_ANOMALY", tags=["uniqueID", "realtime_anomaly"]
    )

    influxdb.client.close()
