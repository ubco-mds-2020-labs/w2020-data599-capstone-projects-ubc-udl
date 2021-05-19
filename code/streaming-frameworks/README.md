# Streaming Frameworks

This folder currently contains the following in-progress (currently on hold) code:

- `influx_interact.py` - contains a class used to query data from and write data to InfluxDB
- `predict_after_run.py` - script that would be run by telegraf using the input exec plug-in using the class in `influx_interact.py` to query/write
    - includes a call to `predict_anomaly_df()` which currently doesn't exist and would be contained in `train_predict.py`
    - has not been tested with the telegraf exec plug-in
- telegraf_inline.py - contains functions that would be used by a predictor inline with telegraf prior to writing data to InfluxDB
    - issues with this currently are that it only looks at a single line so moving windows operations could be an issue if required for prediction
    - the `predict_anomaly_line()` is currently a placeholder function
- predict_before_run.py - script that would be run by telegraf with the execd plug-in using the functions in `telegraf_inline.py`
    - this was tested with Telegraf and was successful but checks still need to be completed to confirm that all data is reporting to InfluxDB (there is no data being dropped)