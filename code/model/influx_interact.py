"""query/write from InfluxDB function"""

import datetime
from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS

# import pytz


class influx_class:
    """
    Class for querying/writing to InfluxDB. Includes creating client and holding tokens.
    """

    def __init__(self, org, url, bucket, token):
        """
        Initialize class with credentials and query location.

        Keyword arguments:
        org -- InfluxDB org, string
        url -- URL to query , string (example: "http://localhost:8086//")
        bucket -- InfluxDB bucket name to query from, string
        token -- token to use for query, string

        Returns:
        None
        """
        self.org = org
        self.url = url
        self.bucket = bucket
        self.token = token
        self.client = InfluxDBClient(url=url, token=token, org=org)

    def make_query(
        self,
        location,
        id=None,
        measurement="READINGS",
        field="val_num",
        start=None,
        end=None,
        window=None,
        fill=False,
    ):
        """
        Make a query to InfluxDB

        Keyword arguments:
        location -- building to query, string (example: "Campus Energy Centre")
        id -- ID of sensor to query, list of strings
            (example: ["p:ubcv:r:205b0392-31f31280"])
        measurements: measurement type to query, strings (default = "READINGS")
        field -- field to query, string (default = "val_num")
        start -- flux query language start, string (default = None)
            if default is used, the start of available data is queried
        end -- flux query language end, string (default = None)
            if default is used, the end of available data is queried
        window -- window to use for averaging data in minutes, int (default = None)
            if default is used, no windows are applied and all available
            data are returned
        fill -- if window is used, add na to windows w/out data, boolean
            (default = False)

        Returns:
        result -- result of query, Pandas DataFrame
        """

        # convert start, end, windowing input for query
        # TODO: potentially build out date parsing/user input checks
        if start:
            use_start = start
        else:
            use_start = 0
        if end:
            use_end = end
        else:
            use_end = datetime.datetime.now()
        if window:
            use_window = datetime.timedelta(minutes=window)
        else:
            use_window = None

        # parameters to be used in query
        p = {
            "_bucket": self.bucket,
            "_measurement": measurement,
            "_start": use_start,
            "_end": use_end,
            "_location": location,
            "_field": field,
            "_every": use_window,
            "_fill": fill,
        }

        query = """from(bucket: _bucket)
            |> range(start: _start, stop: _end)
            |> filter(fn: (r) => r["_measurement"] == _measurement)
            |> filter(fn: (r) => r["siteRef"] == _location)
            |> filter(fn: (r) => r["_field"] == _field)"""

        # adds multiple ids
        if id is not None:
            for i in range(0, len(id)):
                p["_id" + str(i)] = id[i]

            query += """|> filter (fn: (r) => r["uniqueID"] == _id0"""

            # filter on multiple ids
            for i in range(1, len(id)):
                query += """ or r["uniqueID"] == _id""" + str(i)
            query += """)"""

        if window:
            query += (
                """|> aggregateWindow(every: _every, fn: mean, createEmpty: _fill)"""
            )

        query += (
            """|> drop(columns: ["_start", "_stop", "_measurement","""
            """ "_field", "typeRef", "equipRef", "siteRef", "groupRef"])"""
        )

        # Instantiate the query client. Specify org and query.
        result = self.client.query_api().query_data_frame(
            org=self.org, query=query, params=p
        )

        return result

    def write_data(self, df, measurement, tags):
        """
        Write to InfluxDB

        Keyword arguments:
        df: data to write to InfluxDB, Pandas DataFrame
        measurement: group name, string (ie. CHECK_ANOMALY, TRAINING)

        Returns:
        None
        """

        self.client.write_api(write_options=SYNCHRONOUS).write(
            self.bucket,
            self.org,
            record=df,
            data_frame_measurement_name=measurement,
            data_frame_tag_columns=tags,
        )
