"""Build histogram of interval time per stop"""
import numpy as np
import pandas as pd
import plotly.express as px


if __name__ == '__main__':
    # 3A; route_id = 94
    dataframe = pd.read_csv("23_04_2023.csv")
    bus_3A = dataframe[dataframe["route_id"] == 94] # simply change the id to get other bus' intervals


    dataframe_stops = pd.read_csv("stops/Zupynky - 3A.csv")
    list_stops = dataframe_stops["name"].to_list()

    unique_stops = bus_3A["stop_name"].unique()
    new_list = [i for i in unique_stops if i in list_stops]

    counter = 0
    for stop in new_list:
        temporary = bus_3A[bus_3A["stop_name"] == stop]
        temporary = temporary.sort_values(by=["timestamp"])
        time_array = temporary['timestamp'].to_list()
        for i in range(0, len(time_array) - 1):
            time_array[i] = time_array[i + 1] - time_array[i]
        time_array = np.array(time_array)[:-1]
        time_array = pd.DataFrame(time_array, columns=["time interval"])
        time_array = time_array.apply(lambda x : round(x / 60, 2))
        fig = px.histogram(time_array, x="time interval", nbins=100, width=1400, height=700)
        fig.update_layout(title=f"Histogram of Time Intervals for Stop {stop} for route 3A")
        fig.show()
        if counter == 5:
            break
        counter += 1
