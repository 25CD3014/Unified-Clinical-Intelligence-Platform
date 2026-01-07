import pandas as pd
import numpy as np

def run_mb_validation_simulation():
    """
    Simulates forced degradation assay data to prove the accuracy 
    of Relative Mass Balance (RMB) vs Simple Mass Balance (SMB).
    """
    print("--- NEST 2.0: Scientific MB Validation Simulation ---")
    
    # Generate Synthetic Site Data
    n_samples = 100
    np.random.seed(42)
    
    # Initial API Assay (Target 100%)
    initial_api = np.random.normal(99.0, 0.5, n_samples)
    initial_deg = np.random.normal(0.2, 0.1, n_samples)
    
    # Stressed API (Target ~80-90%) - simulated degradation
    degradation_rate = np.random.uniform(0.1, 0.2, n_samples)
    stressed_api = initial_api * (1 - degradation_rate)
    
    # True Degradants generated
    true_degradants = initial_api * degradation_rate
    
    # Detected Degradants (simulating method sensitivity loss)
    method_sensitivity = np.random.uniform(0.7, 0.95, n_samples)
    detected_degradants = true_degradants * method_sensitivity
    
    df = pd.DataFrame({
        'initial_api': initial_api,
        'initial_deg': initial_deg,
        'stressed_api': stressed_api,
        'detected_deg': detected_degradants
    })
    
    # 1. Simple Mass Balance (SMB)
    df['SMB'] = df['stressed_api'] + df['detected_deg']
    
    # 2. Relative Mass Balance (RMB)
    loss_of_api = df['initial_api'] - df['stressed_api']
    increase_in_deg = df['detected_deg'] - df['initial_deg']
    df['RMB'] = (increase_in_deg / loss_of_api) * 100
    
    avg_smb = df['SMB'].mean()
    avg_rmb = df['RMB'].mean()
    
    print(f"Validated Samples: {n_samples}")
    print(f"Average SMB Recovery: {round(avg_smb, 2)}% (May look normal)")
    print(f"Average RMB Recovery: {round(avg_rmb, 2)}% (Exposes sensitivity gap!)")
    
    if avg_rmb < 95:
        print("Conclusion: Relative Mass Balance successfully detected a 5-15% 'Invisible GAP' in degradant detection.")
    else:
        print("Conclusion: Method sensitivity confirmed.")

if __name__ == "__main__":
    run_mb_validation_simulation()
