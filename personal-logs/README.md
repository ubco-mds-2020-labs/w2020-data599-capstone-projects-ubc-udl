# Personal Logs

Each team member folder contains an Excel file with daily logs grouped by project week.

## Team Progress

A brief description of tasks completed in each week is provided below. The tables provide the general tasks that were completed and list individual contributions.

**Week 1: Project Definition and Proposal**

The first project week consisted of:

- Select/Define Project
- Create Project Management Tools
- Write Project Proposal
- Background Data Review

All team-members contributed to the above tasks.

**Week 2: Data and Systems Understanding**

Goals for the second project week included:

- Select Project Data and Complete EDA (still in progress at the end of Week 2)
- Understand Data Systems
- Learn InfluxDB and Telegraf
- Simulate Streaming in InfluxDB
- Anomaly Detection Research

Additionally, a Telegraf parser was worked on allowing streaming data directly into InfluxDB.

| Nate | Mitch | Ryan | All |
| --- | --- | --- | --- |
| Learn InfluxDB and Telegraf, Simulate Streaming in InfluxDB, Investigate Streaming Detection Frameworks, Project Management | Anomaly Detection Research | Learn InfluxDB and Telegraf, EDA, XML Parser | Get a Local Setup of InfluxDB and Telegraf Working in Docker, Work on Streaming Data Parser |

**Week 3: Anomaly Detection Model**

Goals for the third project week included:

- Complete EDA from Week 2
- Data Cleaning/Feature Processing
- Build Streaming Framework for Anomaly Detection Model
- Meet with Domain Experts
- Start Reviewing Azure (secondary goal)

Helping implement the Telegraf parser to support getting streaming data into InfluxDB was also worked on.

| Nate | Mitch | Ryan | All |
| --- | --- | --- | --- |
| Build Streaming Framework and Test Locally, Project Management, Build Anomaly Labeller App, Manually Label Anomalies | Ongoing Anomaly Detection Research, Start Building LSTM | Ongoing EDA, Help with Anomaly Detection Research, Support Telegraf Parsing, Manually Label Anomalies | Meet with Domain Experts |

**Notes:** 

- Felt that additional time was required on anomaly detection research before building the model. Accordingly, building the model was moved to Week 4.
- Also, with the ongoing EDA this week data cleaning will was largely moved to Week 4.
- An additional item not included in the schedule was research of good anomaly detection performance measures, this will be completed early next week.
- Also needed to manually download data and self-label what we consider to be anomalies in the datasets. Five sensors were downloaded and labelled (2 of which required comments from EWS).

**Week 4: Anomaly Detection Model Continued**

The original proposal goal for the fourth project week was implementing the anomaly detection model. However, as discussed above for Week 3, several tasks were behind the proposal schedule. Therefore, the goals for this week were to complete the anomaly detection model and evaluate the labelled datasets from the previous week.

- Mid-Project Status Presentation
- Complete Anomaly Detection Model Pipeline (including understanding various LSTM architectures)
- Evaluate Downloaded Datasets

The five sensors downloaded were evaluated using the various labelling permutations discussed in `/data/labelled-skyspark-data`. It was discussed that additional self-labelling would not be completed as it is very time intensive. Instead, assessment using the five sensors would be completed and additional assessment would just be completed on unlabelled data.

An additional task looked at was research on using a Spectral Residual transformation on the data as a step before the LSTM model.

| Nate | Mitch | Ryan | All |
| --- | --- | --- | --- |
| Project Status Report, Spectral Residual Research, Support on Model Pipeline, Research LSTM architectures | LSTM Model | Cleaning Pipeline | Model Evaluation |