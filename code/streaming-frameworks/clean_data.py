import pandas as pd
import numpy as np

# could potentially use other methods of standardizing
# if we don't want to use this package
from sklearn.preprocessing import StandardScaler


def add_anomalies(df1, df2):
    """
    checks current data against pre-existing anomaly labels

    df1 : single sensor pandas dataframe
    df2 : single sensor pandas dataframe w/ labels
    """

    # make sure our date column is in datetime
    # Datetime can be changed to whatever nameing
    # structure we decide on
    df1["Datetime"] = pd.to_datetime(df1["Datetime"])
    df2["Datetime"] = pd.to_datetime(df2["Datetime"])

    # join dataframes adding anomaly columns
    df1 = df1.combine_first(df2)

    # add false to all anomalies in machine column
    # that were not pre-labelled
    df1["AM"].replace(np.NaN, False, inplace=True)

    # update all machine values where there are human inputs
    cond = ~df1["AH"].isna()
    df1["AM"].loc[cond] = df1["AH"].loc[cond]

    return df1


def split_sensors(df1):
    """
    seperates dataframe into multiple dataframes
    returns list of dataframes

    df1 : single sensor pandas dataframe
    """

    # seperates single dataframe into multiples with each sensor
    # appends to list
    split_df = pd.DataFrame(df1.groupby("uniqueID"))[1]
    sensor_bucket = []

    # couldn't find a way to vectorize this process
    # dropped and renamed columns to be returned to once InfluxDB is running
    for i in range(0, len(split_df)):
        sensor_bucket.append(
            split_df[i]
            .reset_index()
            .drop(["index", "result", "table"], axis=1)
            .rename(columns={"_time": "DateTime", "_value": "Value", "uniqueID": "ID"})
        )

    return sensor_bucket


def standardize_values(col1):
    """
    checks current data against pre-existing anomaly labels

    col1 : single sensor pandas int column
    """

    # create scaler object
    scale = StandardScaler()
    # apply to pandas column
    st_col1 = scale.fit_transform(col1)

    return st_col1


def group_check(df1):
    """
    checks current data if sensor has been assigned a group

    df1 : single sensor pandas dataframe
    """
    # load in group lookup csv. Path to be changed
    group_csv = pd.read_csv("../../data/testing-data/group_lookup.csv")

    # loop through groups looking for match
    # group length is only 3 for now
    # need not vectorize
    for i in range(0, len(group_csv)):
        if df1["ID"].any() in list(group_csv.iloc[:, i]):
            group = list(group_csv.columns)[i]
            return group

    return None


def test_anomaly(df1):
    """
    checks current data if sensor has been assigned a group

    df1 : single sensor pandas dataframe
    """
    df1["AM"]
