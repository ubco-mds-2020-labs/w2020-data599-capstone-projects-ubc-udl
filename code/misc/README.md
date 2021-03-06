# misc

This folder currently contains miscellaneous files created during development. These have been left in the repository as they may provide useful information for future development. Note that they are not directly useable/updated with the latest model, but just provide guidance.

- `predict_before_run.py` - Script that would be run by telegraf with the execd plug-in using the functions in `predict_telegraf_func.py`. This was tested with a Docker environment and Telegraf was able to run the script.
- `predict_telegraf_func.py` - Contains functions that would be used by a predictor inline with telegraf prior to writing. This was just completed to test the ability of the execd plug-in in Telegraf.
- `influxdb_query_test.ipynb` - Used to support understanding of InfluxDB including testing queries and writes.
- `model_server.py` and `example_predictor.py` - Contains code that could be used to setup a flask server for model predictions. This was completed early in the project and has out of date code but may be useful as an example if using flask for predictions is pursued in the future.

