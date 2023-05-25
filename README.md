# Lviv Transport Analysis

## About
- Obtaining information about public transport stops and routes from the results of the project "Optimization of transport connections Lviv UCU-2022.
- Collection of information about public transport traffic schedules in divisions of the Lviv City Council
- Development of algorithms for determining the fact of public transport visiting stops based on open data on public transport traffic, which are published in the GTFS format.
- Identification of metrics for the detection of mass non-compliance with public transport traffic schedules.
- Development of algorithms for calculating metrics for detecting mass non-compliance with public transport traffic schedules and their testing on data for one month.

## Content of the repository
- _tools_ - code for receiving the data of fact of visiting stops based on data gathered for certain day. Also storing in database.
- _data_ - all the data received by ourselves such as open sources and Lvivavtodor documentation.
- _analysis_ - code for analysis, building heatmaps, histograms, dashboard and running linear regression model for certain day.

## analysis
In this topic we will explain the key features that need to be understood in order to interpret the code written. In `analysis` folder we have the following files:
- `bus_stops_histogram_builder.py`
- `heatmaps_builder.py`
- `interval_plot_builder.py`
- `intervals_for_stops_map_builder.py`
- `linear_regression.py`

First of all, let's discuss the `bus_stops_histogram_builder.py`. The code provided builds the histograms of waiting time for the certain bus on the certain bus stop. On the x-axis of the provided histogram we have time that people had to wait in order to get the bus. On the y-axis we have the number of occurences of such waiting time.

Let's now move on to the `heatmaps_builder.py`. This code provides tools that prepare the data for plotting the heatmaps and plots the heatmaps. Here we will briefly discuss the functions that are present in this file:
- `separate_routes(dataframe)` - separates roots into another array
- `preprocess_data(dataframe, list_stops)` - this function takes the data and prepares it for the histogram building. It finds the differences between the arrival of the busses during the certain hour, therefore forming the time that people need to wait in order to catch the bus in the bus stop. Since the code is unable to provide the results if there is no two bus arrivals in the bus stop, we added the feature of saving the last time the bus comes to the bus stop and including it into the waiting hours. Afterwards, we calculate the average wainting time for each hour and each busstop. The brighter is the color, the more time it was necessary to wait for the next bus to come. Sometimes the waiting time can exceed the 1 hour. That means that the bus came only one during that hour and the time displayed is essentially

to clean the data and build the heatmaps of the average waiting time fot the ceratain root 

## The team - students of IT and Business Analytics Programm:
- Sofiia Yamkova
- Dmytro Batko
- Tetiana Vinnik
- Andrii Vandzhura
- Veronika Shevtsova
- Valeriia Fedorchak
- Mariana Skoropad
