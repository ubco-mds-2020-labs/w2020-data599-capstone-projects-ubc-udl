This folder contains the python script files needed to create realtime anomaly detection off of an InfluxDB database.

A description of each file is as follows:

- `clean.py` 
  - contains functions for processing data coming/going to an InfluxDB.
  - also contains function to store percentile loss threshold and standardization parameters for model to use.
- `influx_interact.py`
  - contains class used to read/write to InfluxDB.
- `model_predict.py`
  - contains a function used to make predictions based of loaded model.
- `model_trainer.py`
  - contains functions for training a model and saving it's parameters.
  - contains a function for windowing data used for training and for predictions.
- `sensor_predict.py`
  - a script to be run as need be (short periods, eg. every 5 minutes) to write predicted anomalies to InfluxDB on any new data.
- `sensor_training.py`
  - a script to be run as need be (long periods, eg. every month) that will update the model parameters used for `sensor_predict.py` based on current data in InfluxDB for each individual sensor.
- `threshold_ratios.json`
  - contains test sensor ratios used to flag anomalies for each sensor.
  - default should be 1, most likely will need to be adjusted.
  - should be manually populated with sensors being used.
- `time_step_sizes.json`
  - contains test sensor window sizes used.
  - default should be 15, most likely will not need to be adjusted.
  - should be manually populated with sensors being used.


Since this was developed with no access to a realtime InfluxDB, modification may need to be made to `sensor_predict.py` and `sensor_training.py` upon implementation.