# NEST 2.0: Unified Clinical Intelligence Platform

**NEST 2.0 (Next-Generation Efficacy & Safety Tracker)** is an advanced, AI-driven clinical intelligence dashboard designed to solve the critical "Data Silo" problem in modern clinical trials. By replacing fragmented spreadsheets and manual oversight with a unified, automated engine, NEST 2.0 empowers stakeholders to identify risks, validate scientific data, and discover hidden safety patterns in real-time.

Deployed Link : https://uciplatform.streamlit.app/ (Live rn)

---

## 🚀 Key Features & capabilities

### 1. 📊 Operational Intelligence (Risk Monitoring)
Traditional monitoring is reactive. NEST 2.0 is **predictive**.
-   **Anomaly Detection Engine**: Utilizes an **Isolation Forest** machine learning model to automatically score clinical sites based on multivariate risk factors.
-   **Global Risk Heatmap**: A professional **Choropleth Geospatial Visualization** that maps site-level risks to provide an immediate global "Risk Index" for executive oversight.
-   **Interactive Data Management**: Employs **AgGrid** for Excel-like filtering, sorting, and deep-dive analysis of clinical site metrics directly in the browser.
-   **Professional Report Export**: A built-in **PDF Narrative Generator** that allows users to export AI-generated clinical study narratives into formatted, regulatory-ready documents.
-   **Natural Language Narrative Generator**: Automatically writes draft **Clinical Study Reports (CSR)** regulatory narratives for high-risk sites in **English, Japanese, and Spanish**.

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

## 📈 Technical Assessment & Roadmap

### **Overall Rating: 9.0/10**

#### **Core Strengths**
*   **Performance Optimization:** Leverages `python-calamine` (Rust-based) and `ThreadPoolExecutor` for ultra-fast ingestion of massive clinical datasets.
*   **Scientific Rigor:** Integrates **Relative Mass Balance (RMB)** and Monte-Carlo simulations for regulatory-grade validation.
*   **Professional Reporting:** Features a high-fidelity **PDF Export Engine** for instant generation of Clinical Study Reports (CSR).
*   **Advanced UI/UX:** Utilizes **AgGrid** for complex data manipulation and **Choropleth Maps** for global risk visualization.
*   **Semantic Harmonization:** Heuristic-based column mapping effectively resolves inconsistent data structures across disparate clinical sites.

#### **Future Roadmap (Areas for Improvement)**
*   **Testing Suite:** Implement a formal unit testing framework (e.g., `pytest`) to ensure the reliability of the core ETL and scientific calculation logic.
*   **Enterprise Logging:** Transition from basic text-based logging to a structured, leveled logging system (e.g., `loguru`) for better production traceability.
*   **Data Persistence:** Migrate from a file-based workflow to a persistent relational database (e.g., PostgreSQL with SQLAlchemy) to support enterprise-level scalability.

---

## 👥 Meet the Team 

**Team 23ce3065**

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
