from data_pipeline import load_and_preprocess_data
import os

studies = [
    'Study 1_CPID_Input Files - Anonymization', 
    'Study 10_CPID_Input Files - Anonymization', 
    'Study 11_CPID_Input Files - Anonymization'
]

print("--- Data Pipeline Verification ---")
for s in studies:
    try:
        df = load_and_preprocess_data(s)
        if not df.empty:
            print(f"Study: {s} | Status: SUCCESS | Shape: {df.shape}")
        else:
            print(f"Study: {s} | Status: EMPTY DATAFRAME")
    except Exception as e:
        print(f"Study: {s} | Status: CRASHED | Error: {e}")
