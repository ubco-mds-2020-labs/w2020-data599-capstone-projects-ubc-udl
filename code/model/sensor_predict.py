import influx_interact as ii
import clean as cl
import os
from datetime import datetime
import model_trainer as mt
import model_predict as mp

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
main_bucket = influxdb.make_query(
    building_list, measurements="READINGS", start=start_date, end=end_date
)

# creates a dictionary of dataframes for each sensor in main_bucket
main_bucket = cl.split_sensors(main_bucket)

predictions = {}
model_id = {}

for key, df in main_bucket.items():
    # creates standardized column for each sensor in main bucket
    main_bucket[key]["Stand_Val"] = cl.std_val_predict(
        df[["Value"]], main_bucket[key]["ID"].any()
    )

    # train on only data points not flagged manually
    df = df[df.manual_anomaly != True]

    # creates arrays for sliding windows
    x_data, y_data = mt.create_sequences(
        main_bucket[key][["Value"]], main_bucket[key]["Value"]
    )
    # creates sequences for sliding windows for training
    threshold_ratio = THRESHOLD_RATIOS[key]
    time_steps = TIME_STEP_SIZES[key]
    window_size = time_steps
    x_train, y_train = mt.create_sequences(
        df["Stand_Val"], df["Stand_Val"], time_steps, window_size
    )
    x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))
    x_eval, y_eval = mt.create_sequences(
        df["Stand_Val"], df["Stand_Val"], time_steps, 1
    )
    x_eval = np.reshape(x_eval, (x_eval.shape[0], x_eval.shape[1], 1))

    # potential here for get model ids
    # can add string to whatever we name
    # the models as
    model_id = main_bucket[key]["ID"].any()

    # gets predictions
    predictions = mp.make_prediction(
        model_id=model_id,
        x_data=x_data,
        time_stamps=main_bucket[key]["Datetime"],
        threshold="threshold set somehow",
    )

    # Add anomaly values back to main bucket
    main_bucket[key]["AR"] = predictions["Anomaly"]

    # Write to influx Training and Influx Realtime Buckets
    influxdb.write_data(main_bucket[key], "CHECK_ANOMALY")
    influxdb.write_data(main_bucket[key], "TRAINING")
