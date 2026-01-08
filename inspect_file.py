import pandas as pd
import os

# Pick one of the files found in the previous step
target_file = r"d:\NEST 2.0\QC Anonymized Study Files\STUDY 20__CPID_Input Files - Anonymization\GlobalCodingReport MedDRA_updated.xlsx"

print(f"Inspecting: {target_file}")

try:
    df = pd.read_excel(target_file, nrows=20, engine='calamine')
    print("Columns:", df.columns.tolist())
    print("First 5 rows:")
    print(df.head(5).to_string())
    
    # Check simple contains
    term = "Headache"
    mask = df.astype(str).apply(lambda x: x.str.contains(term, case=False)).any(axis=1)
    if mask.any():
        print(f"DIRECT MATCH FOUND for {term}")
    else:
        print(f"No direct match for {term} in first 20 rows.")
        
except Exception as e:
    print(f"Error reading file: {e}")
