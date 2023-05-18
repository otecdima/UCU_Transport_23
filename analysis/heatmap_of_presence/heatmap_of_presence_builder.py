"""Build the heatmap of presence of route (number of vehicles on the route) in certain hour"""
import pandas as pd
import re
import plotly.graph_objs as go


def order_data(dataframe):

    # create dataframes
    real_route_presence = pd.DataFrame()
    planned_route_presence = pd.DataFrame()

    # get route carrier name
    route_carrier_data = list(dataframe.iloc[0])[0]
    route_carrier = re.search('"(.*?)"', route_carrier_data).group()

    # initialize work hours
    index = []
    work_hours = range(5, 23)
    for i in work_hours:
        since = f"0{i}:00" if i < 10 else f"{i}:00"
        till = f"0{i+1}:00" if i+1 < 10 else f"{i+1}:00"
        hours = f"{since}-{till}"
        index.append(hours)
    index.append("Presence rate")

    real_route_presence.index = index
    planned_route_presence.index = index

    # fill real route presence
    i = 1
    non_null_entries_amount = 36
    current_bus = None
    current_coefficient = None

    for _, row in dataframe.drop(index=dataframe.index[:3]).iterrows():

        # if even column: fill planned and real bus number with values
        if i % 2 == 0:
            # get planned buses number
            planned_bus_number = []
            for j in range(0, non_null_entries_amount, 2):
                bus_number = 0 if type(row[j]) != str else int(row[j])
                planned_bus_number.append(bus_number)

            # get real buses number
            real_bus_number = []
            for j in range(1, non_null_entries_amount, 2):
                bus_number = 0 if type(row[j]) != str else int(row[j])
                real_bus_number.append(bus_number)

            # add planned buses route presence
            planned_bus_number.append(current_coefficient)
            planned_route_presence[current_bus] = planned_bus_number

            # add real buses route presence
            real_bus_number.append(current_coefficient)
            real_route_presence[current_bus] = real_bus_number

        # if odd columns: define bus and presence coefficients
        else:
            current_bus = row[0]
            current_coefficient = row[len(row)-1]
            current_coefficient = current_coefficient.replace(",", ".")
            current_coefficient = float(current_coefficient)

        i += 1

    # real_route_presence.replace(0, -1, inplace=True)  # no need to do this
    planned_route_presence.replace(0, -1, inplace=True)

    # real_route_presence.fillna(-1, inplace=True)  # no need to do this
    planned_route_presence.fillna(-1, inplace=True)

    return real_route_presence, planned_route_presence, route_carrier


def compose_heatmap(dataframe, route_carrier):
    # heatmap about the intervals_development compliance
    heatmap = go.Heatmap(z=dataframe.values,
                         x=dataframe.columns,
                         y=dataframe.index)
    layout = go.Layout(title=f"Presence Rate Hourly For {route_carrier}")
    fig = go.Figure(data=[heatmap], layout=layout)
    return fig


def main():
    # read data
    path = "sample0.csv"
    dataframe = pd.read_csv(path)

    # order data
    real_route_presence, planned_route_presence, route_carrier = order_data(dataframe)

    # write data to csv
    real_route_presence.to_csv("real_route_presence.csv")
    planned_route_presence.to_csv("planned_route_presence.csv")

    # find ratio real/planned to be used in the heatmap
    real_to_planned_relation = real_route_presence[:-1] / planned_route_presence[:-1]

    # make heatmap
    heatmap = compose_heatmap(real_to_planned_relation, route_carrier)
    heatmap.show()


if __name__ == '__main__':
    main()
