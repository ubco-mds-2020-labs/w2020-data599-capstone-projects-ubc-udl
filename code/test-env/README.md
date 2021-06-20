# Test Environment

Copy `docker-compose.yml` located in this directory to a local directory. Then run the command `docker-compose up` from the local directory. Go to `http://localhost:8086/` and enter `MDS2021` as user name and `mypassword` to log in to the user interface.

The notebook file `test_env_demo.ipynb` provides a walk-through of using the anomaly detection framework in a test environment. Includes testing the model training (including saving model files), model predictions (including loading the model files), dashboard, and notification system.

This test environment was used as UDL's InfluxDB instance was still being setup with SkySpark data during the project. The test environment populates an instance of InfluxDB (created using Docker) with sensor data from `../../data/labelled-skyspark-data/`. The sensor data was manually downloaded from SkySpark and corresponds with five sensors used in Phase 1 model testing.

A description of the files in this directory includes:

- `cec_boiler_sensors_(test).json` - dashboard template used in the walk-through
- `docker-compose.yml` - used to create a local instance of InfluxDB
- `test_env_demo.ipynb` - walk-through notebook
- `prediction_timer_demo.ipynb` - notebook that explores the time it would take to run the prediction script and write back to influxDB on a subset of incoming data. It currently looks at a single sensor from `../../data/labelled-skyspark-data/` but can be modified easily to query multiple sensors.
- `test_env_*/` - saved model files from the walk-through
