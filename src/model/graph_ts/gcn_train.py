import torch
import torch.nn as nn
import torch.optim as optim
from torch_geometric.loader import DataLoader

from graph_ts_simple import DelayGraphDataset, TimeSeriesConvolutionalGraphModel


def train():
    """"
    """
    dataset = DelayGraphDataset()

    # Create a data loader
    loader = DataLoader(dataset, batch_size=32, shuffle=True)

    # Instantiate the model
    num_features = 356
    in_channels = num_features
    hidden_channels = 64
    out_channels = num_features
    kernel_size = 3
    stride = 1
    num_layers = 3
    dropout = 0.1

    model = TimeSeriesConvolutionalGraphModel(in_channels, hidden_channels, out_channels, kernel_size, 
                                              stride, num_layers, dropout)

    # Define the loss function and optimizer
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)

    # Training loop
    num_epochs = 100
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model.to(device)
    model.train()

    for epoch in range(num_epochs):
        for batch in loader:
            batch.to(device)
            optimizer.zero_grad()
            output = model(batch)
            loss = criterion(output, batch.y)
            loss.backward()
            optimizer.step()

        print(f'Epoch [{epoch+1}/{num_epochs}], Loss: {loss.item():.4f}')

    print('Training finished.')

if __name__ == "__main__":
    train()