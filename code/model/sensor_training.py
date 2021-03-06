"""
This wil just create a model for every sensor that is queried.
Some code is semipseudo code for untill InfluxDB is going.
"""
import os
import json
import influx_interact as ii
import clean as cl
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

SENSOR_LIST = [
    "Campus Energy Centre Campus HW Main Meter Power",
    "Campus Energy Centre Campus HW Main Meter Entering Water Temperature",
    "Campus Energy Centre Campus HW Main Meter Flow",
    "Campus Energy Centre Boiler B-1 Gas Pressure",
    "Campus Energy Centre Boiler B-1 Exhaust O2",
]

# To be populated with buildings being evaluated
building_list = "Campus Energy Centre"

# Define a few variables with the name of your bucket, organization, and token.
bucket = "MDS2021"
org = "UBC"
# UDL provides public users READ access to the InfluxDB 2.0 instance via this token
token = os.getenv("MDS2021")
url = "http://206.12.92.81:8086"

# create class for
influxdb = ii.influx_class(org, url, bucket, token)

# provides main bucket data, no anomaly labelling
# Readings looks like it coule be Number instead
influx_data = influxdb.make_query(
    building_list,
    measurement="READINGS",
    id=SENSOR_LIST,
)

# creates a dictionary of dataframes for each sensor in sensors_dict
sensors_dict = cl.split_sensors(influx_data)

# create empty dictionary
normal_bucket = {}
abnormal_bucket = {}

for key, df in sensors_dict.items():
    print("Training for : {}".format(key))

    # Delete data that is about to be written, to prevent duplicaete write on timestamp
    delete_api = influxdb.client.delete_api()
    min_time = df["DateTime"].values[0]
    max_time = df["DateTime"].values[-1]
    delete_api.delete(
        str(min_time) + "Z",
        str(max_time) + "Z",
        '_measurement="TRAINING_ANOMALY" AND uniqueID="{}"'.format(key),
        bucket=bucket,
        org=org,
    )

    # creates standardized column for each sensor in main bucket
    sensors_dict[key]["Stand_Val"] = cl.std_val_train(
        df[["Value"]], sensors_dict[key]["ID"].any(), SCALER_SAVE_LOC
    )

    # train on only data points not flagged manually
    df = df[df.manual_anomaly is not True]

    # creates sequences for sliding windows for training
    threshold_ratio = threshold_ratios[key]
    time_steps = time_step_sizes[key]

    window_size = time_steps
    x_train, y_train = mt.create_sequences(
        df["Stand_Val"], df["Stand_Val"], time_steps, window_size
    )

    x_eval, y_eval = mt.create_sequences(
        df["Stand_Val"], df["Stand_Val"], time_steps, 1
    )

    # format needed for fit model
    normal_dict = cl.model_parser(normal_bucket[key], x_train, y_train, x_eval)

    # creates model file for training data.
    mt.fit_models(normal_dict, MODEL_SAVE_LOC, PERCENTILE_SAVE_LOC)

    # creates sequences for sliding windows for predicting on the train set
    timestamps = df["DateTime"].tail(len(df) - x_train.shape[1] + 1).values
    val_nums = df["Value"].tail(len(df) - x_train.shape[1] + 1).values
    manual_anomaly = df["manual_anomaly"].tail(len(df) - x_train.shape[1]).values
    loss_percentile = cl.load_loss_percentile(key, file_path=PERCENTILE_SAVE_LOC)
    threshold = loss_percentile * threshold_ratio

    # predicting and prediction formatting
    pred_df = mp.make_prediction(
        key,
        x_eval,
        timestamps,
        threshold,
        val_nums,
        MODEL_SAVE_LOC,
        anomaly_type="model_anomaly",
        manual_anomaly=manual_anomaly,
    )
    pred_df = pred_df[["uniqueID", "val_num", "model_anomaly", "manual_anomaly"]]

    print(pred_df.groupby("model_anomaly").count())
    print(pred_df.groupby("manual_anomaly").count())

    # write to influxDB
    influxdb.write_data(
        pred_df,
        "TRAINING_ANOMALY",
        tags=["uniqueID", "model_anomaly", "manual_anomaly"],
    )

    influxdb.client.close()
