"""Linear regression of interval with the variables it can depend on"""
import pandas as pd
import datetime
import statsmodels.formula.api as smf


def separate_routes(dataframe):
    """
    Separates the routes
    :param dataframe:
    :return:
    """
    routes = dataframe["route_id"].unique()  # get unique routes
    separate_routes = []

    # Extract routes from dataframe
    for route in routes:
        separate_route = dataframe[dataframe["route_id"] == route]
        separate_routes.append(separate_route)

    return separate_routes


def preprocess_data(dataframe, list_stops, private, route):
    """
    Prepare the data for one root to be places in the build_heatmap() function
    :param dataframe:
    :return:
    """
    # Change timestamps to datetime
    dataframe["timestamp"] = dataframe["timestamp"]\
        .apply(lambda x: datetime.datetime.fromtimestamp(x))

    # Get unique stops
    bus_stops = dataframe["stop_name"].unique()
    bus_stops = [i for i in list_stops if i in bus_stops]

    # Get work hours
    index = []
    work_hours = range(5, 23)
    for i in work_hours:
        since = f"0{i}:00" if i < 10 else f"{i}:00"
        till = f"0{i + 1}:00" if i + 1 < 10 else f"{i + 1}:00"
        hours = f"{since}-{till}"
        index.append(hours)

    # Create processed table
    preprocessed = pd.DataFrame(index=index, columns=bus_stops)

    # Choose buses by stops
    listok = []
    for stop in bus_stops:
        by_stop = dataframe[dataframe["stop_name"] == stop]

        # Choose by time
        # last hour = None
        intervals_per_hour = []
        last_timestamp = 0
        for time in work_hours:
            # print(f"{time}:00-{time+1}:00")

            by_hours = by_stop[(time <= by_stop["timestamp"].apply(lambda x: x.hour))
                                    & (by_stop["timestamp"].apply(lambda x: x.hour) < time+1)]

            # Sort in the chronological order
            by_hours = by_hours.sort_values(by="timestamp")

            # Filter the data by vehicle_id (remove duplicates)
            duplicates = by_hours["vehicle_id"].duplicated()
            by_hours = by_hours[~duplicates]
            differences = []

            if last_timestamp != 0 and len(by_hours["timestamp"].tolist()) != 0:
                differences.append([round((by_hours["timestamp"].tolist()[0] - last_timestamp).total_seconds() / 60, 2),
                                    len(by_hours),
                                    time, len(bus_stops), route, private])

            for i in range(1, len(by_hours)):
                difference = by_hours["timestamp"].tolist()[i] - by_hours["timestamp"].tolist()[i-1]
                differences.append([round(difference.total_seconds() / 60, 2), len(by_hours), time,
                                   len(bus_stops), route, private])

            if len(by_hours["timestamp"]) != 0:  # if current timestamp is not empty
                last_timestamp = by_hours["timestamp"].tolist()[-1]

            intervals_per_hour.append(differences)
        listok.append(intervals_per_hour)

    return listok

def for_dataframe_read(preprocessed):
    data = []
    for stop in preprocessed:
        for time in stop:
            for interval in time:
                data.append(interval)
    df_ = pd.DataFrame(data, columns=['Interval', 'No_of_buses', 'hour', 'No_of_bus_stops', 'Route',
                                      'is_АТП_1'])
    return df_


if __name__ == '__main__':
    path = "09_05_2023.csv" # here you can change the date and get the linea regression for chosen date.
    dataframe = pd.read_csv(path)

    separate_routes = separate_routes(dataframe)

    list_of_dataframes = []
    for item in separate_routes:
        if item["route_id"].to_list()[0] in [94, 117, 2355, 1884, 102, 1001]: # 3а, 52, 5а, 61, 47, 46
            if item["route_id"].to_list()[0] == 94:
                dataframe_stops = pd.read_csv("stops/Zupynky - 3A.csv")
                list_stops = dataframe_stops["name"].to_list()
                preprocessed = preprocess_data(item, list_stops, 1, item["route_id"].to_list()[0])
                list_of_dataframes.append(for_dataframe_read(preprocessed))
            elif item["route_id"].to_list()[0] == 117:
                dataframe_stops = pd.read_csv("stops/Zupynky - 52.csv")
                list_stops = dataframe_stops["name"].to_list()
                preprocessed = preprocess_data(item, list_stops, 1, item["route_id"].to_list()[0])
                list_of_dataframes.append(for_dataframe_read(preprocessed))
            elif item["route_id"].to_list()[0] == 2355:
                dataframe_stops = pd.read_csv("stops/Zupynky - 5А.csv")
                list_stops = dataframe_stops["name"].to_list()
                preprocessed = preprocess_data(item, list_stops, 1, item["route_id"].to_list()[0])
                list_of_dataframes.append(for_dataframe_read(preprocessed))
            elif item["route_id"].to_list()[0] == 1884:
                dataframe_stops = pd.read_csv("stops/Zupynky - 61.csv")
                list_stops = dataframe_stops["name"].to_list()
                preprocessed = preprocess_data(item, list_stops, 1, item["route_id"].to_list()[0])
                list_of_dataframes.append(for_dataframe_read(preprocessed))
            elif item["route_id"].to_list()[0] == 102:
                dataframe_stops = pd.read_csv("stops/Zupynky - 47.csv")
                list_stops = dataframe_stops["name"].to_list()
                preprocessed = preprocess_data(item, list_stops, 1, item["route_id"].to_list()[0])
                list_of_dataframes.append(for_dataframe_read(preprocessed))
            elif item["route_id"].to_list()[0] == 1001:
                dataframe_stops = pd.read_csv("stops/Zupynky - 46.csv")
                list_stops = dataframe_stops["name"].to_list()
                preprocessed = preprocess_data(item, list_stops, 1, item["route_id"].to_list()[0])
                list_of_dataframes.append(for_dataframe_read(preprocessed))
        else:
            if item["route_id"].to_list()[0] == 2299:
                dataframe_stops = pd.read_csv("stops/Zupynky - 22.csv")
                list_stops = dataframe_stops["name"].to_list()
                preprocessed = preprocess_data(item, list_stops, 0, item["route_id"].to_list()[0])
                list_of_dataframes.append(for_dataframe_read(preprocessed))
            elif item["route_id"].to_list()[0] == 146:
                dataframe_stops = pd.read_csv("stops/Zupynky - 34.csv")
                list_stops = dataframe_stops["name"].to_list()
                preprocessed = preprocess_data(item, list_stops, 0, item["route_id"].to_list()[0])
                list_of_dataframes.append(for_dataframe_read(preprocessed))
            elif item["route_id"].to_list()[0] == 992:
                dataframe_stops = pd.read_csv("stops/Zupynky - 39.csv")
                list_stops = dataframe_stops["name"].to_list()
                preprocessed = preprocess_data(item, list_stops, 0, item["route_id"].to_list()[0])
                list_of_dataframes.append(for_dataframe_read(preprocessed))

    result = pd.concat(list_of_dataframes)
    result.to_csv('result_wow.csv')

    mod_all = smf.ols(formula='Interval ~ No_of_buses + hour + No_of_bus_stops + is_АТП_1', data=result)
    mod_all = mod_all.fit()
    print(mod_all.summary())