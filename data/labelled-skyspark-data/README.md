# Labelled SkySpark Data

This folder contains the datasets from the `unlabelled-skspark-data` folder but has data manually labelled as anomalous. The folder contains:

- the updated csv files with the `Anomaly` column updated. Manual labelling done using the Shiny app in `/code/labeller-app/`
- a summary spreadsheet listing the labelled anomaly events with any questions/comments
- an image folder corresponding to each sensor with snapshots from the app (the summary spreadsheet provides information on the images)
- note that the datatime column in the files are in UTC

| **Sensor Name**                                               | **File Name**           | **Image Folder**      |
| :------------------------------------------------------------ | :---------------------- | :------------------ |
| Campus Energy Centre Campus HW Main Meter Power               | CEC_compiled_data_1.csv_updated.csv | 1-images |
| Campus Energy Centre HW Main Meter Entering Water Temperature | CEC_compiled_data_2.csv_updated.csv | 2-images |
| Campus Energy Centre Campus HW Main Meter Flow                | CEC_compiled_data_3.csv_updated.csv | 3-images |
| Campus Energy Centre Boiler B-1 Gas Pressure                  | CEC_compiled_data_4.csv_updated.csv | 4-images |
| Campus Energy Centre Boiler B-1 Exhaust O2                    | CEC_compiled_data_5.csv_updated.csv | 5-images |