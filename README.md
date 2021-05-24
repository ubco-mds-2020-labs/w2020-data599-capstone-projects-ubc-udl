# Data 599 Capstone - Realtime Anomaly Detection with Smart Building Data

This README will be built-out during the project (note that the file structure listed below may not be up to date with the latest folders). There are also READMEs located within each of the folders for additional descriptions.
## File Structure

- [code](code/) - project code used to build the anomaly detection model as well as various tools
    - [docker-files](code/docker-files/) includes docker setups used to run InfluxDB/Telegraf locally
    - [labeller-app](code/labeller-app/) is a Shiny App that can be used to visualize sensor data, graphically select point, and update labelling of the data as normal or anomalous
    - [notebook-demo](code/notebook-demo/) provides various jupyter notebooks
    - [simulate](code/simulate/) is a small package that can be used to facilitate offline streaming tests without using InfluxDB/Telegraf (incomplete and will be built-out as required)
    - [streaming-frameworks](code/streaming-frameworks/) is the package that will be used to for reading/writing data from InfluxDB (in-progress)
- [data](data/) - data used in model development
    - [unlabelled-skyspark-data] - sensor data manually downloaded from SkySpark
    - [labelled-skyspark-data] - data manually labelled as anomalous or normal
- [final-report](final-report) - currently unpopulated
- [meeting-minutes](meeting-minutes/) - client meeting minutes and sprint planning documents
- [misc-docs](misc-docs/) - miscellaneous documents such as `team-contract.md` and `code-standards.md`
- [personal-logs](personal-logs/) - each team-members daily timelogs as well as a `README` with a brief summary of each week
- [proposal](proposal/) - project proposal report and presentation
- [research](research/) - various documents and code associated with researching/exploring various aspects of the project including:
    - [EDA](research/EDA/) - exploratory data analysis completed at the start of the project to understand various CEC sensors
    - [dashboard-research](research/dashboard-research.md) - initial research on dashboards with InfluxDB or Grafana to understand the level of effort associated with the task
    - [model-methods](research/model-methods/) - initial research/selection of model to be used for the study (includes various test files)
    - [papers](research/papers/) - papers used in the study
    - [streaming-methods](research/streaming-methods/) - various tests on streaming methods that could be used with InfluxDB
- [weekly-updates](weekly-updates/) - weekly presentations to UBC supervisors

