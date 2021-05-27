import pandas as pd
import numpy as np
from influx_interact import ii
from clean import cl
import os

# these to be added with Mitch's PR
# from lstm import lstm
# from process_results import *

# To be populated with buildings being evaluated
building_list = "Campus Energy Centre"

# Define a few variables with the name of your bucket, organization, and token.
bucket = "MDS2021"
org = "UBC"
# UDL provides public users READ access to the InfluxDB 2.0 instance via this token
token = os.environ["MDS2021"]
url = "http://206.12.92.81:8086"

# create class for
influxdb = ii.influx_class(org, url, bucket, token)

# provides main bucket data, no anomaly labelling
main_bucket = influxdb.make_query(building_list, measurements="READINGS")

# provides training bucket data
training_bucket = influxdb.make_query(building_list, measurement="TRAINING")

# creates a dictionary of dataframes for each sensor in main_bucket
main_bucket = cl.split_sensors(main_bucket)

# creates a dictionary of dataframes for each sensor in main_bucket
training_bucket = cl.split_sensors(training_bucket)

# create empty dictionary
joined_bucket = {}

# creates standardized column for each sensor in main bucket
for key, df in main_bucket.items():
    main_bucket[key]["Stand_Val"] = cl.standardize_values(df[["Value"]])

    # joins main bucket to training dataframe
    # populates non labelled data as normal
    joined_bucket[key] = cl.add_anomalies(df, training_bucket[key])

    # take buckets into lstm training
    X_train, y_train = lstm.create_sequences(
        joined_bucket[key][["Value"]], joined_bucket[key]["Value"]
    )
    X_test, y_test = lstm.create_sequences(
        joined_bucket[key][["Value"]], joined_bucket[key]["Value"]
    )

    lstm.fit_models(X_train, y_train)
