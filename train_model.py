import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
import joblib
import os

def train_custom_model():
    csv_path = r"d:\NEST 2.0\processed_site_metrics.csv"
    if not os.path.exists(csv_path):
        print(f"Error: {csv_path} not found. Run the data pipeline first.")
        return

    df = pd.read_csv(csv_path)
    # Features for the model: query_count, missing_page_count, sae_count
    X = df[['query_count', 'missing_page_count', 'sae_count']]
    
    print("Training Isolation Forest for Anomaly Detection...")
    # contamination is the expected proportion of outliers (sites with unusual bottlenecks)
    model = IsolationForest(contamination=0.1, random_state=42)
    model.fit(X)
    
    # Save the model
    model_path = r"d:\NEST 2.0\anomaly_model.joblib"
    joblib.dump(model, model_path)
    print(f"Model saved to {model_path}")
    
    # Predict and add scores to the dataframe for dashboard use
    df['anomaly_score'] = model.decision_function(X)
    df['is_anomaly'] = model.predict(X) # -1 for anomaly, 1 for normal
    
    output_path = r"d:\NEST 2.0\scored_site_metrics.csv"
    df.to_csv(output_path, index=False)
    print(f"Scored metrics saved to {output_path}")

if __name__ == "__main__":
    train_custom_model()
