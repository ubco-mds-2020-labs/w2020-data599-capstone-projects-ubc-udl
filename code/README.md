# Code

The current folders include:

- `docker-files` includes docker setups used to run InfluxDB/Telegraf locally
- `labeller-app` is a Shiny App that can be used to visualize sensor data, graphically select point, and update labelling of the data as normal or anomalous
    - this was built to support manual labelling of anomalous data
    - additional details are available in the brief README in the folder
- `notebook-demo` provides various jupyter notebook files used to support understanding InfluxDB (test queries/writes) and testing offline streaming simulation methods.
- `simulate` is a small package that can be used to facilitate offline streaming tests without using InfluxDB/Telegraf
    - Currently incomplete, will be built out as required to support work
- `streaming-frameworks` is the package that will be used to for reading/writing data from InfluxDB
    - In progress
- `streaming-methods` includes various tests on streaming methods that could be used with InfluxDB