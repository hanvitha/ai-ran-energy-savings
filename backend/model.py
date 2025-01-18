import warnings
import os
warnings.filterwarnings("ignore")
from copy import deepcopy as dc
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from fastapi import HTTPException

from datetime import datetime, timedelta
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader

from prometheus_api_client import PrometheusConnect, MetricsList, MetricSnapshotDataFrame
from prometheus_api_client.utils import parse_datetime

dir_path = os.path.dirname(os.path.realpath(__file__))

PROM_URL = os.environ.get('PROM_URL')
PROM_ACCESS_TOKEN = os.environ.get('PROM_ACCESS_TOKEN')

class LSTM(nn.Module):
    def __init__(self, input_size, hidden_size, num_stacked_layers):
        super().__init__()
        self.hidden_size = hidden_size
        self.num_stacked_layers = num_stacked_layers

        self.lstm = nn.LSTM(input_size, hidden_size, num_stacked_layers, 
                            batch_first=True)
        
        self.fc = nn.Linear(hidden_size, 1)

    def forward(self, x):
        batch_size = x.size(0)
        h0 = torch.zeros(self.num_stacked_layers, batch_size, self.hidden_size).to("cpu")
        c0 = torch.zeros(self.num_stacked_layers, batch_size, self.hidden_size).to("cpu")
        
        out, _ = self.lstm(x, (h0, c0))
        out = self.fc(out[:, -1, :])
        return out


def train_one_epoch(model,epoch,train_loader, loss_function,optimizer):
    model.train(True)
    
    running_loss = 0.0

    for batch_index, batch in enumerate(train_loader):
        x_batch, y_batch = batch[0].to("cpu"), batch[1].to("cpu")

        output = model(x_batch)
        loss = loss_function(output, y_batch)
        running_loss += loss.item()

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        if batch_index % 100 == 99:  # print every 100 batches
            avg_loss_across_batches = running_loss / 100
            # print('Batch {0}, Loss: {1:.3f}'.format(batch_index+1, avg_loss_across_batches))
            running_loss = 0.0
   

def validate_one_epoch(model,test_loader,loss_function,optimizer):
    model.train(False)
    running_loss = 0.0

    for batch_index, batch in enumerate(test_loader):
        x_batch, y_batch = batch[0].to("cpu"), batch[1].to("cpu")

        with torch.no_grad():
            output = model(x_batch)
            loss = loss_function(output, y_batch)
            running_loss += loss.item()

    avg_loss_across_batches = running_loss / len(test_loader)

    print('Val Loss: {0:.3f}'.format(avg_loss_across_batches))
    

class TimeSeriesDataset(Dataset):
    def __init__(self, X, y):
        self.X = X
        self.y = y

    def __len__(self):
        return len(self.X)

    def __getitem__(self, i):
        return self.X[i], self.y[i]

def prepare_dataframe_for_lstm(df, n_steps):
    df = dc(df)
    
    df.set_index('timestamp', inplace=True)
    
    for i in range(1, n_steps+1):
        df[f'Close(t-{i})'] = df['value'].shift(i)
        
    df.dropna(inplace=True)
    
    return df


def buildModel(metrics):
    try:
        data = metrics[['timestamp', 'value']]
        lookback = 4
        shifted_df = prepare_dataframe_for_lstm(data, lookback)
        shifted_df_as_np = shifted_df.to_numpy()
        
        
        shifted_df_as_np.shape
        np.save(os.path.join(dir_path+'/data'), shifted_df_as_np)
        shifted_df_as_np = np.load(dir_path+"/data.npy")
        scaler = MinMaxScaler(feature_range=(-1, 1))
        shifted_df_as_np = scaler.fit_transform(shifted_df_as_np)

        X = shifted_df_as_np[:, 1:]
        y = shifted_df_as_np[:, 0]
        X = dc(np.flip(X, axis=1))
        split_index = int(len(X) * 0.75)
        X_train = X[:split_index]
        X_test = X[split_index:]

        y_train = y[:split_index]
        y_test = y[split_index:]

        X_train = X_train.reshape((-1, lookback, 1))
        X_test = X_test.reshape((-1, lookback, 1))

        y_train = y_train.reshape((-1, 1))
        y_test = y_test.reshape((-1, 1))

        X_train = torch.tensor(X_train).float()
        y_train = torch.tensor(y_train).float()
        X_test = torch.tensor(X_test).float()
        y_test = torch.tensor(y_test).float()

        X_train.shape, X_test.shape, y_train.shape, y_test.shape
        train_dataset = TimeSeriesDataset(X_train, y_train)
        test_dataset = TimeSeriesDataset(X_test, y_test)
        batch_size = 40

        train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
        test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False)
        for _, batch in enumerate(train_loader):
            x_batch, y_batch = batch[0].to("cpu"), batch[1].to("cpu")
            break

        model = LSTM(1, 4, 1)
        # model.to("cpu")

        # learning_rate = 0.1
        # num_epochs = 120
        # loss_function = nn.MSELoss()
        # optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

        # for epoch in range(num_epochs):
        #     train_one_epoch(model,epoch,train_loader,loss_function,optimizer)
        #     validate_one_epoch(model,test_loader,loss_function,optimizer)
        # torch.save(model.state_dict(), os.path.join(dir_path+"/metrics-model.pt"))
        print("model saved")
        
        
        with torch.no_grad():
            predictions = model(X_train.to("cpu")).to('cpu').numpy()

        # plt.plot(y_train, label='Actual Value')
        # plt.plot(predictions, label='Predicted Value')
        # plt.xlabel('Time')
        # plt.ylabel('Value')
        # plt.legend()
        # plt.show()
        # print(predictions)
        return model,predictions

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error querying Prometheus: {e}")

