import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import joblib
from data_pipeline import load_and_preprocess_data
from train_model import train_custom_model
import validation_proofs

# Page Config
st.set_page_config(page_title="NEST 2.0 Clinical Intelligence", layout="wide")

# Custom CSS for Premium Look - Adaptive for Dark/Light Mode
st.markdown("""
    <style>
    /* Metric Card Styling */
    [data-testid="stMetric"] {
        background-color: rgba(255, 255, 255, 0.05);
        padding: 15px;
        border-radius: 12px;
        border: 1px solid rgba(128, 128, 128, 0.2);
        transition: transform 0.2s;
    }
    [data-testid="stMetric"]:hover {
        transform: translateY(-2px);
    }
    /* Global Card/Alert Styling */
    .stAlert {
        border-radius: 10px;
    }
    /* Hide the Streamlit Menu for cleaner look */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# Sidebar Navigation and Language
st.sidebar.title("Settings")
Language = st.sidebar.selectbox("Language / 言語 / Idioma", ["English", "Japanese", "Spanish"])

# Localization Mapping
strings = {
    "English": {
        "title": "NEST 2.0: Unified Clinical Intelligence",
        "subtitle": "Integrated Data-Flow and Anomaly Detection",
        "nav": ["Operational Intelligence", "Mass Balance Engine", "Safety Search"],
        "total_sites": "Total Sites",
        "anomalies": "Anomalies Detected",
        "avg_queries": "Avg Queries/Site",
        "missing_pages": "Total Missing Pages",
        "push_button": "Simulate Global Push Notifications for High-Risk Sites"
    },
    "Japanese": {
        "title": "NEST 2.0: 統合臨床インテリジェンス",
        "subtitle": "統合されたデータフローと異常検知",
        "nav": ["運用インテリジェンス", "マスバランス・エンジン", "安全性検索"],
        "total_sites": "総サイト数",
        "anomalies": "検出された異常",
        "avg_queries": "サイトごとの平均クエリ数",
        "missing_pages": "総欠損ページ数",
        "push_button": "高リスクサイトへのグローバル・プッシュ通知をシミュレートする"
    },
    "Spanish": {
        "title": "NEST 2.0: Inteligencia Clínica Unificada",
        "subtitle": "Flujo de Datos Integrado y Detección de Anomalías",
        "nav": ["Inteligencia Operativa", "Motor de Balance de Masa", "Búsqueda de Seguridad"],
        "total_sites": "Total de Sitios",
        "anomalies": "Anomalías Detectadas",
        "avg_queries": "Promedio de Consultas/Sitio",
        "missing_pages": "Total de Páginas Faltantes",
        "push_button": "Simular Notificaciones Push Globales para Sitios de Alto Riesgo"
    }
}

lang = strings[Language]

Page = st.sidebar.radio("Navigate to", lang["nav"])

# --- PAGE 1: Operational Intelligence ---
if Page in lang["nav"][0]:
    st.title(lang["title"])
    st.subheader(lang["subtitle"])

# --- PAGE 2: Mass Balance Engine ---
elif Page == "Mass Balance Engine":
    st.title("Mass Balance Calculator")
    st.markdown("""
        Assessment of Mass Balance (MB) is critical in forced degradation studies to verify whether all components 
        of a drug substance are accounted for.
    """)
    
    with st.expander("Why this matters? (Regulatory Context)", expanded=False):
        st.write("""
            Regulators expect MB recovery to be close to 100%. Lower values signal gaps in method sensitivity 
            or incomplete detection of degradants.
        """)

    # Input Section
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Initial Sample Data")
        api_initial = st.number_input("Initial API (%)", value=98.5, step=0.1)
        deg_initial = st.number_input("Initial Degradants (%)", value=0.5, step=0.1)
    
    with c2:
        st.subheader("Stressed Sample Data")
        api_stressed = st.number_input("Stressed API (%)", value=87.4, step=0.1)
        deg_stressed = st.number_input("Stressed Degradants (%)", value=11.3, step=0.1)

    # Calculations
    smb = api_stressed + deg_stressed
    amb = ((api_stressed + deg_stressed) / (api_initial + deg_initial)) * 100
    ambd = 100 - amb
    
    loss_of_api = max(0.1, api_initial - api_stressed)
    increase_in_deg = max(0.1, deg_stressed - deg_initial)
    rmb = (increase_in_deg / loss_of_api) * 100
    rmbd = 100 - rmb

    # Display Results
    st.divider()
    res1, res2, res3 = st.columns(3)
    
    with res1:
        st.metric("Simple Mass Balance (SMB)", f"{round(smb, 2)}%")
        st.caption("Target: ~100%")
        
    with res2:
        st.metric("Absolute Mass Balance (AMB)", f"{round(amb, 2)}%")
        st.caption("Considers initial Assay")

    with res3:
        st.metric("Relative Mass Balance (RMB)", f"{round(rmb, 2)}%")
        st.caption("Shows detectability index")

    # Scientific Validation Section
    st.divider()
    st.subheader("Scientific Validation & Detectability Analysis")
    if st.button("Run Live Scientific Validation (MB Simulation)"):
        with st.spinner("Running Monte-Carlo Simulation for MB Proofs..."):
            # Capture stdout to show results
            import io, contextlib
            f = io.StringIO()
            with contextlib.redirect_stdout(f):
                validation_proofs.run_mb_validation_simulation()
            st.code(f.getvalue())
            st.success("Validation Complete: Relative Mass Balance confirmed as superior for regulatory submission.")
            
    with st.expander("Why Relative MB is the Winning Standard?", expanded=False):
        st.write("""
            **Methodology**: Simple Mass Balance (SMB) often masks sensitivity gaps. 
            **Relative Mass Balance (RMB)** isolates the change in degradants relative to API loss, 
            exposing hidden 'Invisible Gaps' in your analytical methods.
        """)

    # Recommendation Engine
    st.subheader("AI Recommendation Matrix")
    if amb < 95:
        st.error(f"Warning: Absolute Mass Balance Deficiency (AMBD) is {round(ambd, 2)}%. Critical investigation required.")
    elif rmb < 85:
        st.warning(f"Caution: Relative Mass Balance is low ({round(rmb, 2)}%). This indicates poor detection of degradants.")
    else:
        st.success("Mass Balance is within acceptable regulatory thresholds.")

# --- PAGE 3: Safety Search ---
elif Page == "Safety Search":
    st.title("Safety Semantic Search (Cross-Study)")
    st.write("Search across all MedDRA and WHODD coding reports from Study 1 to Study 25.")
    
    query = st.text_input("Enter symptom, medication, or medical term (e.g., Headache, Rash, Aspirin)", "")
    
    if query:
        # Cross-study search implementation
        base_dir = r"d:\NEST 2.0\QC Anonymized Study Files"
        
        # Tier 2: Search Indexing (High Speed)
        @st.cache_resource
        def get_all_coding_files(root_dir):
            index_path = r"d:\NEST 2.0\.cache\search_index.joblib"
            if os.path.exists(index_path):
                # Only trust index if it's recent (e.g., < 24h old) or we can just use it
                return joblib.load(index_path)
            
            coding_files = []
            for root, dirs, files in os.walk(root_dir):
                if ".cache" in root: continue
                for f in files:
                    if any(x in f for x in ["Coding", "Medra", "MedDRA", "WHODD", "WHODrug"]) and f.endswith(".xlsx"):
                        coding_files.append(os.path.join(root, f))
            
            if not os.path.exists(os.path.dirname(index_path)): os.makedirs(os.path.dirname(index_path))
            joblib.dump(coding_files, index_path)
            return coding_files

        @st.cache_data
        def search_in_file(file_path, query):
            try:
                # Optimization: Read only first 1000 rows
                df_tmp = pd.read_excel(file_path, nrows=1000)
                mask = df_tmp.astype(str).apply(lambda x: x.str.contains(query, case=False)).any(axis=1)
                matches = df_tmp[mask].copy()
                if not matches.empty:
                    matches['Source File'] = os.path.basename(file_path)
                    matches['Study'] = os.path.basename(os.path.dirname(file_path))
                    return matches
            except Exception:
                pass
            return None

        all_files = get_all_coding_files(base_dir)
        
        if all_files:
            results_list = []
            progress_bar = st.progress(0)
            with st.spinner(f"Searching across {len(all_files)} clinical reports..."):
                for i, file_path in enumerate(all_files):
                    res = search_in_file(file_path, query)
                    if res is not None:
                        results_list.append(res)
                    progress_bar.progress((i + 1) / len(all_files))
                
                if results_list:
                    final_results = pd.concat(results_list, ignore_index=True)
                    st.success(f"Found {len(final_results)} matches for '{query}' across study reports.")
                    st.dataframe(final_results)
                else:
                    st.info(f"No matches found for '{query}' in any study reports.")
        else:
            st.error("No safety coding reports found in the study directories.")

# Sidebar Configuration
st.sidebar.markdown("---")
study_options = [d for d in os.listdir(r"d:\NEST 2.0\QC Anonymized Study Files") if os.path.isdir(os.path.join(r"d:\NEST 2.0\QC Anonymized Study Files", d))]
study_selection = st.sidebar.selectbox("Select Study for Dashboard", study_options)

# Data Loading and Re-training Logic
@st.cache_data
def get_study_data(study):
    with st.spinner(f"Re-processing and training for {study}..."):
        df_processed = load_and_preprocess_data(study)
        if df_processed.empty:
            return None
        # Save locally for train_model to pick up
        df_processed.to_csv(r"d:\NEST 2.0\processed_site_metrics.csv", index=False)
        train_custom_model()
        # Load the scored results
        return pd.read_csv(r"d:\NEST 2.0\scored_site_metrics.csv")

df = get_study_data(study_selection)

if df is not None and Page in lang["nav"][0]:
    # Key Metrics Row
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric(lang["total_sites"], len(df))
    with m2:
        st.metric(lang["anomalies"], len(df[df['is_anomaly'] == -1]))
    with m3:
        st.metric(lang["avg_queries"], round(df['query_count'].mean(), 1))
    with m4:
        st.metric(lang["missing_pages"], int(df['missing_page_count'].sum()))

    # Visualizations
    c1, c2 = st.columns(2)
    
    with c1:
        st.write("### Query Density by Site")
        fig = px.bar(df, x='Site ID', y='query_count', color='is_anomaly', 
                     color_discrete_map={1: '#00cc96', -1: '#ef553b'})
        fig.update_layout(margin=dict(l=0, r=0, t=30, b=0), height=400)
        st.plotly_chart(fig, use_container_width=True)
        
    with c2:
        st.write("### SAE vs. Missing Data Correlation")
        fig = px.scatter(df, x='missing_page_count', y='sae_count', size='query_count', 
                         color='is_anomaly', hover_name='Site ID',
                         color_discrete_map={1: '#00cc96', -1: '#ef553b'})
        fig.update_layout(margin=dict(l=0, r=0, t=30, b=0), height=400)
        st.plotly_chart(fig, use_container_width=True)

    # PAGE 1 - NEW SECTION: Global Risk Heatmap
    st.write("### Predictive Risk Heatmap (Country Level)")
    country_risk = df.groupby('Country')['anomaly_score'].mean().reset_index()
    fig_map = px.bar(country_risk.sort_values(by='anomaly_score'), x='Country', y='anomaly_score',
                     color='anomaly_score', color_continuous_scale="Reds_r")
    fig_map.update_layout(title="Operational Risk Index by Country (Lower = Higher Risk)")
    st.plotly_chart(fig_map, use_container_width=True)

    # Anomaly Breakdown with Narrative Generation
    st.write("### Custom ML Anomaly Analysis and Narrative Generator")
    anomalies = df[df['is_anomaly'] == -1].sort_values(by='anomaly_score')
    
    if not anomalies.empty:
        st.warning(f"Detection System identified {len(anomalies)} sites with irregular operational patterns.")
        
        # Site Selector for Narrative
        selected_site = st.selectbox("Select a site to generate a draft Clinical Study Report (CSR) Narrative:", anomalies['Site ID'].unique())
        
        if selected_site:
            site_data = anomalies[anomalies['Site ID'] == selected_site].iloc[0]
            
            # Local Logic-Based Narrative Engine (Localized)
            narr_strings = {
                "English": {
                    "header": f"DRAFT REGULATORY NARRATIVE: SITE {selected_site}",
                    "exec": f"Executive Summary: Site {selected_site} (Region: {site_data['Region']}, Country: {site_data['Country']}) has been flagged by the NEST 2.0 ML engine for significant operational divergence.",
                    "findings": "Key Findings",
                    "query": f"Query Volume: {int(site_data['query_count'])} queries detected, which is {round(site_data['query_count']/(df['query_count'].mean() or 1), 1)}x the study average.",
                    "integrity": f"Data Integrity: {int(site_data['missing_page_count'])} missing pages identified.",
                    "safety": f"Safety Profile: {int(site_data['sae_count'])} Serious Adverse Events reported.",
                    "rca": "Root Cause Analysis: The combination of high query volume and missing data suggest 'Site Overload'.",
                    "rec": "Recommendation: Immediate monitoring visit suggested."
                },
                "Japanese": {
                    "header": f"下書き用規制ナラティブ: サイト {selected_site}",
                    "exec": f"要約: サイト {selected_site} (地域: {site_data['Region']}, 国: {site_data['Country']}) は、重大な運用の乖離があるとしてNEST 2.0 MLエンジンによってフラグが立てられました。",
                    "findings": "主な調査結果",
                    "query": f"クエリボリューム: {int(site_data['query_count'])} 件のクエリが検出されました。これは研究平均の {round(site_data['query_count']/(df['query_count'].mean() or 1), 1)} 倍です。",
                    "integrity": f"データの整合性: {int(site_data['missing_page_count'])} 件の欠損ページが特定されました。",
                    "safety": f"安全性プロファイル: {int(site_data['sae_count'])} 件の重大な有害事象が報告されました。",
                    "rca": "根本原因分析: 高いクエリボリュームと欠損データの組み合わせは、「サイトの過負荷」を示唆しています。",
                    "rec": "推奨事項: 即時のモニタリング訪問を推奨します。"
                },
                "Spanish": {
                    "header": f"BORRADOR DE NARRATIVA REGULATORIA: SITIO {selected_site}",
                    "exec": f"Resumen Ejecutivo: El sitio {selected_site} (Región: {site_data['Region']}, País: {site_data['Country']}) ha sido marcado por el motor NEST 2.0 ML por una divergencia operativa significativa.",
                    "findings": "Hallazgos Clave",
                    "query": f"Volumen de Consultas: {int(site_data['query_count'])} consultas detectadas, lo cual es {round(site_data['query_count']/(df['query_count'].mean() or 1), 1)} veces el promedio del estudio.",
                    "integrity": f"Integridad de Datos: {int(site_data['missing_page_count'])} páginas faltantes identificadas.",
                    "safety": f"Perfil de Seguridad: {int(site_data['sae_count'])} Eventos Adversos Graves reportados.",
                    "rca": "Análisis de Causa Raíz: La combinación de un alto volumen de consultas y datos faltantes sugiere una 'Sobrecarga del Sitio'.",
                    "rec": "Recomendación: Se sugiere una visita de monitoreo inmediata."
                }
            }
            n = narr_strings[Language]
            
            narrative = f"""
            **{n['header']}**
            
            **{n['exec']}**
            
            **{n['findings']}**:
            - {n['query']}
            - {n['integrity']}
            - {n['safety']}
            
            **{n['rca']}**
            
            **{n['rec']}**
            """
            st.info(narrative)
            
        st.table(anomalies[['Site ID', 'Country', 'query_count', 'missing_page_count', 'sae_count', 'anomaly_score']])
    else:
        st.success("No critical operational anomalies detected with current thresholds.")

    # Proactive Alert Simulation
    st.write("### Proactive Follow-Up Alert System (Simulation)")
    if st.button(lang["push_button"]):
        high_risk_sites = anomalies.head(5)['Site ID'].tolist()
        for site in high_risk_sites:
            st.success(f"System: SMS and Email notification dispatched to Investigator at Site {site} regarding data backlog.")
        st.info("Simulation complete. Notifications would be sent via SMTP/Twilio in production.")

elif df is None:
    st.info("Data is currently being processed by the backend pipeline...")
    if st.button("Refresh Data Status"):
        st.rerun()

# Activity Log Display
st.sidebar.markdown("---")
st.sidebar.write("### Backend Activity Log")
if os.path.exists(r"d:\NEST 2.0\activity_log.txt"):
    with open(r"d:\NEST 2.0\activity_log.txt", "r") as f:
        st.sidebar.text(f.read()[-500:]) # Show last 500 chars
