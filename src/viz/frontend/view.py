import asyncio
import plotly.graph_objects as go

from ...data.get_airport_locations import get_airport_locations
from ...data.helper_scripts import flight_trace_locations_df


async def trace_lines() -> go.Scattergeo:
    df = await flight_trace_locations_df()
    return go.Scattergeo()


async def create_plot(width: int = 1200, height: int = 900) -> go.Figure:
    df = await get_airport_locations()

    trace = go.Scattermapbox(
        # locationmode="USA-states",
        lon=df.longitude_deg,
        lat=df.latitude_deg,
        hoverinfo="text",
        text=df.name,
        mode="markers",
        marker=dict(size=3, color="rgb(255,0,0)"),
    )

    fig = go.Figure(trace)

    fig.update_layout(
        mapbox=dict(
            style="carto-positron",
            center=dict(lat=df.latitude_deg.mean(), lon=df.longitude_deg.mean()),
            zoom=3.5,
        )
    )
    # fig = go.Figure(
    #     data=[trace],
    #     layout=go.Layout(
    #         # title_text="Placeholder Title for Now",  # TODO
    #         showlegend=False,
    #         width=width,
    #         height=height,
    #         autosize=True,
    #         geo=dict(
    #             projection_type="orthographic",
    #             projection_rotation=dict(lon=-102.5795, lat=25.8283),
    #             showland=True,
    #             showocean=True,
    #             showcountries=True,
    #             landcolor="rgb(243,243,243)",
    #             countrycolor="rgb(204,204,204)",
    #             bgcolor="#070606",
    #             oceancolor="#5b7882",
    #         ),
    #     ),
    # )

    return fig


if __name__ == "__main__":
    asyncio.run(create_plot()).show()
