"""Build heatmap for intervals per hour and per stop for chosen route"""
import pandas as pd
import datetime
import plotly.graph_objs as go


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


def preprocess_data(dataframe, list_stops):
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

            # Find differences
            differences = []

            if last_timestamp != 0 and len(by_hours["timestamp"].tolist()) != 0:
                differences.append(by_hours["timestamp"].tolist()[0] - last_timestamp)

            for i in range(1, len(by_hours)):
                difference = by_hours["timestamp"].tolist()[i] - by_hours["timestamp"].tolist()[i-1]
                differences.append(difference)

            if len(by_hours["timestamp"]) != 0:  # if current timestamp is not empty
                last_timestamp = by_hours["timestamp"].tolist()[-1]

            # Get the sum of times
            times_sum = sum(differences, datetime.timedelta(hours=0, minutes=0, seconds=0))
            times_amount = len(differences)

            # Calculate the average interval and add it to the list
            average_interval = datetime.timedelta(hours=0, minutes=0, seconds=0)
            if times_sum != 0 and times_amount != 0:
                average_interval = times_sum / times_amount

            intervals_per_hour.append(average_interval)

        for i in range(len(intervals_per_hour)):
            intervals_per_hour[i] = round(intervals_per_hour[i].total_seconds() / 60, 2)

        preprocessed[stop] = intervals_per_hour

    return preprocessed


def build_heatmap(dataframe):
    """
    Builds heatmap
    :param dataframe:
    :return:
    """
    heatmap = go.Heatmap(
        x=dataframe.columns,
        y=dataframe.index,
        z=dataframe.values
    )
    layout = go.Layout(title=f"Average intervals per bus stop for 3A")
    fig = go.Figure(data=[heatmap], layout=layout)
    fig.show()


if __name__ == '__main__':
    path = "23_04_2023.csv"
    dataframe = pd.read_csv(path)

    dataframe_stops = pd.read_csv("stops/Zupynky - 3A.csv")  # 3A, 22 (here you can change the file with stops for another route)
    list_stops = dataframe_stops["name"].to_list()

    separate_routes = separate_routes(dataframe)
    preprocessed = preprocess_data(separate_routes[6], list_stops)  # 6, 8 (here also you should change the index to get the chose route)
    build_heatmap(preprocessed)
