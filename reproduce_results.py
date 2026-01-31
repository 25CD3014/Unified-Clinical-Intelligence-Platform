import os
import sys
import pandas as pd
from data_pipeline import load_and_preprocess_data
from train_model import train_custom_model
from validation_proofs import run_mb_validation_simulation

def main():
    print("=== NEST 2.0: Automated Reproducibility Suite ===")
    
    # 1. Clean previous results
    files_to_clean = ["processed_site_metrics.csv", "scored_site_metrics.csv", "anomaly_model.joblib"]
    for f in files_to_clean:
        if os.path.exists(f):
            os.remove(f)
            print(f"Cleaned: {f}")

    # 2. Run Data Pipeline (ETL)
    print("\n[1/3] Running Data Pipeline...")
    # Using a default study folder for the reproduction demonstration
    try:
        df = load_and_preprocess_data("STUDY 21_CPID_Input Files - Anonymization")
        df.to_csv("processed_site_metrics.csv", index=False)
        print(f"Success: Data pipeline processed {len(df)} site records.")
    except Exception as e:
        print(f"Error in Data Pipeline: {e}")
        return

    # 3. Train ML Model
    print("\n[2/3] Training Anomaly Detection Model...")
    try:
        train_custom_model()
        print("Success: Isolation Forest trained and sites scored.")
    except Exception as e:
        print(f"Error in Model Training: {e}")
        return

    # 4. Run Scientific Validation Simulation
    print("\n[3/3] Running Scientific MB Validation...")
    try:
        run_mb_validation_simulation()
        print("Success: Mass Balance proofs generated.")
    except Exception as e:
        print(f"Error in Scientific Validation: {e}")
        return

    print("\n=== REPRODUCTION COMPLETE ===")
    print("You can now run 'streamlit run app.py' to view the results in the dashboard.")

if __name__ == "__main__":
    main()
