from pathlib import Path

import pandas as pd


def get_airport_locations(
    indir: str = "data/raw/btsdelay", outdir: str = "data/raw/locations"
) -> pd.DataFrame:
    """Grabs a csv database of airport locations from github and matches the ones in our dataset"""
    LOCATION_URI = "https://davidmegginson.github.io/ourairports-data/airports.csv"
    curr_path = Path().absolute()
    outfile = curr_path.joinpath(outdir).joinpath("locations.csv")

    if outfile.exists():
        return pd.read_csv(outfile)

    flight_data_path = curr_path.joinpath(indir)
    flight_df = pd.concat(
        [pd.read_parquet(i) for i in flight_data_path.glob("*.parquet")]
    )

    port_origin_list = flight_df.Origin.unique()
    port_locations = pd.read_csv(LOCATION_URI)

    locations_df: pd.DataFrame = port_locations[
        port_locations.iata_code.isin(port_origin_list)
    ].reset_index(drop=True)

    locations_df.to_csv(outfile)

    return locations_df


if __name__ == "__main__":
    get_airport_locations()
