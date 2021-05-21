
# Model Frame work

## Questions

1. Considering frameworks discussed in literature - what does/doesn't work for IoT systems. We need to have a literature review that we can cite as part of this for our report and it makes sense to use a framework that makes sense.
2. What our data looks like (types of data/groups of sensors and types of anomalies).
3. How we're going to train our model.
4. Consideration of packages available.

## Answers

1. LSTM models have been researched to be the best general model.

2. From the EDA we can see different anomaly types. Some sensors produce data with constant mean and variance and other sensors produce data with seasonal trends. The types of anamalies we are looking for are: point anomalies, contextual anomalies, collective anomalies, and missing data. LSTMs are general enough to detect point, contextual, and collective anomalies. Missing data will require a different system.

3. We are going to train the model at scheduled intervals in an offline fashion, and the relevent pipelines will be passed their models for inline prediction.

4. Refer to `comperison_of_packages.xlsx` and `research/notebook-demo/package_demo.ipynb`

# Performance Measures

## Questions

1. How are we identifying anomalies in our dataset such that we can check performance measures.
2. How are we detecting anomalies: anomaly scores, yes/no, are we also classifying/identifying different types of anomalies specifically.
3. Following that, what performance measure will we use.
4. Consideration of how we're training/testing our model: are we using a hold-out period and is it random selection based or a time based selection, or are we using hold-out sensors.
5. Are we considering injection of anomalies.

## Answers

1. No labeled data from UDL, the data would be manually labeled.
2. Two methodologies, the model would return either binary labels or an anomaly score. The anomaly score gives more flexibility for manual threshold setting. The LSTM system that has been chosen has a thresholding value that can automatically or manually set.
3. To be determined
4. To be determined
5. To be determined
