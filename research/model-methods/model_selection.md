
# Model Selection

**Considering frameworks discussed in literature - what does/doesn't work for IoT systems?**

LSTM model appear to perform well on general IoT data based on a literature review. We are looking to provide a framework that could be used for multiple system/sensors so this seems like a good choice. Initial testing in `model-demo/lstm_sensor1.ipynb` and `model-demo/lstm_sensor2.ipynb` which use a limited subset of data from the EDA (manual downloads of data from SkySpark) indicate promising results. Note that there was limited project data available during this research phase.

**What does data looks like (types of data/groups of sensors and types of anomalies)?**

From the EDA we can see different anomaly types. Some sensors produce data with constant mean and variance and other sensors produce data with seasonal trends. The types of anomalies we are looking for are: point anomalies, contextual anomalies, collective anomalies, and missing data. LSTMs are general enough to detect point, contextual, and collective anomalies. Missing data will likely require a different system but should not be difficult to implement.

**How are we going going to train our model?**

We do not have labelled data. As such the LSTM provides a model that can be used in an unsupervised fashion - it can be trained using reconstruction error and can then flag data points with a low probability of occurrence.

The framework we are considering will train the the model on normal data such that it has not seen anomalous patterns and we believe this will provide better performance for anomaly detection. This does require that we manually label and remove data we consider to be anomalous for the study; however, we need to label data we are consider anomalous to evaluate performance anyways. 

When the model is online and retrains itself, it would just remove any data it has previously labelled as anomalous. This also provides a method for putting a human-in-the-loop by providing a framework where a user could label data as anomalous or normal which would or would not get included in the model training.


**Consideration of packages available.**

Refer to `comparison_of_packages.xlsx` and `model-demo/model_test.ipynb`. While there are many packages available for anomaly detection which provide machine learning or statistical algorithms we are moving forward with the LSTM model.

We will be using Keras for model development.
