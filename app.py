import torch
import numpy as np
from src.data_ingestion import generate_ran_telemetry
from src.model import RANResourcePredictor
from src.orchestrator import PredictiveOrchestrator

def main():
    """
    Main entry point for the AI-Driven Predictive Resource Orchestrator.
    Executes a complete simulation loop.
    """
    print("--- [ Predictive Cloud-RAN Orchestrator: Simulation Start ] ---")
    
    # 1. Generate RAN Telemetry Metrics
    df = generate_ran_telemetry()
    print(f"Generated {len(df)} data points from Cloud-RAN telemetry.")
    
    # 2. Setup AI Model for Prediction
    model = RANResourcePredictor(input_size=3, hidden_size=64, output_size=1)
    # Using mock weights for demonstration purposes
    print("Initialized LSTM Predictive Model.")
    
    # 3. Simulate Prediction for Next Time Step (using last 10 points)
    last_10_points = df[['cpu_usage', 'memory_usage', 'throughput_mbps']].tail(10).values
    input_tensor = torch.FloatTensor(last_10_points).unsqueeze(0) # [1, 10, 3] batch, seq, feat
    
    with torch.no_grad():
        predicted_cpu_raw = model(input_tensor).item()
        # Scale to a realistic CPU percentage for demo
        predicted_cpu = abs(predicted_cpu_raw * 100) % 100 
        
    # 4. Proactive Orchestration Decision
    orchestrator = PredictiveOrchestrator()
    scaling_action = orchestrator.evaluate_scaling(predicted_cpu)
    
    # 5. Output Results
    report = orchestrator.generate_report(df['cpu_usage'].iloc[-1], predicted_cpu, scaling_action)
    
    print("\n--- [ Decision Report ] ---")
    for key, value in report.items():
        print(f"{key:25}: {value}")
    print("\n--- [ Simulation End ] ---")

if __name__ == "__main__":
    main()
