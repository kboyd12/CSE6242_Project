import numpy as np
import pandas as pd
import xarray as xr
import scipy.sparse as sp
import glob
import os

filedir_path = "../../data/raw/btsdelay/"
files = glob.glob(f"{filedir_path}*.parquet")

def construct_adj_mat(flights: pd.DataFrame) -> pd.DataFrame:
    """ajd matrix of form Aij => flight from i to j, id est rows are origin, cols are dest """

    squared_delays = (flights
                      .assign(sqrd_delay = lambda df_: df_['ArrDelay']**2,
                              dtime=lambda df_: pd.to_datetime((df_['FlightDate'].astype(str) + " " +
                                                                df_['CRSDepTime'].astype(int).astype(str)),
                                    format="%Y-%m-%d %H%M%S", errors='coerce'))
                      [['Origin', 'Dest', 'sqrd_delay', 'dtime']]
                      .groupby(['Origin', 'Dest', pd.Grouper(key='dtime', freq="H")])
                      .agg(mean_sqr_delay = pd.NamedAgg('sqrd_delay', np.sum),)
                      .reset_index()
                      )

    locs = np.unique(np.concatenate((flights['Origin'].unique(), flights['Dest'].unique())))
    
    time_grouped = (squared_delays
                    .groupby(pd.Grouper(key="dtime", freq="H")))

    adj_mat = xr.DataArray(np.zeros((len(locs), len(locs), len(time_grouped)), dtype=np.single),
                           dims=("Origin", "Dest", "timestamp"),
                           coords={"Origin": locs, 'Dest': locs, 'timestamp': [t for t, _ in time_grouped]})
    
    for timestamp, group in time_grouped:
        for idx, origin, dest, dtime, mean_sqr_delay in group.itertuples():
            adj_mat.loc[{'Origin': origin, 'Dest': dest, 'timestamp': timestamp}] = mean_sqr_delay

    return adj_mat


def adj_mat_to_file(adj_mat: xr.DataArray=None, filepath: str=None) -> None:
    if not filepath:
        filepath = os.path.join(os.path.dir(os.getcwd()), "data", "processed", "flight_ts_graphs")
    os.makedirs(filepath, exist_ok=True)
    amt = adj_mat.transpose('timestamp', ...)
    for hr in amt:
        coo_adj_mat = sp.coo_matrix(hr.values)
        sp.save_npz(os.path.join(filepath, f"file_{hr.timestamp.item()}.npz"), coo_adj_mat, compressed=True)


    for file in files:
    adj_mat_to_file(construct_adj_mat(file))
