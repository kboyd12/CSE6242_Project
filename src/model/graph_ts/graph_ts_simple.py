import glob
import os
import sys
import pandas as pd
import numpy as np
import pickle
import torch.nn as nn
import torch.nn.functional as F
from torch_geometric.nn import GCNConv, GatedGraphConv, global_add_pool
import torch
from torch_geometric.data import Dataset, download_url, Data

sys.setrecursionlimit(10_000)

class DelayGraphDataset(Dataset):
    def __init__(self, file_path=os.path.join(os.getcwd(), "data", "processed", "flight_ts_graphs")):
        """
        Args:
            file_path (str): Path to the file containing the data samples.
        """
        self.file_path = file_path
        self.data = []
        
        # Load data from disk

    def process(self, file):
        #files = glob.glob(os.path.join(self.file_path, "*.npz"))
        with open(os.path.join(self.file_path, "columns"), 'rb') as f:
            columns = pickle.load(f)
        #for file_i, file in enumerate(files):    
        read_file = np.load(file)
        print(read_file.files)
        df = pd.DataFrame(data=read_file['data'], columns=columns)

        data = torch.from_numpy(df.to_numpy()).float()
        timestamp = file[-20:]
        torch_data = Data(edge_index=data, pos=timestamp)
        torch.save(torch_data, os.path.join(self.processed_dir, f'data_{timestamp}.pt'))
        return torch_data

                
    @property
    def processed_file_names(self):
        files = glob.glob(os.path.join(self.file_path, "*.pt"))
        return files
    
    @property
    def raw_file_names(self):
        files = glob.glob(os.path.join(self.file_path, "*.npz"))
        return files

    #@property
    def len(self):
        return len(self.raw_file_names)
    
    def __len__(self):
        return len(self.raw_file_names)
    
    def get(self):
        return 42

    def __getitem__(self, index):
        """
        Args:
            index (int): Index of the data sample to retrieve.

        Returns:
            tuple: A tuple containing the data sample and its label (if available).
        """
        self.data = self.raw_file_names
        sample = self.data[index]
        return self.process(sample)

class TimeSeriesConvolutionalGraphModel(nn.Module):
    def __init__(self, in_channels, hidden_channels, out_channels, num_layers, 
                 kernel_size, stride, dropout):
        super().__init__()
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

#delaydata = DelayGraphDataset()

#tscg = TimeSeriesConvolutionalGraphModel()
