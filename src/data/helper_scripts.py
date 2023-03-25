import asyncio
import pandas as pd
from .get_airport_locations import build_flight_data


async def main():
    # Builds the list of unique airlines to avoid loading the full dataframe each time
    df = await build_flight_data()

    pd.DataFrame(df.Airline.unique(), columns=["Airline"]).to_csv(
        "src/data/airline_list.csv", index=False
    )


if __name__ == "__main__":
    asyncio.run(main())
