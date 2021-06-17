# Code

The Python environment used for project development can be installed using anaconda or miniconda with the following command from this directory:

`conda env create -f environment.yml`

This will create the `anomaly` environment which can then be activated using:

`conda activate anomaly`

The environment uses Python 3.7 and has influxdb-client, jupyterlab, pandas, scikit-learn, and tensorflow.

Alternatively, the required packages are located in `requirements.txt`.

**NOTE: should delete `simulate` and `streaming-framework` directories when we're sure we don't need anything from them anymore**
## docker-files

Includes docker setups used to run InfluxDB/Telegraf locally. Also provides a docker file that can be used to modify a telegraf image to include Python installed in the container.

## labeller-app

Shiny App that can be used to visualize sensor data and graphically select and update labelling of the data as normal or anomalous. This was built to support manual labelling of anomalous data (used in Phase 1 Testing). Additional details and a demo are available in the folder README. This app may be useful for future use to visualize data.

## misc-notebooks

Currently only contains `influxdb_query_test.ipynb` used to support understanding of InfluxDB including testing queries and writes.
## model

Provides code for the model training and anomaly predictions with the anomaly detection framework.

<p align="center">
  <img src="../images/framework.png" alt="Anomaly Detection Framework" width="450"/>
</p>

The model pipeline implemented is shown below (details are provided in the final report).

<p align="center">
  <img src="../images/LSTM_pipeline.png" alt="LSTM Pipeline" width="600"/>
</p>

The directory contains a README that provides a description of  the files.

**TODO - update and clean-up package and provide description of files in the code folder README**

## results

Model testing of the LSTM-ED in notebook format. This corresponds with the Phase 1 and Phase 2 testing discussing in the final report.

**TODO - provide a good README in the folder (the sequence reconstruction vs next point prediction figure from the report is available as images/LSTM_type if it's needed)**

## test-env
 
Provides a detailed jupyter notebook walk-through of the anomaly detection framework in a test InfluxDB environment. Includes testing the model training (including saving model files), model predictions (including loading the model files), dashboard, and notification system.

**TODO - still a work in progress**
