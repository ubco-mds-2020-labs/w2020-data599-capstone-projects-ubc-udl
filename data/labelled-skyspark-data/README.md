# Labelled SkySpark Data

This folder contains the datasets from the `unlabelled-skyspark-data` folder but has data manually labelled as anomalous. The folder contains:

- `dataset_summaries.xlsx` includes a table noting various permutations on sensor labelling  
- updated csv files with the `Anomaly` column updated. Manual labelling done using the Shiny app in `/code/labeller-app/`
- `labelled_anomalies_summary` listing the labelled anomaly events with any questions/comments
- an image folder corresponding to each sensor with snapshots from the app (the summary spreadsheet provides information on the images)
- a folder `machine-labelled` containing csv files that have their data labelled by our anomaly detection method - these files were used to generate the figures in the report

**Note that the datetime column in the csv files are in UTC**

| Sensor Name                                    | Filename                         | Description                                                                                          | Image Folder          |
| ---------------------------------------------- | -------------------------------- | ---------------------------------------------------------------------------------------------------- | --------------------- |
| HW Main Meter Power                            | CEC_compiled_data_1a_updated.csv | No anomalies labelled                                                                                | 1-images              |
| HW Main Meter Power                            | CEC_compiled_data_1b_updated.csv | Anomalies visually labelled                                                                          | 1-images              |
| HW Main Meter Entering Water Temperature       | CEC_compiled_data_2a_updated.csv | No anomalies labelled                                                                                | 2-images              |
| HW Main Meter Entering Water Temperature       | CEC_compiled_data_2b_updated.csv | Anomalies visually labelled, periods in summer with distinct patterns labelled as anomalous data     | 2-images              |
| HW Main Meter Entering Water Temperature       | CEC_compiled_data_2c_updated.csv | Anomalies visually labelled, periods in summer with distinct patterns not labelled as anomalous data | 2-images              |
| HW Main Meter Flow                             | CEC_compiled_data_3a_updated.csv | No anomalies labelled                                                                                | 3-images              |
| HW Main Meter Flow                             | CEC_compiled_data_3b_updated.csv | Anomalies visually labelled                                                                          | 3-images              |
| Boiler B-1 Gas Pressure                        | CEC_compiled_data_4a_updated.csv | No anomalies labelled                                                                                | 4-images              |
| Boiler B-1 Gas Pressure                        | CEC_compiled_data_4b_updated.csv | Anomalies visually labelled, patterns in winter labelled as anomalous data                           | 4-images              |
| Boiler B-1 Gas Pressure                        | CEC_compiled_data_4c_updated.csv | Anomalies visually labelled, patterns in winter labelled not labelled as anomalous data              | 4-images              |
| Boiler B-1 Exhaust O2                          | CEC_compiled_data_5a_updated.csv | No anomalies labelled                                                                                | 5-images              |
| Boiler B-1 Exhaust O2                          | CEC_compiled_data_5b_updated.csv | Anomalies visually labelled                                                                          | 5-images              |
| Campus Energy Centre Boiler B-2 Exhaust O2     | CEC_compiled_data_6_updated.csv  | No anomalies labelled                                                                                | No Images |
| Campus Energy Centre Feeder 60L56 Real Power   | CEC_compiled_data_7_updated.csv  | No anomalies labelled                                                                                | No Images |
| Campus Energy Centre Boiler B-2 Gas Pressure   | CEC_compiled_data_8_updated.csv  | No anomalies labelled                                                                                | No Images |
| Campus Energy Centre Boiler B-1 Power          | CEC_compiled_data_9_updated.csv  | No anomalies labelled                                                                                | No Images |
| Campus Energy Centre Process System Pump Speed | CEC_compiled_data_10_updated.csv | No anomalies labelled                                                                                | No Images |