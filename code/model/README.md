# Model

This directory contains the Python files for the real-time anomaly detection framework with InfluxDB. A description of each file in the directory is provided below:

## Functions
The following files contain the functions/classes used in the model framework:

- `clean.py` 
  - contains functions for processing data from InfluxDB for model training or predictions
  - also contains function to store percentile loss threshold and standardization parameters
- `influx_interact.py`
  - contains class used to read/write with InfluxDB
- `model_predict.py`
  - contains a function used to make predictions using a previously trained and loaded model
- `model_trainer.py`
  - contains functions for training a model and saving the model and model parameters
  - contains a function for windowing data used for training and for predictions

## Scripts

The following files  are scripts that call the functions noted in the list above. These would be run on a timed basis within the model framework:

- `sensor_predict.py`
  - a script to be run as need be (short periods, eg. every 1 to 5 minutes) to read recent data from InfluxDB, make predictions and write predicted anomalies to InfluxDB
- `sensor_training.py`
  - a script to be run as need be (long periods, eg. every month) that will update the model parameters used for `sensor_predict.py` based on current data in InfluxDB for each individual sensor

**NOTE:** The anomaly detection framework was tested/implemented in notebook format [here](../test-env/) and these scripts were not used (UDL's live streaming InfluxDB instance was not available during the project timeline). As such, it is expected that these scripts may require modification if implementing the framework.

## Additional

These files provide example files of how model user values for the threshold factor and time-steps for each sensor could be stored for use in the scripts described above. If not provided, the model will use the default values for each sensor (15 steps for window size and 1 for threshold ratio).

- `threshold_ratios.json`
  - contains test sensor ratios used to flag anomalies for each sensor
  - default is 1, most likely will need to be adjusted
  - should be manually populated with sensors being used
- `time_step_sizes.json`
  - contains test sensor window sizes used
  - default should be 15, most likely will not need to be adjusted
  - should be manually populated with sensors being used


