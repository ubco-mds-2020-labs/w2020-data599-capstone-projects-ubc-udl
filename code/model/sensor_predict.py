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
    main_bucket[key]["Stand_Val"] = cl.standardize_values(df[["Value"]])

    # creates arrays for sliding windows
    x_data, y_data = mt.create_sequences(
        main_bucket[key][["Value"]], main_bucket[key]["Value"]
    )

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
