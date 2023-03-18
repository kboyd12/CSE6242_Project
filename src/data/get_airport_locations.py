import pandas as pd
from pathlib import Path


def get_airport_locations(
    indir: str = "data/raw/btsdelay", outdir: str = "data/raw/locations"
) -> pd.DataFrame:
    LOCATION_URI = "https://raw.githubusercontent.com/plotly/datasets/master/2011_february_us_airport_traffic.csv"

    curr_path = Path()
    flight_data_path = curr_path.absolute().joinpath(indir)

    flight_df = pd.concat(
        [pd.read_parquet(i) for i in flight_data_path.glob("*.parquet")]
    )

    port_origin_list: list = flight_df.Origin.unique()
    port_locations = pd.read_csv(LOCATION_URI)

    locations_df = port_locations[port_locations.iata_code.isin(port_origin_list)]

    return locations_df
