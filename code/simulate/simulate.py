import numpy as np

# import pandas as pd
# import matplotlib.pyplot as plt
import os
import psutil
import time


def simulate_stream(df, cumulative=True, batch_size=10, model=None):
    """Simulated data stream form a pandas dataframe with an
    an algorithm that can be applied. The algorithm can be applied
    on the cumulative dataframe or only the new batch of data.

    Keyword arguments:
    df -- the entire dataset, pandas.DataFrame
    cumulative -- if algorithm should be applied in
        batch or cumulative, boolean (default True)
    batch_size -- batch size, int (default = 10)
    model -- algorithm to be applied to batch
        dataset, if None calculates mean of data, function (default None)

    Returns:
    output -- results from processing, dict
    """

    output = {
        "batch_num": [],
        "time_measures": [],
        "memory_measures": [],
        "model_results": [],
        "time_avg": 0,
        "memory_avg": 0,
        "model_avg": [],
    }

    counter = 0
    for i in range(batch_size, df.shape[0], batch_size):

        # Time taking
        start_t = time.perf_counter()

        # Model
        if model:
            # TODO: write code for algorithm
            pass
        else:
            temp_results = X.loc[0:i, "_value"].mean()

        # Memory and time taking
        t = time.perf_counter() - start_t
        m = psutil.Process(os.getpid()).memory_full_info().uss

        # append values
        output["batch_num"].append(counter)
        output["time_measures"].append(t)
        output["memory_measures"].append(m)
        output["model_results"].append()

        counter += 1

    # Compute average statistics
    output["time_avg"] = np.mean(output["time_measures"])  # average time in seconds
    output["memory_avg"] = np.mean(
        output["memory_measures"]
    )  # average memory usage in Byte
    output["model_avg"] = np.mean(output["model"])  # average model values

    return output
