"""
loads csvs into influx to create a test environment
"""
import time

import pandas as pd

from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS

PATH_TO_CSVS = "../../data/labelled-skyspark-data/"
CSVS_TO_LOAD = [
    "CEC_compiled_data_1b_updated.csv",
    "CEC_compiled_data_5b_updated.csv",
]

if __name__ == "__main__":

    start = time.time()

    # as set up in the docker-compose
    token = "mytoken"
    org = "UBC"
    bucket = "MDS2021"

    # set up influx
    client = InfluxDBClient(url="http://localhost:8086", token=token, timeout=30_000)
    write_api = client.write_api(write_options=SYNCHRONOUS)

    for csv in CSVS_TO_LOAD:

        # load and set up dataframes
        df = pd.read_csv(PATH_TO_CSVS + csv, parse_dates=["Datetime"])
        df.rename(columns={"Value": "val_num"}, inplace=True)
        df.rename(columns={"ID": "uniqueID"}, inplace=True)
        df.rename(columns={"Anomaly": "AH"}, inplace=True)
        df["navName"] = "Energy"
        df["siteRef"] = "Campus Energy Centre"
        df.set_index("Datetime", drop=True, inplace=True)

        # save anomalies for writing later
        anomalies = df["AH"]
        df = df.drop(["AH"], axis=1)

        # write values
        write_api.write(
            bucket,
            org,
            record=df,
            data_frame_measurement_name="numeric",
            data_frame_tag_columns=["uniqueID", "navName", "siteRef"],
        )

        # TODO write human anomalies - AH

    print("time taken to write to influx: {}".format(time.time() - start))
