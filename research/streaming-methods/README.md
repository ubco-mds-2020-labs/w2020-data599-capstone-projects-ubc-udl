# Streaming Methods

This folders contains various test files (non project code) for running a Python program with InfluxDB. The current plan is to move forward with an implementation with `RxPy` that queries data from InfluxDB on a rapid schedule, run anomaly detection, and writes back to InfluxDB. This implementation can likely be modified in the future but should provide an initial framework for implementing the near real-time anomaly detection system.

The files/methods currently include:

## Python programs using RxPy

Both of these scripts are taken from examples provided with the [`influxdb-client-python` package](https://github.com/influxdata/influxdb-client-python). They have been modified slightly as needed.

An instance of InfluxDB/telegraf needs to be running to use these scripts.

`RxPy` is a package allowing reactive programming with Python. The files tested include:

- `iot_sensors.py` which reads cpu data (using `psutil`) and writes to InfluxDB every 10 seconds which is scheduled by `RxPy`
    - This is a similar implementation to what telegraf does and could be a potential replacement for telegraf - reading JSON files, and processing them to go into InfluxDB (however, it may be slower that telegraf). There are also likely methods where RxPy listens for files instead of running on a timed basis but this would required additional research.
    - Alternatively, a setup could be implemented where RxPy is being used to both query data from InfluxDB, process for anomalies, and write back to InfluxDB.
    - Note that the script is currently terminated by user input, a better termination method is likely required.

- `realtime-stream.ipynb` uses `RxPy` to query the latest 10 seconds of data from InfluxDB and uses the `streamz` package to create a sink that can be read and plotted in real-time using `hvplot`.
    - I do not believe that `streamz` is required for our purposes, the purpose in this file was to allow `hvplot` to plot the streaming data.
    - It is also not entirely clear how to clear a sink created by `streamz`.
    - The main point of this script is showing how `RxPy` could be used with querying.

In general, using `RxPy` to query InfluxDB, run an anomaly detection script, and write back to InfluxDB seems like a doable process. Items that need to be figured out would be:

- How to query multiple sensors.
- How to run different anomaly detection models on different sensors.
- How/where to save anomaly detection model parameters for future use.

Using `RxPy` in place of telegraf to read the initial files prior to InfluxDB seems possible but time would need to be spent figuring out reactive programming in Python. This should only be explored if the project timeline permits. A couple of resources identified include:

- Udemy course: [Reactive Programming in Python](https://www.udemy.com/course/reactive-programming-in-python/)
- Book: [Hands-On Reactive Programming with Python](https://www.oreilly.com/library/view/hands-on-reactive-programming/9781789138726/)

## Using InfluxDB Tasks

Using InfluxDB scheduled tasks would allow InfluxDB to provide data using http POST. This could then be picked up by a program for anomaly detection that then writes back to InfluxDB.

This was tested using the the `two-telegraf` docker setup. 

- One telegraf container is reading cpu/mem data and sending it to influxDB. 
- A task was then written into InfluxDB (through logging into the visual interface). The query for the task is in `tasks-qury`. The `tasks-test.ipynb` file is just a test of the query.
- The second telegraf container is setup to listen for the task; however, I was not able to get this to work.

If this method is to be used, the following needs to be figured out:

- How to get telegraf to pick-up the task http post from InfluxDB and then have telegraf initiate a python program.
- Or, create an API that receives the InfluxDB task and runs a python program.

This method seems like a higher effort route than using `RxPy`. We've had trouble with telegraf so far and relying on telegraf to receive the http POST from InfluxDB may be difficult. It also required telegraf to run a Python program. The alternative method of setting up an API is interesting but as the group does not have experience with this, it also is a higher effort route.

## Using Telegraf to run a Python Program on Input Data

Similar to the discussion above, we are not sure about the level of effort required to get a Python program to successfully run from Telegraf. Going this route could result in a high-effort unsuccessful method (however, it should be noted that this may ultimately be the fastest method).

## Others

There may be other methods (using PySpark etc) that could work. However, given the timeline unless an obvious method is identified, additional methods are not being pursued.