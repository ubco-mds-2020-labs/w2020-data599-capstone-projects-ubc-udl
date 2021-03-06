## results

This folder contains the notebooks used to examine the LSTM-ED model with slight variations on the five test sensor data. Each was evaluated at several different thresholds determined by multiplying the max loss error (MAE loss for sequence reconstruction) by a constant.  
Details for the notebooks are as follows:

| Sensor Name                              | Filename                     | Description                                                                 | Image Folder     |
| ---------------------------------------- | ---------------------------- | --------------------------------------------------------------------------- | ---------------- |
| HW Main Meter Power                      | CEC_compiled_data_1_PD.ipynb | Evaluated predict next point for 15, 30, 60, and 120 point windows.         | images/dataset-1 |
| HW Main Meter Power                      | CEC_compiled_data_1_SW.ipynb | Evaluated sequence reconstruction for 15, 30, 60, and 120 point windows.    | images/dataset-1 |
| HW Main Meter Entering Water Temperature | CEC_compiled_data_2_PD.ipynb | Evaluated predict next point for 15 point window.                           | images/dataset-2 |
| HW Main Meter Entering Water Temperature | CEC_compiled_data_2_SW.ipynb | AEvaluated sequence reconstruction for 15, 30, 60, and 120 point windows.   | images/dataset-2 |
| HW Main Meter Flow                       | CEC_compiled_data_3_PD.ipynb | Evaluated predict next point for 15, 30, 60, and 120 point windows.         | images/dataset-3 |
| HW Main Meter Flow                       | CEC_compiled_data_3_SW.ipynb | Evaluated sequence reconstruction for 15, 60, and 120 point windows.        | images/dataset-3 |
| Boiler B-1 Gas Pressure                  | CEC_compiled_data_4_PD.ipynb | Evaluated predict next point for 15, 30, 60, and 120 point windows.         | images/dataset-4 |
| Boiler B-1 Gas Pressure                  | CEC_compiled_data_4_SW.ipynb | Evaluated sequence reconstruction for 4, 15, 30, 60, and 120 point windows. | images/dataset-4 |
| Boiler B-1 Exhaust O2                    | CEC_compiled_data_5_PD.ipynb | Evaluated predict next point for 4, 8, and 48 point windows.                | images/dataset-5 |
| Boiler B-1 Exhaust O2                    | CEC_compiled_data_5_SW.ipynb | Evaluated sequence reconstruction for 4, 8, and 48 point windows.           | images/dataset-5 |

Data used for the notebooks can be found in the `data/labelled-skyspark-data` folder with the prefix 'CEC_compiled_data_'

Images for the corresponding investigation can be found in the respective image folders.
Image naming structure follows format of data, modelling method, window size, and threshold.   
**For example:** `data_2a_PD_ts_15_thresh_5_a.png` is evaluating the `CEC_compiled_data_2a_updated.csv` with predict next point modelling method with window size of 15 points and a threshold of 5% of the maximum training error.

The `initial_results_testing.xlsx` contains a summerized collection of the testing performed using these notebooks.