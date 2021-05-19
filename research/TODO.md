# Anomaly Detection Model To Do

## Anomaly Detection Methodology

**Hopefully we can have this done by Friday morning to support the meeting (worst case EOD Friday)**

Come up with a method that makes sense given data we're looking at considering the different types of data and the types of anomalies. This should be selected based on:

- Considering frameworks discussed in literature - what does/doesn't work for IoT systems. We need to have a literature review that we can cite as part of this for our report and it makes sense to use a framework that makes sense.
- What our data looks like (types of data/groups of sensors and types of anomalies).
- How we're going to train our model.
- Consideration of packages available.

We should be able to answer these questions clearly (and we'll need to in our report). We're going to run into trouble if we just 'try' things and hope something shakes out.

## Performance Measures

**Should have this done no later than Monday EOD to support Tuesday meeting**

Select what we're going to use for performance measures. This includes:

- How are we identifying anomalies in our dataset such that we can check performance measures.
- How are we detecting anomalies: anomaly scores, yes/no, are we also classifying/identifying different types of anomalies specifically.
- Following that, what performance measure will we use.
- Consideration of how we're training/testing our model: are we using a hold-out period and is it random selection based or a time based selection, or are we using hold-out sensors.
- Are we considering injection of anomalies.

Similar to the above, section we need to be able to answer these clearly and cite literature for examples - why we selected what we selected.

## Put Together Model

**Need to be coding the model frameowkr no later than Monday morning, need to be testing with performance measures no later than Wed morning**

Without answers to the above, we can't really build a model appropriately and we're risking going down a path that is doesn't lead anywhere. We maybe want to be able to have 2 potential detection frameworks that we're trying for example:

- Specific framework where we look to use specific algorithms targeting different types of anomalies
- More general framework to see if that's successful

Within each of the above frameworks we'll be looking at several algorithms. Ultimately we'll select one of the frameworks and set of algorithms (or maybe end up blending them together). Without anomalies identified, performance measures selected, and the train/test sets split out we won't be able to test the frameworks.

