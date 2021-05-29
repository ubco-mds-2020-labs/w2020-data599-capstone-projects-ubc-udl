# Spectral Residual

Testing spectral residual transformations on the manually labelled [datasets](../../data/labelled-skyspark-data) to assess if the transformation could be useful in anomaly identification.

The notebook `SR-explore.ipynb` provides the exploration and the .csv files in this folder provide datasets that are standardized and then have a spectral residual algorithm applied.

Note that the idea came from Microsoft's use of spectral residual in their [SR-CNN](https://techcommunity.microsoft.com/t5/ai-customer-engineering-team/overview-of-sr-cnn-algorithm-in-azure-anomaly-detector/ba-p/982798) anomaly detection algorithm. The paper on SR-CNN can be found [here](https://arxiv.org/abs/1906.03821).

The `images\` folder contains various images referenced in the notebook file.

Overall, it is recommended to try the SR transformation with the LSTM as it looks like it could help highlight anomalies; however, as also discussed in the notebook, there are types of anomalous data that the transformation could make harder to detect.
