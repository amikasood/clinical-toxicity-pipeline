import torch
import torch.nn as nn

class ToxicityPredictionModel(nn.Module):
    def __init__(self):
        super().__init__()
        # Input layer takes in two features Baseline ALT and Peak ALT
        # Outputs 8 hidden nodes
        self.input_layer = nn.Linear(in_features=2, out_features=8)

        # Non-linear activation
        self.relu = nn.ReLU()

        # Output layer predicts toxicity (0 or 1)
        # Outputs 1 node
        self.output_layer = nn.Linear(in_features=8, out_features=1)

        #Final activation: sigmoid to ensure output is between 0 and 1
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        x = self.input_layer(x)
        x = self.relu(x)
        x = self.output_layer(x)
        x = self.sigmoid(x)
        return x

model_0 = ToxicityPredictionModel()
print(model_0)
print("Done")

# Setup a Binary Cross Entropy Loss Function
loss_fn = nn.BCELoss()

# Setup an Optimizer (stochastic gradient descent)
optimizer = torch.optim.SGD(model_0.parameters(), lr=0.01)