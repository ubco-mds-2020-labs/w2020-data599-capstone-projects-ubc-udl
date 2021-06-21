## results

This folder contains the folder `model-evaluations` in which notebooks and images for the exploratory analysis of our LSTM-ED model are contained.  
It also contains the following notebooks which were generated after finding a decent performing default window size of 15 and a default threshold of the 99.5% percentile of the MAE loss in the training data.  
These notebooks primary function was to determine the threshold multiplicative factor which qualitatively identified the most anomalies, with little false positive identifications.  
Details for each notebook are as follows:

| Sensor Name                              | Filename                         | Threshold Multiplicative Factor | Window |
| ---------------------------------------- | -------------------------------- | ------------------------------- | ------ |
| HW Main Meter Power                      | CEC_compiled_data_1_PD_15.ipynb  | 1.4                             | 15     |
| HW Main Meter Power                      | CEC_compiled_data_1_SW_15.ipynb  | 0.6                             | 15     |
| HW Main Meter Entering Water Temperature | CEC_compiled_data_2_SW_15.ipynb  | 1.2                             | 15     |
| HW Main Meter Flow                       | CEC_compiled_data_3_SW_15.ipynb  | 1.72                            | 15     |
| Boiler B-1 Gas Pressure                  | CEC_compiled_data_4_SW_15.ipynb  | 0.23                            | 15     |
| Boiler B-1 Exhaust O2                    | CEC_compiled_data_5_SW_15.ipynb  | 1                               | 15     |
| Boiler B-1 Gas Pressure                  | CEC_compiled_data_6_SW_15.ipynb  | 0.7                             | 15     |
| Boiler B-1 Gas Pressure                  | CEC_compiled_data_7_SW_15.ipynb  | 0.4                             | 15     |
| Boiler B-1 Exhaust O2                    | CEC_compiled_data_8_SW_15.ipynb  | 0.4                             | 15     |
| Boiler B-1 Exhaust O2                    | CEC_compiled_data_9_SW_15.ipynb  | 1                               | 15     |
| Boiler B-1 Exhaust O2                    | CEC_compiled_data_10_SW_15.ipynb | 1.5                             | 15     |

CSV data used for the notebooks can be found in the `data/labelled-skyspark-data` folder with the prefix 'CEC_compiled_data_'

