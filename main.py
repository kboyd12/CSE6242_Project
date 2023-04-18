import asyncio
import calendar
import json

import pandas as pd
from dash import Dash, Input, Output, State, dcc, html

from src.data.get_airport_locations import CURR_PATH, get_airport_locations
from src.viz.frontend.view import (
    create_plot,
    trace_lines,
    airport_points,
    flight_trace_df,
)
from src.model.model_utils import load_model, predictions

airline_list = (
    pd.read_csv(CURR_PATH.joinpath("src/data/airline_list.csv"))
    .Airline.sort_values()
    .to_list()
)
airline_lookup = pd.read_parquet("src/data/airline_lookup.parquet")

model = load_model()

fig = asyncio.run(create_plot())

external_stylesheets = [
    {
        "href": (
            "https://fonts.googleapis.com/css2?" "family=Lato:wght@400;700&display=swap"
        ),
        "rel": "stylesheet",
    },
]

app = Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.H1(children="Team 154 CSE 6242 Project", className="header-title"),
                html.P(
                    children="""
                    Choose your preferred airline and Month of flight in the dropdowns, then click on an airport in the map to view chance of delay
                    """,
                    className="header-description",
                ),
            ],
            className="header",
        ),
        html.Div(
            children=[
                html.Div(children="Airline", className="menu-title"),
                dcc.Dropdown(
                    id="airline-filter",
                    options=[
                        {"label": airline, "value": airline} for airline in airline_list
                    ],
                    value="Airline",
                    clearable=False,
                    className="dropdown",
                ),
                html.Div(children="Month", className="menu-title"),
                dcc.Dropdown(
                    id="month-filter",
                    options=[
                        {"label": month, "value": month}
                        for month in list(calendar.month_name)[1:]
                    ],
                    value="January",
                    clearable=False,
                    className="dropdown",
                ),
            ],
            className="menu",
        ),
        html.Div(id="asdf", className="prediction-container"),
        html.Div(
            children=[
                html.Div(
                    children=dcc.Graph(
                        figure=fig,
                        id="airport-chart",
                    ),
                    className="card",
                ),
            ],
        ),
    ],
)


@app.callback(
    Output("asdf", "children"),
    Input("airport-chart", "clickData"),
    State("airline-filter", "value"),
    State("month-filter", "value"),
)
def display_click_data(click_data, drop_val_1, drop_val_2):
    if drop_val_1 == "Airline":
        return (html.H3("Choose an Airline for Predictions", id="predictions-title"),)

    if click_data is not None:
        origin = click_data["points"][0]["customdata"]
        airline = drop_val_1
        month = list(calendar.month_name).index(drop_val_2)

        x, y = predictions(model, origin=[origin], airline=[airline], month=[month])

        return html.Div(
            children=[
                html.H3("Probability of Delay > 5 Minutes", id="predictions-title"),
                html.P(
                    f"From: {origin} Airport | {x}% Chance of No Delay -- {y}% Chance of >5 Minute Delay",
                    id="predicted-delay",
                ),
            ],
            className="predictions",
        )
    else:
        return html.Div()


@app.callback(
    Output("airport-chart", "figure"),
    [Input("airport-chart", "clickData"), Input("airline-filter", "value")],
    [State("airport-chart", "figure")],
)
def on_map_click(click_data, drop_val, map_state):
    filtered_ports = None

    if drop_val != "Airline":
        mask = airline_lookup.Airline.apply(lambda x: drop_val in x)
        filtered_df = airline_lookup[mask]
        filtered_ports = list(filtered_df.Origin.unique()) + list(
            filtered_df.Dest.unique()
        )

        airport_locations = asyncio.run(get_airport_locations())
        df = airport_locations[airport_locations.iata_code.isin(filtered_ports)]

        fig.update({"data": [airport_points(df)]})

    if len(fig.data) > 1:  # type: ignore
        fig.data = [fig.data[1]]

    if click_data is not None:
        if filtered_ports != None:
            lookup_df = flight_trace_df[(flight_trace_df.Dest.isin(filtered_ports))]

            fig.add_traces(
                trace_lines(click_data["points"][0]["customdata"], lookup_df=lookup_df)
            )
        else:
            fig.add_traces(trace_lines(click_data["points"][0]["customdata"]))

        fig.data = [fig.data[1], fig.data[0]]

        fig.update_layout(
            mapbox=dict(
                style="carto-positron",
                center=map_state["layout"]["mapbox"]["center"],
                zoom=map_state["layout"]["mapbox"]["zoom"],
            )
        )

    return fig


if __name__ == "__main__":
    app.run_server(use_reloader=True)
