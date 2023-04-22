import numpy as np
import pandas as pd
import xarray as xr
import scipy.sparse as sp
import glob
import os
from tqdm import tqdm
import pyarrow.parquet as pq
import pickle


filedir_path = os.path.join(os.getcwd(), 'data', 'raw', 'btsdelay')
files = glob.glob(os.path.join(filedir_path, "Combined_Flights_*.parquet"))

def construct_adj_mat(flights: pd.DataFrame, squared: bool) -> pd.DataFrame:
    """ajd matrix of form Aij => flight from i to j, id est rows are origin, cols are dest """

    if squared:
        f = lambda df_: df_['ArrDelay']**2
    else:
        f = lambda df_: df_['ArrDelay']

    delays = (flights
                .assign(delay = f,
                        dtime=lambda df_: pd.to_datetime((df_['FlightDate'].astype(str) + " " +
                                                        df_['CRSDepTime'].astype(int).astype(str)),
                            format="%Y-%m-%d %H%M%S", errors='coerce'))
                [['Origin', 'Dest', 'delay', 'dtime']]
                .groupby(['Origin', 'Dest', pd.Grouper(key='dtime', freq="H")])
                .agg(mean_delay = pd.NamedAgg('delay', np.sum),)
                .reset_index()
                )

    locs = np.unique(np.concatenate((flights['Origin'].unique(), flights['Dest'].unique())))
    
    time_grouped = (delays
                    .groupby(pd.Grouper(key="dtime", freq="H")))

    adj_mat = xr.DataArray(np.zeros((len(locs), len(locs), len(time_grouped)), dtype=np.single),
                           dims=("Origin", "Dest", "timestamp"),
                           coords={"Origin": locs, 'Dest': locs, 'timestamp': [t for t, _ in time_grouped]})
    
    for timestamp, group in time_grouped:
        for idx, origin, dest, dtime, mean_delay in group.itertuples():
            adj_mat.loc[{'Origin': origin, 'Dest': dest, 'timestamp': timestamp}] = mean_delay

    return adj_mat


def adj_mat_to_file(adj_mat: xr.DataArray=None, filepath: str=None) -> None:
    if not filepath:
        filepath = os.path.join(os.getcwd(), "data", "processed", "flight_ts_graphs")
    os.makedirs(filepath, exist_ok=True)
    amt = adj_mat.transpose('timestamp', ...)

    with open(os.path.join(filepath, 'columns'), 'wb') as f:
        pickle.dump(adj_mat.Origin.values, f)

    for hr in amt:
        coo_adj_mat = sp.coo_matrix(hr.values)
        print(coo_adj_mat.shape)
        sp.save_npz(file=os.path.join(filepath, f"file_{hr.timestamp.item()}.npz"), 
                    matrix=coo_adj_mat,
                    compressed=True)
    return None

if __name__ == "__main__":
    columns = ['ArrDelay', 'FlightDate', 'CRSDepTime', 'Origin', 'Dest',]
    for file in files:
        parquet_file = pq.ParquetFile(file)
        for i, batch in enumerate(tqdm(parquet_file.iter_batches(columns=columns,
                                                    batch_size=2**19))):
            if i < 4:
                continue

            batch_df = batch.to_pandas()
            adj_mat = construct_adj_mat(batch_df, squared=False)
            adj_mat_to_file(adj_mat)

        