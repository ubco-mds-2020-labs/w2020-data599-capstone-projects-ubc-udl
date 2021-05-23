rm(list=ls())


library(tidyverse)
library(plotly)
library(DT) # data table output
library(lubridate)
library(shinybusy) # busy indicator for rendering plots/tables

# customized data processing functions are in a separate file
source('functions.R') 

shinyServer(function(input, output) {
    
    data1 <- reactiveVal(tibble())

    # read csv file and convert to format for plotting
    observeEvent(input$file1, {
        inFile <- input$file1
        
        if (is.null(inFile))
            return(NULL)
        
        temp <- read.csv(input$file1$datapath, header = input$header)
        colnames(temp) <- c('Datetime', 'Value', 'ID', 'Anomaly')
        temp$Datetime <- lubridate::as_datetime(temp$Datetime)
        temp$Value <- as.numeric(temp$Value)
        temp$Anomaly <- as.logical(temp$Anomaly)
        data1(temp)
    })
    
    
    # plot the data (see functions.R for the function)
    output$plotgroup <-renderPlotly({
        suppressWarnings(plotting_func(data1()))
        
    })
    
    # data selected from the plot
    selected <- reactive({
        
        if(is.null(event_data("plotly_selected")) | 
           length(event_data("plotly_selected")) == 0){
            selected <- NULL
        } else {
            selected <- event_data("plotly_selected")
        }
        
        validate(
            need(!is.null(selected), "No data selected for removal")
        )
        
        
        selected <- selected %>%
            tibble() %>%
            
            mutate(ID = customdata,
                   # datetime was converted to numeric value in plotly_selected
                   # numerical value are in millisecond -> converted to second for datetime
                   # when datetime got converted to numeric, it was already in local time
                   # use 'UTC' to avoid duplicate timezone shift
                   # the output datetime has been manually validated against raw data
                   Datetime = as.POSIXct(x/1000, origin = '1970-01-01', tz = 'UTC')
            ) %>% 
            select(ID, Datetime) 
        
        return(selected)
    })
    
    
    # DataTable rendering
    output$removal_selected <- DT::renderDataTable({
        
        selected() %>% mutate(Datetime = Datetime %>% as.character()) %>%
            
            DT::datatable(
                
                extensions = c('FixedColumns', 'Scroller'),
                options = list(
                    
                    # Options for extension "Buttons"
                    dom = 'Bfrtip',
                    buttons = list(I('colvis')),
                    columnDefs = list(list(className = "dt-center", targets = "_all")),
                    
                    # Options for extension "FixedColumns"
                    scrollX = TRUE,
                    fixedColumns = TRUE,
                    
                    # Options for extension "Scroller"
                    deferRender = TRUE,
                    scrollY = 600,
                    scroller = TRUE
                    
                )
                
            ) # End of DT::datatable
        
    }) # End of datatable rendering
    
    # update the data labels when the action button is clicked
    observeEvent(input$update_labels, {
        if (input$label_type == 'anomaly') {
            label <- TRUE
        } else {
            label <- FALSE
        }
        
        new_table <- mutate(selected(), Anomaly = label)
        
        join_table <- left_join(data1(), new_table, by=c("Datetime", "ID")) %>%
            mutate(new = if_else(is.na(Anomaly.y), Anomaly.x, Anomaly.y)) %>%
            select(Datetime, Value, ID, Anomaly = new)
        
        data1(join_table)
    
    })
    
    # Data Download button
    output$download_data <- downloadHandler(
        filename = function() {
            paste0(input$file1$name,"_updated.csv")
        },
        content = function(file) {
            write.csv(data1(), file, row.names = FALSE)
        }
    ) # End of csv file download

    
})
