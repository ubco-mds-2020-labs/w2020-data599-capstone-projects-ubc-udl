# Unlabelled SkySpark Data

This folder consists of data manually downloaded from the EWS SkySpark Database. This was done to support model development as there is currently not an easy way to access data.

The data were downloaded in CSV format 10,000 data points at a time and then merged into single csv files for each sensor. The data was modified as follows:

- units were removed from the values (for example data was in the format 32MW, this was changed to be 32)
- an `ID` column was added with the name of the sensor
- an `Anomaly` column was added (True/False) and was populated with `False`

**Notes:**

- the sensors have different recording intervals
- sensors 1-5 were used in Phase 1 testing and sensors 6-10 were used in Phase 2 testing as discussed in the final report

| **Sensor Name**                                               | **File Name**            | **Date Range**      |
| :------------------------------------------------------------ | :----------------------- | :------------------ |
| Campus Energy Centre Campus HW Main Meter Power               | CEC_compiled_data_1.csv  | Jan 2020 - May 2021 |
| Campus Energy Centre HW Main Meter Entering Water Temperature | CEC_compiled_data_2.csv  | Nov 2016 - May 2021 |
| Campus Energy Centre Campus HW Main Meter Flow                | CEC_compiled_data_3.csv  | Jan 2020 - May 2021 |
| Campus Energy Centre Boiler B-1 Gas Pressure                  | CEC_compiled_data_4.csv  | Jan 2020 - May 2021 |
| Campus Energy Centre Boiler B-1 Exhaust O2                    | CEC_compiled_data_5.csv  | Jan 2020 - May 2021 |
| Campus Energy Centre Boiler B-2 Exhaust O2                    | CEC_compiled_data_6.csv  | Jan 2020 - May 2021 |
| Campus Energy Centre Feeder 60L56 Real Power                  | CEC_compiled_data_7.csv  | Nov 2016 - May 2021 |
| Campus Energy Centre Boiler B-2 Gas Pressure                  | CEC_compiled_data_8.csv  | Jan 2020 - May 2021 |
| Campus Energy Centre Boiler B-1 Power                         | CEC_compiled_data_9.csv  | Jan 2020 - May 2021 |
| Campus Energy Centre Process System Pump Speed                | CEC_compiled_data_10.csv | Jan 2020 - May 2021 |