import numpy as np
import pandas as pd

def generate_ran_telemetry(steps=1000):
    """
    Simulates Cloud RAN gNB telemetry metrics.
    Metrics: CPU Usage, Memory Usage, Throughput, and Latency.
    """
    np.random.seed(42)
    time = np.arange(steps)
    
    # Base load with daily seasonality
    seasonal_load = 50 + 20 * np.sin(2 * np.pi * time / 100)
    
    # Add random noise and spikes
    cpu_usage = seasonal_load + np.random.normal(0, 5, steps)
    memory_usage = 40 + 10 * np.sin(2 * np.pi * time / 100) + np.random.normal(0, 2, steps)
    throughput = 100 + 50 * np.sin(2 * np.pi * time / 100) + np.random.normal(0, 10, steps)
    
    data = pd.DataFrame({
        'timestamp': time,
        'cpu_usage': np.clip(cpu_usage, 0, 100),
        'memory_usage': np.clip(memory_usage, 0, 100),
        'throughput_mbps': np.clip(throughput, 0, 500)
    })
    
    return data

if __name__ == "__main__":
    df = generate_ran_telemetry()
    print(df.head())
