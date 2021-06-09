# Test Environment Creation Steps

`Requirements.txt` provides the list of Python packages required to use the test environment.
## Step 1

Copy `docker-compose.yml` located in this directory to a local directory. Then run the command `docker-compose up` from this local directory. It is recommended to increase the ram available to docker from the default of 2gb to 5gb.

Go to `http://localhost:8086/` and enter `MDS2021` as user name and `mypassword` to log in. You will need to create the `MDS2021` bucket if it is not already created.

## Step 2

Navigate back to this directory and run `populate_influx.py`. This will populate InfluxDB with csv files located in `../../data/labelled-skyspark-data/`. These files correspond with the Phase 1 model testing.

N.B `populate_influx.py` times out regardless of the `timeout` parameter in the influx client call, solution is to rerun this file until it completes

## Step 3

Run `test_env_scheduled_trainer.py`. This will provide anomaly detection model training and will save model files for each data set in `test_env_models\` and `test_env_standardizers`. A cron job can be used on this script to simulate model retraining. The script will also write the training results to InfluxDB in the TRAINING_ANOMALY Measurement.

## Step 4

Run `test_env_scheduled_trainer.py`. This will provide anomaly detection predictions. It loads the model files saved in Step 4. A wait can be included in the prediction loop to simulate waiting a given time period between predictions. Predictions will be written to InfluxDB in the PREDICT_ANOMALY Measurement.
