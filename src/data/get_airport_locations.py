import asyncio
from pathlib import Path

import pandas as pd

CURR_PATH = Path().absolute()


async def build_flight_data(
    indir: str = "data/raw/btsdelay", outdir: str = "data/raw/btsdelay"
) -> pd.DataFrame:
    infiles = CURR_PATH.joinpath(indir)
    outfile = CURR_PATH.joinpath(outdir, "comb_data.parquet")

    if outfile.exists():
        return pd.read_parquet(outfile)

    df = pd.concat([pd.read_parquet(i) for i in infiles.glob("*.parquet")])
    df.to_parquet(outfile)
    return df


async def get_airport_locations(
    indir: str = "data/raw/btsdelay", outdir: str = "data/raw/locations"
) -> pd.DataFrame:
    """Grabs a csv database of airport locations from github and matches the ones in our dataset"""

    LOCATION_URI = "https://davidmegginson.github.io/ourairports-data/airports.csv"

    outfile = CURR_PATH.joinpath(outdir).joinpath("locations.parquet")

    if outfile.exists():
        return pd.read_parquet(outfile)

    flight_df = await build_flight_data(indir)

    port_origin_list = flight_df.Origin.unique()
    port_locations = pd.read_csv(LOCATION_URI)

    locations_df: pd.DataFrame = port_locations[
        port_locations.iata_code.isin(port_origin_list)
    ].reset_index(drop=True)

    locations_df.to_parquet(outfile)

    return locations_df


if __name__ == "__main__":
    df = asyncio.run(build_flight_data())
