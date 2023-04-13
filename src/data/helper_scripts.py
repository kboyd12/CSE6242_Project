import asyncio
from pathlib import Path

import pandas as pd

from .get_airport_locations import build_flight_data
from .get_airport_locations import get_airport_locations

CURR_PATH = Path().absolute()


async def build_ariline_list():
    """Builds the list of unique airlines to avoid loading the full dataframe each time"""
    df = await build_flight_data()

    pd.DataFrame(df.Airline.unique(), columns=["Airline"]).to_csv(
        "src/data/airline_list.csv", index=False
    )


async def flight_trace_locations_df(outfile: str = "src/data/flight_traces.parquet"):
    """Returns a dataframe of Origin, Destination with their respective LATs and LONs"""

    trace_file = CURR_PATH.joinpath(outfile)

    if trace_file.exists():
        return pd.read_parquet(trace_file)

    df = await build_flight_data()
    dff = await get_airport_locations()

    group_df = df.groupby("Origin").Dest.unique()
    group_df = pd.DataFrame(group_df.explode()).reset_index()

    merged_df = pd.merge(group_df, dff, left_on="Origin", right_on="iata_code").merge(
        dff, left_on="Dest", right_on="iata_code", suffixes=("_origin", "_dest")
    )

    final_df: pd.DataFrame = merged_df[
        [
            "Origin",
            "Dest",
            "latitude_deg_origin",
            "longitude_deg_origin",
            "latitude_deg_dest",
            "longitude_deg_dest",
        ]
    ]

    final_df.to_parquet(trace_file)

    return final_df


if __name__ == "__main__":
    asyncio.run(build_ariline_list())
