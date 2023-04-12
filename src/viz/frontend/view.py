import asyncio
from typing import Tuple

import plotly.graph_objects as go

from ...data.get_airport_locations import get_airport_locations
from ...data.helper_scripts import flight_trace_locations_df
import numpy as np
import pandas as pd

flight_trace_df = asyncio.run(flight_trace_locations_df())


def start_end_array(df: pd.DataFrame) -> Tuple[np.ndarray, np.ndarray]:
    lons = np.empty(3 * len(df))
    lats = np.empty(3 * len(df))

    lons[::3] = df.longitude_deg_origin
    lons[1::3] = df.longitude_deg_dest
    lons[2::3] = None

    lats[::3] = df.latitude_deg_origin
    lats[1::3] = df.latitude_deg_dest
    lats[2::3] = None

    return (lats, lons)


def trace_lines(
    iata_code: str, lookup_df: pd.DataFrame = flight_trace_df
) -> go.Scattermapbox:
    df = lookup_df[lookup_df.Origin == iata_code]
    lat, lon = start_end_array(df)

    line_trace = go.Scattermapbox(
        lon=lon,
        lat=lat,
        mode="lines",
        line=dict(width=1, color="red"),
        opacity=0.3,
        below="Airports",
        name="Flight Paths",
    )

    return line_trace


async def create_plot() -> go.Figure:
    df = await get_airport_locations()

    trace = go.Scattermapbox(
        lon=df.longitude_deg,
        lat=df.latitude_deg,
        hoverinfo="text",
        text=df.name,
        mode="markers",
        marker=dict(size=3, color="rgb(255,0,0)"),
        customdata=df.iata_code,
        name="Airports",
    )

    fig = go.Figure(trace)

    fig.update_layout(
        mapbox=dict(
            style="carto-positron",
            center=dict(lat=df.latitude_deg.mean(), lon=df.longitude_deg.mean()),
            zoom=3.5,
        )
    )

    return fig


if __name__ == "__main__":
    asyncio.run(create_plot()).show()
