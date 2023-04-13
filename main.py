import asyncio

import pandas as pd
from dash import Dash, Input, Output, dcc, html

from src.data.get_airport_locations import CURR_PATH
from src.viz.frontend.view import create_plot, trace_lines

airline_list = (
    pd.read_csv(CURR_PATH.joinpath("src/data/airline_list.csv"))
    .Airline.sort_values()
    .to_list()
)
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
                    children="Flight Delay Model, TODO", className="header-description"
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
                    value=airline_list[0],
                    clearable=False,
                    className="dropdown",
                ),
            ],
            className="menu",
        ),
        html.Div(
            children=[
                html.Div(
                    children=dcc.Graph(
                        figure=fig,
                        id="airport-chart",
                    ),
                    className="card",
                )
            ],
        ),
    ],
)


@app.callback(Output("airport-chart", "figure"), [Input("airport-chart", "clickData")])
def on_map_click(click_data):
    if len(fig.data) > 1:
        fig.data = [fig.data[1]]
    if click_data is not None:
        fig.add_traces(trace_lines(click_data["points"][0]["customdata"]))
        fig.data = [fig.data[1], fig.data[0]]

    return fig


if __name__ == "__main__":
    app.run_server(debug=True, use_reloader=True)
