import torch
from torch.utils.data import Dataset
import os
import glob
import pandas as pd
import numpy as np
from torch_geometric.data import Dataset, download_url, Data
import pickle

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
        print(processing)
        #files = glob.glob(os.path.join(self.file_path, "*.npz"))
        with open(os.path.join(self.file_path, "columns"), 'rb') as f:
            columns = pickle.load(f)
        #for file_i, file in enumerate(files):    
        read_file = np.load(file)
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

mydataset = DelayGraphDataset()
data_loader = torch.utils.data.DataLoader(mydataset, batch_size=2,
                                          shuffle=True, num_workers=2)
print(data_loader)