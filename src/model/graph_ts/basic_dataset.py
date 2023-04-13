import torch
from torch.utils.data import Dataset
import os
import glob
import pandas as pd
import pyarrow.parquet as pq


class MyDataset(Dataset):
    def __init__(self, file_path=os.path.join(os.getcwd(), "data", "raw", "btsdelay")):
        """
        Args:
            file_path (str): Path to the file containing the data samples.
        """
        self.file_path = os.path.join(os.getcwd(), file_path)
        self.data = []
        
        # Load data from disk
        files = glob.glob(os.path.join(self.file_path, "*.parquet"))
        for file_i, file in enumerate(files):    
            parquet_file = pq.ParquetFile(file)
            for batch_i, batch in enumerate(parquet_file.iter_batches()):
                batch_df = batch.to_pandas()
                print("batch_df:", batch_df.shape)
    
                data = torch.from_numpy(batch_df.to_numpy()).float()
                timestamp = file[-20:]
                torch_data = Data(edge_index=data, pos=timestamp)
            torch.save(torch_data, os.path.join(self.processed_dir, f'data_{file_i}{batch_i}.pt'))

                
    def __len__(self):
        return len(self.data)
    
    def __getitem__(self, index):
        """
        Args:
            index (int): Index of the data sample to retrieve.

        Returns:
            tuple: A tuple containing the data sample and its label (if available).
        """
        sample = self.data[index]
        # Assuming the last value in each line is the label
        label = int(sample[-1])
        # Convert data values to torch tensors (if needed)
        data = torch.tensor([float(val) for val in sample[:-1]])
        return data, label

mydataset = MyDataset()
data_loader = torch.utils.data.DataLoader(mydataset, batch_size=2,
                                          #num_samples=2,
                                          shuffle=True, num_workers=2)
