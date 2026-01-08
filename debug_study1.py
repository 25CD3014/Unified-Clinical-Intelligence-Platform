from data_pipeline import load_and_preprocess_data, optimized_excel_read, find_column
import pandas as pd
import os

study = 'Study 1_CPID_Input Files - Anonymization'
base_root = r"d:\NEST 2.0\QC Anonymized Study Files"
base_path = os.path.join(base_root, study)

files = [os.path.join(base_path, f) for f in os.listdir(base_path) if f.endswith(".xlsx")]
edc = None
for f in files:
    if "edc metrics" in f.lower(): edc = f

print(f"EDC File: {edc}")
if edc:
    df_edc = optimized_excel_read(edc, [], study, "edc")
    print(f"EDC DF Shape: {df_edc.shape}")
    if not df_edc.empty:
        print("EDC Cols:", df_edc.columns.tolist())
        print(df_edc.head())
    
    # Check aggregation
    available_cols = [c for c in ['Site ID', 'Country', 'Region'] if c in df_edc.columns]
    print(f"Available Cols: {available_cols}")
    site_info = df_edc[available_cols].drop_duplicates().dropna(subset=['Site ID'])
    print(f"Site Info Shape: {site_info.shape}")
    
    site_queries = df_edc.groupby('Site ID').size().reset_index(name='query_count')
    print(f"Site Queries Shape: {site_queries.shape}")

    final = load_and_preprocess_data(study)
    print(f"Final Data Pipeline Result Shape: {final.shape}")
