import os
import pandas as pd
import joblib

base_dir = r"d:\NEST 2.0\QC Anonymized Study Files"

def get_all_safety_files(root_dir):
    keywords = ["coding", "medra", "meddra", "whodd", "whodrug", "sae", "dashboard", "safety"]
    files_found = []
    print(f"Scanning {root_dir}...")
    for root, dirs, files in os.walk(root_dir):
        if ".cache" in root: continue
        for f in files:
            f_low = f.lower().replace("_", " ")
            if any(kw in f_low for kw in keywords) and f.endswith(".xlsx"):
                files_found.append(os.path.join(root, f))
    return files_found

files = get_all_safety_files(base_dir)
print(f"Found {len(files)} safety files.")
for f in files[:5]:
    print(f" - {f}")

query = "Headache"
semantic_map = {
    "headache": ["migraine", "cephalgia", "head pain", "nervous system"],
}
expanded = [query.lower()]
for k, v in semantic_map.items():
    if k in query.lower(): expanded.extend(v)

print(f"Searching for: {expanded}")

def search_in_file(file_path, queries):
    try:
        # Use calamine for high-speed scanning
        df_tmp = pd.read_excel(file_path, nrows=1000, engine='calamine')
        
        # Semantic logic: Mask across all columns for ANY of the expanded queries
        mask = pd.Series([False] * len(df_tmp))
        for q in queries:
            mask |= df_tmp.astype(str).apply(lambda x: x.str.contains(q, case=False)).any(axis=1)
        
        matches = df_tmp[mask].copy()
        for c in matches.columns:
            matches[c] = matches[c].astype(str) # Force string for debug printing
            
        if not matches.empty:
            print(f"MATCH FOUND in {os.path.basename(file_path)}")
            print(matches.head(1).to_string())
            return True
    except Exception as e:
        print(f"ERROR processing {os.path.basename(file_path)}: {e}")
    return False

found_any = False
for f in files[:10]: # Test first 10
    if search_in_file(f, expanded):
        found_any = True

if not found_any:
    print("NO MATCHES FOUND in first 10 files.")
