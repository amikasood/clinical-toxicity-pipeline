import pandas as pd
import numpy as np
import torch
from torch.utils.data import Dataset, DataLoader
import torch.nn as nn
import torch.optim as optim

class ToxicityDataset(Dataset):
    def __init__(self, csv_path):
        df = pd.read_csv(csv_path)
        feature_columns = ['baseline_val', 'peak_val', 'fold_change']
        self.labels = df['Toxicity'].values
        self.features = df[feature_columns].values

    def __len__(self):
        return len(self.labels)

    def __getitem__(self, idx):
        patient_feature = torch.tensor(self.features[idx], dtype=torch.float32)
        patient_label = torch.tensor(self.labels[idx], dtype=torch.float32)
        return patient_feature, patient_label

dataset = ToxicityDataset('data/raw/clinical_data.csv')
loader = DataLoader(dataset, batch_size=10, shuffle=True)

class ToxicityPredictor(nn.Module):
    def __init__(self):
        super().__init__()
        self.layer1 = nn.Linear(in_features=3, out_features=8)
        self.relu = nn.ReLU()
        self.layer2 = nn.Linear(in_features=8, out_features=1)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        x = self.layer1(x)
        x = self.relu(x)
        x = self.layer2(x)
        x = self.sigmoid(x)
        return x

model = ToxicityPredictor()
optimizer = optim.SGD(model.parameters(), lr=0.01)
criterion = nn.BCELoss()

for epoch in range(10):
    for features, labels in loader:
        predictions = model(features) # Forward pass
        loss = criterion(predictions, labels.unsqueeze(1)) # Calculate loss
        optimizer.zero_grad() # Reset gradients
        loss.backward() # Backward pass
        optimizer.step() # Update weights
    print(f"Epoch {epoch+1} | Loss {loss.item()}")

