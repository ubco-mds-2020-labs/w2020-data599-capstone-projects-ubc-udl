# Performance Criteria Selection

**How are we identifying anomalies in our dataset such that we can check performance measures?**

No labeled data from UDL are available, we will need to manually label any data we consider anomalous. We will consider any data that does not follow the typical patterns to be anomalous, the could include:

- sensor malfunctions
- equipment malfunctions
- operational issues (opening a valve, annual maintenance, etc)

The goal will be for the system to hopefully detect any patterns that do not appear normal. This could be very different for different types of sensors and the hope is that the model will be sufficiently general to learn each sensor.

**How are we detecting anomalies?:**

This could include anomaly scores, yes/no, classifying/identifying different types of anomalies specifically.

We will focus on whether the model detects a pattern we identified as anomalous or not (binary event based classification). Would the system provide a notification for the event or not? Note that one parameter we will be able to tune for the model is probability score from the LSTM.

**Following that, what performance measure will we use?**

The study will likely use a semi-quantitative approach to performance. Quantitative in terms of anomaly event prediction (Precision, Recall, F-score) but we will also need to look at qualitative assessment - the model may find events that we did not label as anomalous (not picked out by the human eye) but on further inspection are anomalous data. We will also need to look qualitatively at how quickly the model predicts an anomaly (how quickly would the system provide a notification into an anomalous event) and how long the model continuous to flag data as anomalous after the sensor has returned to normal conditions. These considerations will be important for a realtime prediction system.

**Are we considering injection of anomalies?**

No, our training approach is unsupervised and this is not felt to be necessary. It could be used to help evaluate model performance if there is time.
