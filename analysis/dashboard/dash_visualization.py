import pandas as pd

import os

import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output

from schedule_compliance.heatmaps_for_database import heatmaps_builder as builder


def business_logic(path):
    route_data = pd.read_csv("../bus_data/routes.txt")
    path = f"../dates_data/{path.replace('.', '_') + '.csv'}"

    dataframe = pd.read_csv(path)

    # Separate routes and get their names
    separate_routes = builder.separate_routes(dataframe)
    route_names = [route_data["route_id"].to_list()[0] for route_data in separate_routes]
    for i in range(len(route_names)):
        route_names[i] = route_data.loc[route_data['route_id'] == route_names[i], 'route_short_name'].iloc[0]

    # Clean from A16
    index = route_names.index("А16")
    separate_routes.pop(index)
    route_names.pop(index)

    # Get stops
    list_stops = []
    for route_name in route_names:
        dataframe_stops = pd.read_csv(f"../routes/route_{route_name}.csv")
        list_stops.append(dataframe_stops["name"].to_list())

    # Build heatmaps for each route
    preprocessed = [builder.preprocess_data(separate_routes[i], list_stops[i]) for i in range(len(separate_routes))]

    heatmaps = {}
    for i in range(len(preprocessed)):
        heatmaps.setdefault(route_names[i], builder.build_heatmap(preprocessed[i], route_names[i]))

    # Create dropdown for available routes for analysis
    route_dropdown_options = [{"label": route_names[i], "value": route_names[i]} for i in range(len(route_names))]

    return heatmaps, route_dropdown_options


# <!!!> MAKE IT POSSIBLE TO CHOOSE WHAT DAY TO DISPLAY <!!!>
possible_days = os.listdir("../dates_data")
date_dropdown_options = [day.replace(".csv", "").replace("_", ".") for day in possible_days]
dates_data = {}
for i in range(len(date_dropdown_options)):
    dates_data.setdefault(date_dropdown_options[i], business_logic(date_dropdown_options[i])[0])

# Get data about routes
route_data = pd.read_csv("../bus_data/routes.txt")

# read data
path = f"../dates_data/08_05_2023.csv"
dataframe = pd.read_csv(path)

# Separate routes and get their names
separate_routes = builder.separate_routes(dataframe)
route_names = [route_data["route_id"].to_list()[0] for route_data in separate_routes]
for i in range(len(route_names)):
    route_names[i] = route_data.loc[route_data['route_id'] == route_names[i], 'route_short_name'].iloc[0]

# Clean from A16
index = route_names.index("А16")
separate_routes.pop(index)
route_names.pop(index)

# Get stops
list_stops = []
for route_name in route_names:
    dataframe_stops = pd.read_csv(f"../routes/route_{route_name}.csv")
    list_stops.append(dataframe_stops["name"].to_list())

# Build heatmaps for each route
heatmaps = [builder.preprocess_data(separate_routes[i], list_stops[i]) for i in range(len(separate_routes))]
heatmaps = [builder.build_heatmap(heatmaps[i], route_names[i]) for i in range(len(heatmaps))]

# Create dropdown for available routes for analysis
route_dropdown_options = [{"label": route_names[i], "value": route_names[i]} for i in range(len(route_names))]

# Dash app
app = dash.Dash(__name__)

app.layout = html.Div(children=[
    html.H1(children="Schedule Compliance Research"),

    html.Div(children="""
        Schedule Compliance Research for the routes
    """),

    dcc.Dropdown(
        id='date_dropdown',
        options=date_dropdown_options,
        value=date_dropdown_options[0],
        style={'width': '50%'}
    ),

    dcc.Dropdown(
        id='route_dropdown',
        options=route_dropdown_options,
        value=route_dropdown_options[0]["value"],
        style={'width': '50%'}
    ),

    dcc.Graph(
        id='heatmap',
        figure=dates_data[date_dropdown_options[0]][route_names[0]]
    )],

    style={
        'font-family': 'Arial'
    })


@app.callback(
    Output('heatmap', 'figure'),
    [Input('route_dropdown', 'value'), Input('date_dropdown', 'value')]
)
def update_heatmap_on_route(route_name, date):
    heatmap = dates_data[date][route_name]
    return heatmap


if __name__ == '__main__':
    app.run_server(debug=True)
