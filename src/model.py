import torch
import torch.nn as nn

class RANResourcePredictor(nn.Module):
    """
    LSTM-based model for predicting future Cloud RAN resource requirements.
    Input: Historical telemetry metrics (CPU, Memory, Throughput).
    Output: Predicted metrics for the next time step.
    """
    def __init__(self, input_size=3, hidden_size=64, num_layers=2, output_size=1):
        super(RANResourcePredictor, self).__init__()
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        
        # LSTM Layer
        self.lstm = nn.LSTM(input_size, hidden_size, num_layers, batch_first=True, dropout=0.2)
        
        # Fully connected layer
        self.fc = nn.Linear(hidden_size, output_size)
        
    def forward(self, x):
        # Initialize hidden state and cell state
        h0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size).to(x.device)
        c0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size).to(x.device)
        
        # Forward propagate LSTM
        out, _ = self.lstm(x, (h0, c0))
        
        # Decode the hidden state of the last time step
        out = self.fc(out[:, -1, :])
        return out

if __name__ == "__main__":
    # Test model with dummy input
    model = RANResourcePredictor()
    dummy_input = torch.randn(32, 10, 3) # Batch size 32, Sequence length 10, Input features 3
    output = model(dummy_input)
    print(f"Output shape: {output.shape}")
