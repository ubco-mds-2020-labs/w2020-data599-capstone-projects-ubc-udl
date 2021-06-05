# Test Envrionment Creation Steps

## Step 1

Navigate to your influx docker compose (This was setup and tested using `docker-files/one-telegraf/`) Then run `docker-compose up`  

## Step 1.1

Go to `http://localhost:8086/` and enter `MDS2021` as user name and `mypassword` to log in, you will need to create the `MDS2021` bucket

## Step 2

Run `populate_influx.py` to put csvs from the data directory into the influx running in docker from step 1. This python file is currently set up to upload only two csvs and it can easily be edited to upload more.

## Step 3

Run `test_env_scheduled_trainer.py` to create and save models as well as standard scalers for each data set. Can be put on a cron for simulated re training

## Step 4

Run `test_env_scheduled_predictor.py` to create simulated real time predictions. A wait can be included in the prediction loop to simulate waiting a given time period between predictions