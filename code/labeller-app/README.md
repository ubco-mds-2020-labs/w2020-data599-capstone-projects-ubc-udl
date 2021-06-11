# Labeller App

The labeller app is built in Shiny. It is meant to support easily self-labelling of anomalies. Note that the app was built rapidly (<1 day development) as a support tool. The app uses the plotly WebGL functionality to easily plot as much data as required without performance issues.

The app allows a user to upload a csv file of sensor data, visualize the data in an interactive graph, select data, and change the `Anomaly` column labels to be True or False based on the selected data. The user can then export the updated dataset to a csv file.

## Input/Output

The input csv file needs to have the following columns (in this order):

- **Datetime**: Datetime format (should be able to handle most formats), the manual export format from SkySpark was tested with the app and works
- **Value:**: A column of numeric sensor values, note that any non-numeric values will be coerced to NAs
- **ID:** Any label used to identify a sensor, multiple sensors can be used in a single file and they will be plotted as different colors
- **Anomaly:** True/False and needs to be fully populated prior to import to the app

The file `test.csv` was used to test input data to the app. Note that the column names are not required, they just need to be in this order.

The output format is the same as the input format but will have the columns labelled using the names in the above list. **Note:** The timezone of the output data will be UTC (converted from whatever input timezone was used).

## Loading the App

The app uses the [`renv` package](https://rstudio.github.io/renv/articles/renv.html). Use `renv::restore()` to load and use the environment. Running the app can easily be done through RStudio. Note that due to the use of WebGL, it is recommended to run the app in a web browser and not through the RStudio pop-up.

## Demo

A demo of the app is available [here](../../images/app.GIF). It includes loading a file (previously labelled) that has approximately 400,000 data points (34 MB file), interactively moving around the graph, selecting/labelling data points as anomalous, and downloading the updated file. The demo shows that while loading the graph takes some timem interacting with the graph has good performance.