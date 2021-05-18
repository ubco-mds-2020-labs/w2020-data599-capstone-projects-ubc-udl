# Code

The current folders include:

- `docker-files` includes docker setups used to run InfluxDB/Telegraf locally
- `notebook-demo` provides various jupyter notebook files used to support understanding InfluxDB (test queries/writes) and testing offline streaming simulation methods.
- `simulate` is a small package that can be used to facilitate offline streaming tests without using InfluxDB/Telegraf
    - Currently incomplete, will be built out as required to support work
- `streaming-frameworks` is the package that will be used to for reading/writing data from InfluxDB
    - In progress
- `streaming-methods` includes various tests on streaming methods that could be used with InfluxDB