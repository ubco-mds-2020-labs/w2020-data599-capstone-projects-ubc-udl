# function for plotting trace
plotting_func <- function(df){
    
    fig <- suppressPlotlyWarnings(plot_ly(data = df, x = ~Datetime, y = ~Value, 
                                          color = ~factor(Anomaly),
                                          symbol = ~factor(ID),
                                          type='scattergl', mode = "markers", 
                                          height = 800,
                                          customdata = ~ID,
                                          legendgroup = ~ID, 
                                          showlegend = TRUE)) %>%
        # register selected points
        event_register(., "plotly_selected")
    
    
    # Add range slider
    fig <- fig %>% layout(
        xaxis=list(
            rangeslider=list(
                visible=TRUE,
                thickness=0.05
            ),
            type="date",
            title = "Datetime"
        ),
        # re-enable the zooming of y-axis after adding the slider
        yaxis=list(fixedrange=FALSE)
    )
    
    fig
}

# warning about WebGL does not plot in RStudio despite app launched in webbrowser
# warning about too many ID for 8 color paletes (will auto generate more colors anyway)
# surpress them is not that easy...must go around with plotly_build()
# https://www.rdocumentation.org/packages/plotly/versions/3.6.0/topics/plotly_build
# https://github.com/ropensci/plotly/issues/1202

suppressPlotlyWarnings <- function(p) {
    suppressWarnings(plotly_build(p))
}
