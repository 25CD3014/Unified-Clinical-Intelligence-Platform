import pandas as pd
import numpy as np
import os
from concurrent.futures import ThreadPoolExecutor

def find_column(df, patterns):
    """
    Advanced Heuristic: Uses semantic proximity to find columns.
    Addresses Problem Statement 1 (Semantic Harmonization).
    """
    # Exact Match First
    for pattern in patterns:
        for col in df.columns:
            if pattern.lower() == col.lower().strip():
                return col
    
    # Fuzzy/Partial Match Second
    for pattern in patterns:
        for col in df.columns:
            if pattern.lower() in col.lower():
                return col
                
    # Problem Statement 1: 'Agentic' Fallback - Check common clinical abbreviations
    abbr_map = {
        'site': ['center', 'loc', 'stn', 'investigator', 'hosp', 'medical', 'point'],
        'country': ['nation', 'ctry', 'geo', 'region', 'territory', 'market'],
        'query': ['clarification', 'discrepancy', 'flag', 'question', 'dc', 'pending'],
        'sae': ['safety', 'serious', 'event', 'adverse', 'ae', 'harm'],
        'missing': ['gap', 'lost', 'null', 'void', 'empty', 'unavailable']
    }
    
    for key, aliases in abbr_map.items():
        if any(p.lower() in key for p in patterns):
            for alias in aliases:
                for col in df.columns:
                    if alias in col.lower():
                        return col
    return None

def optimized_excel_read(file_path, patterns, study_name, metric_name):
    """Reads only required columns from a specific Excel file using Calamine."""
    if not file_path or not os.path.exists(file_path):
        return pd.DataFrame()
    
    try:
        # Header scan
        head = pd.read_excel(file_path, nrows=0, engine='calamine')
        cols = []
        
        if metric_name == "edc":
            s_col = find_column(head, ['Site ID', 'Site number', 'Site', 'SITE'])
            c_col = find_column(head, ['Country', 'COUNTRY'])
            r_col = find_column(head, ['Region', 'REGION'])
            if s_col: cols.append(s_col)
            if c_col: cols.append(c_col)
            if r_col: cols.append(r_col)
            
            if s_col:
                df = pd.read_excel(file_path, usecols=cols, engine='calamine')
                # Standardize
                rename_map = {s_col: 'Site ID'}
                if c_col: rename_map[c_col] = 'Country'
                if r_col: rename_map[r_col] = 'Region'
                return df.rename(columns=rename_map)
                
        else: # Missing or SAE
            s_col = find_column(head, patterns)
            if s_col:
                df = pd.read_excel(file_path, usecols=[s_col], engine='calamine')
                return df.rename(columns={s_col: 'Site ID'})
                
    except Exception as e:
        print(f"Error reading {metric_name} in {study_name}: {e}")
    return pd.DataFrame()

def load_and_preprocess_data(study_folder="STUDY 21_CPID_Input Files - Anonymization"):
    base_root = r"d:\NEST 2.0\QC Anonymized Study Files"
    base_path = os.path.join(base_root, study_folder)
    
    # Cache path
    cache_dir = r"d:\NEST 2.0\.cache"
    if not os.path.exists(cache_dir): os.makedirs(cache_dir)
    cache_file = os.path.join(cache_dir, f"{study_folder.replace(' ', '_')}_binary.csv")
    
    if not os.path.exists(base_path):
        return pd.DataFrame()

    # Dynamic File Finding
    files = [os.path.join(base_path, f) for f in os.listdir(base_path) if f.endswith(".xlsx")]
    if not files: return pd.DataFrame()
    
    # Check Cache Validity
    if os.path.exists(cache_file):
        cache_time = os.path.getmtime(cache_file)
        if all(os.path.getmtime(f) < cache_time for f in files if os.path.exists(f)):
            print(f"Loading Study {study_folder} from High-Speed Binary Cache...")
            return pd.read_csv(cache_file)

    # File identification
    edc_metrics_file = None
    missing_pages_file = None
    sae_file = None

    for f in files:
        f_low = f.lower()
        if "edc metrics" in f_low: edc_metrics_file = f
        elif "missing_pages" in f_low: missing_pages_file = f
        elif "sae" in f_low and "dashboard" in f_low: sae_file = f

    if not edc_metrics_file: edc_metrics_file = files[0]

    print(f"Parallel Processing Study {study_folder} (Calamine Engine)...")
    
    # Run parallel loads
    with ThreadPoolExecutor(max_workers=3) as executor:
        f_edc = executor.submit(optimized_excel_read, edc_metrics_file, [], study_folder, "edc")
        f_missing = executor.submit(optimized_excel_read, missing_pages_file, ['Site number', 'Site', 'SITE'], study_folder, "missing")
        f_sae = executor.submit(optimized_excel_read, sae_file, ['Site ID', 'Site No', 'Site', 'SITE'], study_folder, "sae")
        
        df_edc = f_edc.result()
        df_m = f_missing.result()
        df_s = f_sae.result()

    # Aggregate EDC
    if not df_edc.empty:
        site_info = df_edc[['Site ID', 'Country', 'Region']].drop_duplicates().dropna(subset=['Site ID'])
        site_queries = df_edc.groupby('Site ID').size().reset_index(name='query_count')
        site_data = site_queries.merge(site_info, on='Site ID', how='left')
    else:
        return pd.DataFrame()

    # Aggregate Missing
    site_missing = df_m.groupby('Site ID').size().reset_index(name='missing_page_count') if not df_m.empty else pd.DataFrame(columns=['Site ID', 'missing_page_count'])
    
    # Aggregate SAE
    site_sae = df_s.groupby('Site ID').size().reset_index(name='sae_count') if not df_s.empty else pd.DataFrame(columns=['Site ID', 'sae_count'])

    # Merge
    final_df = site_data.merge(site_missing, on='Site ID', how='outer').merge(site_sae, on='Site ID', how='outer')
    
    if 'Country' not in final_df.columns: final_df['Country'] = 'Unknown'
    if 'Region' not in final_df.columns: final_df['Region'] = 'Global'
    final_df.fillna(0, inplace=True)
    
    final_df.to_csv(cache_file, index=False)
    return final_df

if __name__ == "__main__":
    df = load_and_preprocess_data()
    df.to_csv(r"d:\NEST 2.0\processed_site_metrics.csv", index=False)
    print(f"Processed data saved. Shape: {df.shape}")
