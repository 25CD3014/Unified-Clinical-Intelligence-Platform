import pandas as pd
import os

def inspect_excel(file_path):
    print(f"\n--- Inspecting: {os.path.basename(file_path)} ---")
    try:
        # Read only headers and first few rows to save time
        df = pd.read_excel(file_path, nrows=5)
        print(f"Columns: {df.columns.tolist()}")
        print(f"Head:\n{df.head(2)}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    base_path = r"d:\NEST 2.0\QC Anonymized Study Files\STUDY 21_CPID_Input Files - Anonymization"
    files = [
        "CPID_EDC Metrics_URSV2.0 (1) 1_updated.xlsx",
        "SAE Dashboard_Standard Metrics Input file template V1.0_updated.xlsx (1) (2)_updated.xlsx",
        "Missing LNR_Standard Metrics Input File template V1.0_updated.xlsx (1) 3_updated.xlsx"
    ]
    for f in files:
        inspect_excel(os.path.join(base_path, f))
