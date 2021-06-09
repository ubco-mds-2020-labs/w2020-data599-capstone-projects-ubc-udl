# Code

The current folders include:

- `create-test-env` provides an implementation of the model framework in a test environment as an example
- `docker-files` includes docker setups used to run InfluxDB/Telegraf locally
- `labeller-app` is a Shiny App that can be used to visualize sensor data, graphically select point, and update labelling of the data as normal or anomalous
    - this was built to support manual labelling of anomalous data
    - additional details are available in the brief README in the folder
- `model` provides code for the anomaly detection framework
- `notebook-demo` provides various jupyter notebooks, currently includes:
    - `influxdb_query_test.ipynb` used to support understanding of InfluxDB including testing queries and writes
- `results` provides model testing in notebook format
- `simulate` is a small package that can be used to facilitate offline streaming tests without using InfluxDB/Telegraf
    - Currently incomplete, will be built out as required to support work
- `streaming-frameworks` is the package that will be used to for reading/writing data from InfluxDB
    - In progress

