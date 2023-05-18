"""Build the map for showing intervals on certain stop on the map"""
import numpy as np
import pandas as pd
import plotly.express as px
import folium

m = folium.Map(location= [49.8397,24.0297], zoom_start=15)


if __name__ == '__main__':
    # 3A; route_id = 94
    dataframe = pd.read_csv("23_04_2023.csv")
    bus_3A = dataframe[dataframe["route_id"] == 2299] # change the number to get another route


    dataframe_stops = pd.read_csv("stops/Zupynky - 22.csv") # change the stops file to get tanotehr route
    list_stops = dataframe_stops["name"].to_list()

    unique_stops = bus_3A["stop_name"].unique()
    new_list = [i for i in unique_stops if i in list_stops]


    dict_stops = {}
    for stop in new_list:
        temporary = bus_3A[bus_3A["stop_name"] == stop]
        temporary = temporary.sort_values(by=["timestamp"])
        time_array = temporary['timestamp'].to_list()
        for i in range(0, len(time_array) - 1):
            time_array[i] = time_array[i + 1] - time_array[i]
        time_array = np.array(time_array)[:-1]
        dict_stops[stop] = [np.round(np.mean(time_array)/60, 2), [temporary.loc[temporary['stop_name'] == stop]["stop_lat"].iloc[0],
                                                  temporary.loc[temporary['stop_name'] == stop]["stop_lon"].iloc[0]]]

    for i in list(dict_stops.keys()):
       folium.Marker(
          location=[dict_stops[i][1][0], dict_stops[i][1][1]],
          popup=f"{i};\n Average waiting time/interval: {dict_stops[i][0]}",
       ).add_to(m)

    m.save("map22.html")

