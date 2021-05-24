# Simulate Folder

Small package that can be used to facilitate offline streaming tests without using InfluxDB/Telegraf. Currently incomplete and will be built out as/if required.

Folder currently includes:

- `simulate.py` - code framework, batch aggregating or non-aggregating simulated streaming from a Pandas DataFrame
- `simulate_stream_test.ipynb` - testing `simulate.py` using data queried from InfluxDB
- `simpy_test.ipynb` - demo file of the SimPy package in the event a more detailed simulation environment was required (unlikely)
