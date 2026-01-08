# NEST 2.0: Unified Clinical Intelligence Platform

**NEST 2.0 (Next-Generation Efficacy & Safety Tracker)** is an advanced, AI-driven clinical intelligence dashboard designed to solve the critical "Data Silo" problem in modern clinical trials. By replacing fragmented spreadsheets and manual oversight with a unified, automated engine, NEST 2.0 empowers stakeholders to identify risks, validate scientific data, and discover hidden safety patterns in real-time.

---

## 🚀 Key Features & capabilities

### 1. 📊 Operational Intelligence (Risk Monitoring)
Traditional monitoring is reactive. NEST 2.0 is **predictive**.
-   **Anomaly Detection Engine**: Utilizes an **Isolation Forest** machine learning model to automatically score clinical sites based on multivariate risk factors (Query Volume, Missing Pages, SAE Frequency).
-   **Global Risk Heatmap**: A geospatial visualization that aggregates site-level risks to provide a country-level "Risk Index", helping Study Managers allocate resources where they are needed most.
-   **Natural Language Narrative Generator**: Automatically writes draft **Clinical Study Reports (CSR)** regulatory narratives for high-risk sites in **English, Japanese, and Spanish**, significantly reducing medical writing time.

### 2. ⚖️ Mass Balance Engine (Scientific Validation)
Validating drug substance stability is complex. NEST 2.0 instills **mathematical rigor**.
-   **Scientific Calculation Suite**: Computes:
    -   **Simple Mass Balance (SMB)**: The traditional sum (API + Degradants).
    -   **Absolute Mass Balance (AMB)**: Accounts for initial assay variability.
    -   **Relative Mass Balance (RMB)**: A novel metric that isolates the *change* in degradants relative to the *loss* of API.
-   **Validation Simulation**: Runs **Monte-Carlo simulations** on synthetic assay data to mathematically prove that RMB is superior at detecting "invisible gaps" (method sensitivity issues) that SMB misses.
-   **Regulatory Compliance**: ensuring all calculations align with ICH Q1A/Q1B standards for forced degradation studies.

### 3. 🛡️ Safety Signal Intelligence (Agentic Discovery)
Safety signals often hide in unstructured text. NEST 2.0 uses **Agentic AI** to find them.
-   **Cross-Study Signal Detection**: Scans raw Excel/CSV data across multiple studies to track specific safety terms (e.g., "Headache").
-   **Generative Semantic Expansion**: If you search for "Headache", the AI automatically expands the search to include medically relevant synonyms like "Migraine", "Cephalgia", "Head pain", and "Neurological discomfort".
-   **Agentic Pattern Discovery**: "Discovery Mode" runs without user input. It analyzes the entire portfolio to surface the most dominant medical patterns and "Hotspots", alerting safety physicians to emerging trends they didn't know to look for.

---

## ⚙️ Technical Architecture

-   **Frontend**: Built with **Streamlit**, customized with CSS/HTML injection for a premium "Dark Mode" aesthetic.
-   **Data Engine**: Powered by **`python-calamine`** (Rust-based Excel reader) for ultra-fast ingestion of large clinical datasets.
-   **Machine Learning**: **`scikit-learn`** (Isolation Forest) for unsupervised anomaly detection.
-   **Interactive Visualization**: **`plotly.express`** for dynamic, drill-down capable charts and maps.

---

## 🛠️ Installation & Setup

### Prerequisites
-   Python 3.9+ installed on your system.
-   Git (for cloning the repository).

### Step-by-Step Guide

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/25CD3014/Unified-Clinical-Intelligence-Platform.git
    ```

2.  **Install Dependencies**
    We use `requirements.txt` to manage dependencies. Install them cleanly using pip:
    ```bash
    pip install -r requirements.txt
    ```


---

## 📂 Project Structure Explained

-   **`app.py`**: The "Brain" of the application. Handles the UI, navigation, and orchestrates the calls to other modules. Note: Includes global scope path handling for cloud compatibility.
-   **`data_pipeline.py`**: The "Heart". Handles ETL (Extract, Transform, Load) processes. It intelligently merges disparate data sources (EDC, Safety, Missing Data) into a unified dataset.
-   **`train_model.py`**: The "Intelligence". Fetches processed data, trains the anomaly detection model, and saves the scored metrics for the dashboard to consume.
-   **`validation_proofs.py`**: A specialized scientific module containing the logic for the Mass Balance Monte-Carlo simulations.
-   **`requirements.txt`**: List of all necessary Python libraries for deployment.

---

## 👥 Meet the Team 

We are a diverse team of innovators bridging the gap between Data Science and Clinical Operations.

### Core Leadership
-   **Kumkum Gupta** - *Project Lead & System Architect*
    -   Responsible for the overall vision, architecture, and core ML algorithms.

### Development & Engineering
-   **Ayush Pratap Singh** - *Lead Frontend Engineer*
    -   Designed the premium Streamlit UI and interactive visualizations.
### Scientific & Clinical Advisors
-   **Aarsh Patel** - *Clinical Operations Subject Matter Expert*
    -   Provided domain expertise on Risk-Based Monitoring (RBM) and regulatory requirements.

---
*© 2026 NEST 2.0 Clinical Intelligence. All Rights Reserved.*
