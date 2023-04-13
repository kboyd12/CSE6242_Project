import torch.nn as nn
import torch.nn.functional as F
from torch_geometric.nn import GCNConv, GatedGraphConv, global_add_pool

import glob
import os
import sys
import pandas as pd

import torch
from torch_geometric.data import Dataset, download_url, Data

sys.setrecursionlimit(10_000)

class FlightsDataset(Dataset):
    def __init__(self, root, transform=None, pre_transform=None, pre_filter=None,
                 raw_paths: str="../../data/raw/btsdelay/",
                 processed_dir: str="../../data/processed/btsdelay_torch_adjm/"):
        super().__init__(root, transform, pre_transform, pre_filter)
        self.raw_paths = raw_paths
        self.processed_dir = processed_dir

    @property
    def raw_file_names(self):
        files = glob.glob(f"{self.raw_paths}*.parquet")
        return files

    @property
    def processed_file_names(self):
        return glob.glob(f"{self.processed_dir}*.npz")
    
    def process(self):
        for idx, file in enumerate(self.raw_paths):
            # Read data from `raw_paths`.
            df = pd.read_parquet(file)
            data = torch.from_numpy(df.to_numpy()).float()

            timestamp = file[-20:]
            torch_data = Data(edge_index=data, pos=timestamp)

            torch.save(torch_data, os.path.join(self.processed_dir, f'data_{idx}.pt'))

    def len(self):
        return len(self.processed_file_names)

    def get(self, idx):
        data = torch.load(os.path.join(self.processed_dir, f'data_{idx}.pt'))
        return data



class TimeSeriesConvolutionalGraphModel(nn.Module):
    def __init__(self, in_channels, hidden_channels, out_channels, num_layers):
        super(self).__init__()
        self.num_layers = num_layers
        self.conv_layers = nn.ModuleList()
        self.pool_layers = nn.ModuleList()

        # Define the graph convolutional layers
        for i in range(num_layers):
            if i == 0:
                self.conv_layers.append(GCNConv(in_channels, hidden_channels))
            else:
                self.conv_layers.append(GCNConv(hidden_channels, hidden_channels))
            self.pool_layers.append(nn.MaxPool2d(2, 2))

        # Define the fully connected layers
        self.fc_layers = nn.ModuleList()
        for i in range(num_layers):
            self.fc_layers.append(nn.Linear(hidden_channels, out_channels))

    def forward(self, data):
        x, edge_index, batch = data.x, data.edge_index, data.batch

        for i in range(self.num_layers):
            x = self.conv_layers[i](x, edge_index)
            x = F.relu(x)
            x = self.pool_layers[i](x)

        x = global_add_pool(x, batch)
        for i in range(self.num_layers):
            x = self.fc_layers[i](x)
            x = F.relu(x)

        return x

data = FlightsDataset(root="./data/raw/btsdelay", download=False)
data