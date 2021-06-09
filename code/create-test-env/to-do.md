# Test Environment To-Do List

Note that many of the items in the list below are written based on the notebook, but many apply to `test_env_scheduled_predictor.py` and `test_env_scheduled_trainer.py` as well. Recommend fixing the notebook and then going through these two scripts at the end and updated. `README.md` also will likely need to be updated at the end.

## General:

- Should include a requirements.txt file
- Recommend changing the following files names in this directory to line up with our code directory as closely as possible:
    - `test_env_scheduled_predictor.py` to `test_env_sensor_predict.py`
    - `test_env_scheduled_trainer.py` to `test_env_sensor_train.py`
    - Confirm the ram requirement issue in docker noted in `README.md`
    - Resolve timeout issue noted in `README.md`

## Step 2:

- Question: is navName required in `populate_influx.py`?
- Add screenshot of InfluxDB at end of Step 2 in notebook

## Step 3:

- Update the threshold section of the notebook based on the model - likely provide brief description
- Need to explain what the END_TIME setting means - ie time does this relate to as the value doesn't appear to be a normal time?
- Need to update the notebook/scripts such that MODEL_TRAINING is pre-populated with the manual_anomaly field in the TRAINING_ANOMALY measurement for "Campus Energy Centre Campus HW Main Meter Entering Water Temperature". This will allow us to run the code as it would be run. Will probably have a description in Step 2 in the populate InfluxDB section and then no need in Step 3 to have this stuff. This may also require updates in terms of how functions work based on what we're doing with the model and then will also require updates in the test env code but I think will make it much better and closer to what should exist in `../code/sensor_training.py`.
- We also need to update all of the code files to be inline with how our model works based on the last week. This includes ensuring that Keras defaults to a GPU if it's available.
- Update variable names - `main_bucket` in Step 3 doesn't really make sense - I also don't follow the `main_bucket` description in the notebook
- Add screenshot(s) to end of Step 3
- Add code that provides a list of the save model files to show that it worked.

## Step 4:

- similar to Step 3, need to provide some comments on the Start/End time formats and what it means.
- there's some code related to data reshaping/renaming that should potentially be built directly into the functions?

## Steps 5, 6, 7

Related to the dashboard and notification system. Comments put directly in the notebook.
