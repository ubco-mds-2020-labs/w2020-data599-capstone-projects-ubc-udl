rm(list=ls())

library(shiny)
library(plotly)
library(shinycssloaders) # withSpinner() calculation/rendering in progress
library(shinythemes)

options(shiny.maxRequestSize = 75*1024^2) # increase allowable filesize

# a more elegant solution than multiple br()
linebreaks <- function(n){HTML(strrep(br(), n))}

shinyUI(fluidPage(
    
    theme = shinytheme("sandstone"),

    # Application title
    titlePanel("Label Anomalies"),
    

    # tabset
    tabsetPanel(
        # data input tab
        tabPanel(
            "Read/Write Data",
            fileInput("file1", "Choose CSV File",
                      accept = c(".csv")
                      ),
            checkboxInput("header", "Header", TRUE),
            downloadButton("download_data", "Download Data")
            ),

        # plotting tab
        tabPanel(
            "View/Label Data",
            br(),
            shinycssloaders::withSpinner(plotlyOutput('plotgroup')),
            # use linebreak to adjust
            linebreaks(22),
            fluidRow(
                    column(3, offset=1,
                           h4("Data Removal Log Entry"),
                           selectInput('label_type', 'Label',
                                       choices = c('Anomaly' = 'anomaly',
                                                   'Normal' = 'normal'),
                                       selected = 'Anomaly'
                                       ),
                           actionButton("update_labels", "Update Labels"),
                           br()
                           ),
                    column(6,
                           DT::dataTableOutput('removal_selected')
                            )
            )
        )
    )
))
