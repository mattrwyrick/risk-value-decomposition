import pywt
import torch
import torch.nn as nn
import torch.optim as optim
import pandas as pd
import numpy as np
from torch.utils.data import DataLoader, Dataset


# Custom Dataset to handle the time series data
class TimeSeriesDataset(Dataset):
    def __init__(self, X, y):
        self.X = X
        self.y = y

    def __len__(self):
        return len(self.y)

    def __getitem__(self, idx):
        return self.X[idx], self.y[idx]


# Helper function to perform wavelet decomposition
def wavelet_transform(x, wavelet_name='db1', level=3):
    coeffs = pywt.wavedec(x, wavelet_name, level=level)
    return np.concatenate(coeffs)  # Concatenate approximation and detail coefficients


# Kolmogorov-Arnold Network with Wavelet Transforms and Contribution Tracking
class WaveletKAN(nn.Module):
    def __init__(self, target_series, exogenous_vars_df, hidden_size, wavelet_level=3, wavelet_name='db1',
                 learning_rate=0.001):
        super(WaveletKAN, self).__init__()

        # Convert target series and exogenous variables to tensors
        self.target_series = torch.tensor(target_series.values, dtype=torch.float32)
        self.exogenous_vars = torch.tensor(exogenous_vars_df.values, dtype=torch.float32)
        self.input_size = exogenous_vars_df.shape[1]

        # Store wavelet settings
        self.wavelet_level = wavelet_level
        self.wavelet_name = wavelet_name

        # Univariate transformations (psi functions after wavelet decomposition)
        self.psi_layers = nn.ModuleList([nn.Linear((wavelet_level + 1), hidden_size) for _ in range(self.input_size)])

        # Summing the outputs from psi_layers
        self.sum_layer = nn.Linear(hidden_size * self.input_size, hidden_size)

        # Univariate transformations (phi functions after summation)
        self.phi_layer = nn.Linear(hidden_size, 1)

        # Optimizer and loss function
        self.learning_rate = learning_rate
        self.optimizer = optim.Adam(self.parameters(), lr=self.learning_rate)
        self.criterion = nn.MSELoss()

    def forward(self, x):
        # Apply wavelet transform to each input variable (column)
        wavelet_transformed = []
        for i in range(x.shape[1]):  # Iterate over input variables
            wavelet_coeffs = np.apply_along_axis(lambda y: wavelet_transform(y, self.wavelet_name, self.wavelet_level),
                                                 0, x[:, i:i + 1].detach().cpu().numpy())
            wavelet_transformed.append(torch.tensor(wavelet_coeffs, dtype=torch.float32).to(x.device))

        # Apply univariate psi transformations (after wavelet)
        psi_outputs = [torch.relu(psi_layer(wavelet_transformed[i])) for i, psi_layer in enumerate(self.psi_layers)]

        # Concatenate psi outputs and sum them
        psi_outputs_concat = torch.cat(psi_outputs, dim=1)
        summed_output = self.sum_layer(psi_outputs_concat)

        # Apply final univariate transformation (phi function)
        output = self.phi_layer(summed_output)

        return output, psi_outputs  # Return both the final output and psi outputs for contribution analysis

    def fit(self, epochs=100, batch_size=32):
        # Create DataLoader for batching
        dataset = TimeSeriesDataset(self.exogenous_vars, self.target_series)
        dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True)

        for epoch in range(epochs):
            running_loss = 0.0

            for i, (inputs, labels) in enumerate(dataloader):
                # Zero the parameter gradients
                self.optimizer.zero_grad()

                # Forward pass
                outputs, _ = self.forward(inputs)
                loss = self.criterion(outputs, labels)

                # Backward pass and optimize
                loss.backward()
                self.optimizer.step()

                running_loss += loss.item()

            # Print average loss for the epoch
            avg_loss = running_loss / len(dataloader)
            print(f"Epoch [{epoch + 1}/{epochs}], Loss: {avg_loss:.4f}")

    def predict(self, exogenous_vars_df):
        # Convert the new exogenous variables to tensor
        exogenous_vars = torch.tensor(exogenous_vars_df.values, dtype=torch.float32)

        # Forward pass for prediction
        with torch.no_grad():
            predictions, _ = self.forward(exogenous_vars)

        return predictions.numpy()

    def get_contributions(self, exogenous_vars_df):
        # Convert exogenous variables to tensor
        exogenous_vars = torch.tensor(exogenous_vars_df.values, dtype=torch.float32)

        # Get the forward pass and retrieve psi outputs
        with torch.no_grad():
            _, psi_outputs = self.forward(exogenous_vars)

        # Calculate the absolute sum of psi outputs for each variable to determine their contribution
        contributions = [torch.sum(torch.abs(psi_output), dim=0).item() for psi_output in psi_outputs]

        # Normalize contributions to get proportions
        total_contribution = sum(contributions)
        normalized_contributions = [contrib / total_contribution for contrib in contributions]

        return normalized_contributions  # Returns the proportionate contribution of each exogenous variable


# Example usage
if __name__ == "__main__":
    # Generate example target time series (e.g., stock price) and exogenous variables (e.g., interest rates, volatility)
    np.random.seed(42)
    target_series = pd.Series(np.random.randn(500))  # Example stock prices
    exogenous_vars_df = pd.DataFrame({
        'Interest_Rate_5Y': np.random.randn(500),
        'Interest_Rate_10Y': np.random.randn(500),
        'Market_Volatility': np.random.randn(500)
    })

    # Initialize the model with the target and exogenous variables
    hidden_size = 10
    model = WaveletKAN(target_series, exogenous_vars_df, hidden_size, wavelet_level=3)

    # Fit the model
    model.fit(epochs=10, batch_size=32)

    # Predict on new exogenous data (could be future values)
    new_exogenous_vars_df = pd.DataFrame({
        'Interest_Rate_5Y': np.random.randn(10),
        'Interest_Rate_10Y': np.random.randn(10),
        'Market_Volatility': np.random.randn(10)
    })

    predictions = model.predict(new_exogenous_vars_df)
    print("Predictions:", predictions)

    # Get the contribution proportions of each exogenous variable
    contributions = model.get_contributions(new_exogenous_vars_df)
    print("Exogenous Variable Contributions:", contributions)
