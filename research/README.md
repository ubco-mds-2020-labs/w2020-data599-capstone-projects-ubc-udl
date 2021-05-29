# Research Folder

Contains research based components of the project including:

- `dashboard_research.md` provides initial research on dashboards with InfluxDB or Grafana to understand the level of effort associated with the task
- `EDA` folder contains the initial exploratory data analysis completed for the project
    - completed on a very limited dataset accessed through manual data downloads from the SkySpark UI
    - `UDL_EDA.ipynb` provides the notebook for the analysis
- `model-methods` folder contains the research associated with selecting the model to move forward with
    - LSTM model selected and comments on the selection are provided in the file `model_selection.md`
    - `performance_selection.md` provides comments on how we will evaluate the model/study
    - `comparison_of_packages.xlsx` provides comment on several packages that are available for anomaly detection in python (however, it was decided to build our own LSTM in Keras ultimately)
    - contains the `model-demo` folder which includes initial testing on various packages and the high-level tests on an LSTM model
- `papers` folder provides references used in the project (ongoing)
- `SR-testing` testing spectral residual transformations on the manually labelled [datasets](../data/labelled-skyspark-data/)
- `streaming-methods` folder includes various tests on streaming methods that could be used with InfluxDB
    - completed when trying to understand how the detection streaming framework with InfluxDB and what tools/packages would be required to implement it
    - contains `README.md` in the folder for description of findings
    - provides various `.py` and `.ipynb` files used for testing as described in the README

