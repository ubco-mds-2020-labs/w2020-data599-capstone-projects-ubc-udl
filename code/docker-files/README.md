# Docker Files

This folder contains docker files that can be used to setup local InfluxDB and telegraf containers.

- `one-telegraf` provides a setup with one instance of telegraf running and reading/streaming cpu and memory data into InfluxDB
- `two-telegraf` provides a setup with two instances of telegraf running with the first instance reading/streaming cpu and memory data into InfluxDB and the second instance listening for tasks sent from influxdb (currently not successfully)