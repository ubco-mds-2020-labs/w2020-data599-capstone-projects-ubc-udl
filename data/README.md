# Data

This folder contains data used in model development.

## unlabelled-skyspark-data

This folder consists of the data manually downloaded from the EWS SkySpark interface. The data were downloaded in multiple chunks and joined together to create a single file for each sensor.

## labelled-skyspark-data

This folder contains the datasets from the `unlabelled-skspark-data` folder but has data manually labelled as anomalous for input to modelling. The folder contains:

- a summary spreadsheet with a table noting various permutations on sensor labelling  
- the updated csv files with the `Anomaly` column updated. Manual labelling done using the Shiny app in `/code/labeller-app/`
- a summary spreadsheet listing the labelled anomaly events with any questions/comments
- an image folder corresponding to each sensor with snapshots from the app (the summary spreadsheet provides information on the images)


## testing-data

This folder contains data that has been manually altered to replicate a set of a data from an original sensor:
- training_bucket.csv: an example of data that would exist in InfluxDB's training bucket
- main_bucket.csv: an example of data that would exist in InfluxDB's main bucket