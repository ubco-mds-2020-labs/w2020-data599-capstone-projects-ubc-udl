# Docker Files

This folder contains docker setups that can be used to run local InfluxDB and Telegraf containers. These are used to test various InfluxDB/Telegraf setups.

The command `docker-compose up` can be used within each of the following folders to run the containers. Running `docker-compose down` will remove the containers.

A description of the various test environments are provided below:

- `one-telegraf`
    - provides a setup with one instance of Telegraf running and reading/streaming example EWS xml data into InfluxDB
    - used to test the xml parser that will be used to read streaming data to InfluxDB
- `two-telegraf`
    - provides a setup with two instances of Telegraf running with the first instance reading/streaming cpu and memory data into InfluxDB and the second instance listening for tasks sent from Influxdb (currently not successfully)
    - used as a test setup to see if Telegraf can listen to tasks from InfluxDB
- `incl-python`
    - same setup as `one-telegraf` but runs the streaming data through the execd processor with a python script
    - includes a new docker container `natewray/telegraf-python:1.18.2` which installs python allowing python scripts to be run from the Telegraf execd plug-in

`telegraf-python.docker` is not required to run the above setups but provides the file used to create the derivative `natewray/telegraf-python:1.18.2` container which is a copy of the `telegraf:1.18.2` container but with python installed. This container is hosted directly on docker hub [here](https://hub.docker.com/repository/docker/natewray/telegraf-python) but can also be built using the command `docker build -t natewray/telegraf-python:1.18.2 - < telegraf-python.docker`.