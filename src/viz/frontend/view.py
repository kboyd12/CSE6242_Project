import plotly.graph_objects as go

from ...data.get_airport_locations import get_airport_locations


def create_plot():
    df = get_airport_locations()

    fig = go.Figure()

    fig.add_trace(
        go.Scattergeo(
            locationmode="USA-states",
            lon=df.longitude_deg,
            lat=df.latitude_deg,
            hoverinfo="text",
            text=df.name,
            mode="markers",
            marker=dict(size=2, color="rgb(255,0,0)"),
        )
    )

    fig.update_layout(
        title_text="Placeholder Title for Now",  # TODO
        showlegend=False,
        geo=dict(
            scope="north america",
            projection_type="azimuthal equal area",
            showland=True,
            landcolor="rgb(243,243,243)",
            countrycolor="rgb(204,204,204)",
        ),
    )

    return fig
