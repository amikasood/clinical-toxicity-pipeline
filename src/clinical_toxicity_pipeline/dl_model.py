import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
from sklearn.metrics import average_precision_score, f1_score, PrecisionRecallDisplay
import numpy as np
import matplotlib.pyplot as plt

class ToxicityDataset(Dataset):
    '''Custom Dataset for tabular clinical data'''
    def __init__(self, X, y):
        self.features = X.values
        self.labels = y.values
    
    def __len__(self):
        return len(self.labels)
    
    def __getitem__(self, idx):
        patient_feature = torch.tensor(self.features[idx], dtype=torch.float32)
        patient_label = torch.tensor(self.labels[idx], dtype=torch.float32)
        return patient_feature, patient_label
    
class ToxicityPredictor(nn.Module):
    '''Deep Learning Model for Toxicity Prediction'''
    def __init__(self, input_size):
        super().__init__()
        self.layer_1 = nn.Linear(in_features=input_size, out_features=16)
        self.relu = nn.ReLU()
        self.layer_2 = nn.Linear(in_features=16, out_features=1)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        x = self.layer_1(x)
        x = self.relu(x)
        x = self.layer_2(x)
        x = self.sigmoid(x)
        return x
    
def run_baseline(X_train, y_train, X_test, y_test, epochs=10):
    '''
    Run a baseline deep learning model for toxicity prediction
    Parameters
    ----------
    X : Features matrix 
    y : Target vector
    epochs: Number of epochs to train the model
    '''
    print("Preparing Toxicity model")

    #X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    train_dataset = ToxicityDataset(X_train, y_train)
    train_loader = DataLoader(train_dataset, batch_size=10, shuffle=True)
    num_features = X_train.shape[1]
    
    # Pass the detected number of features to the model
    model = ToxicityPredictor(num_features)
    optimizer = optim.SGD(model.parameters(), lr=0.01)
    criterion = nn.BCELoss()

    print("Training the model...")
    for epoch in range(epochs):
        epoch_loss = 0.0
        for features, labels in train_loader:
            predictions = model(features)
            loss = criterion(predictions, labels.unsqueeze(1))
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            epoch_loss += loss.item()
        print(f"Epoch {epoch+1}/{epochs}, Loss: {epoch_loss/len(train_loader)}")
    
    # Evaluate the model
    model.eval()
    X_test_tensor = torch.tensor(X_test.values, dtype=torch.float32)
    y_test_tensor = torch.tensor(y_test.values, dtype=torch.float32)

    with torch.no_grad():
        test_predictions = model(X_test_tensor)
    
    # Convert the predictions to a numpy array
    test_predictions = test_predictions.numpy().flatten()
    y_pred = (test_predictions >= 0.5).astype(int)
    test_labels = y_test_tensor.numpy().flatten()

    # Calculate the accuracy
    f1 = f1_score(test_labels, y_pred)
    pr_auc = average_precision_score(test_labels, test_predictions)

    print("\nPytorch Baseline Metrics\n")
    print(f"F1-Score:   {f1:.2f}")
    print(f"PR-AUC:     {pr_auc:.2f}")

    # Generate figures
    plt.figure(figsize=(8,6))
    display = PrecisionRecallDisplay.from_predictions(test_labels, test_predictions, name="Pytorch", color="darkorange")
    plt.title(f"Precision-Recall Curve (AUC = {pr_auc:.2f})")
    plt.grid(alpha=0.3)
    plt.savefig('pr_curve_pytorch.png', dpi=300, bbox_inches='tight')
    plt.close()
