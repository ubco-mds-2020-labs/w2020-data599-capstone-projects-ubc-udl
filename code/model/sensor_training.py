import influx_interact as ii
import clean as cl
import os
import model_trainer as mt

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
main_bucket = influxdb.make_query(building_list, measurements="READINGS")

# provides training bucket data
training_bucket = influxdb.make_query(building_list, measurement="TRAINING")

# creates a dictionary of dataframes for each sensor in main_bucket
main_bucket = cl.split_sensors(main_bucket)

# creates a dictionary of dataframes for each sensor in main_bucket
training_bucket = cl.split_sensors(training_bucket)

# create empty dictionary
normal_bucket = {}
abnormal_bucket = {}

for key, df in main_bucket.items():
    # creates standardized column for each sensor in main bucket
    main_bucket[key]["Stand_Val"] = cl.standardize_values(df[["Value"]])

    # joins main bucket to training dataframe
    # populates non labelled data as normal
    normal_bucket[key], abnormal_bucket[key] = cl.split_normal(
        cl.add_anomalies(df, training_bucket[key])
    )

    x_train, y_train = mt.create_sequences(
        normal_bucket[key][["Value"]], normal_bucket[key]["Value"]
    )

    normal_dict = cl.model_parser(normal_bucket[key], x_train, y_train)

    mt.fit_models(normal_dict, "Path to where models saved")
