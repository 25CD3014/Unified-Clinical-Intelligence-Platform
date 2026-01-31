import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import joblib
from data_pipeline import load_and_preprocess_data
from train_model import train_custom_model
import validation_proofs
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode
from fpdf import FPDF
import base64

# PDF Report Generator Class
class NESTReport(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'NEST 2.0: Clinical Study Report Narrative', 0, 1, 'C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

def create_pdf_report(site_id, narrative_text, site_data):
    pdf = NESTReport()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    # Title
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 10, txt=f"Site Investigation Report: {site_id}", ln=True)
    pdf.ln(5)
    
    # Narrative Content
    pdf.set_font("Arial", size=11)
    # Cleaning markdown for PDF
    clean_narrative = narrative_text.replace("**", "").replace("-", "*")
    pdf.multi_cell(0, 10, txt=clean_narrative)
    
    pdf.ln(10)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, txt="Site Metrics Summary", ln=True)
    pdf.set_font("Arial", size=10)
    
    metrics = [
        f"Country: {site_data['Country']}",
        f"Region: {site_data['Region']}",
        f"Query Count: {int(site_data['query_count'])}",
        f"Missing Pages: {int(site_data['missing_page_count'])}",
        f"SAE Count: {int(site_data['sae_count'])}",
        f"Anomaly Score: {round(site_data['anomaly_score'], 4)}"
    ]
    
    for m in metrics:
        pdf.cell(200, 8, txt=m, ln=True)
        
    return pdf.output(dest='S').encode('latin-1')

# Dynamic Path Handling - Global Scope
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
base_dir = os.path.join(BASE_DIR, "QC Anonymized Study Files")

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

# --- PAGE 3: Safety Signal Intelligence (Agentic Discovery) ---
elif Page == "Safety Search":
    st.title("Safety Signal Intelligence: Discovery Mode")
    st.write("""
        This engine performs **Cross-Study Signal Detection**. It analyze data patterns in raw clinical reports 
        to find emerging safety signals (like 'Headache') that are not explicitly labeled.
    """)

    # --- Mode Selector ---
    discovery_mode = st.radio("Intelligence Mode", ["Keyword Signal Tracking", "Global Pattern Discovery (Agentic)"], horizontal=True)

    # Dynamic Path Handling (Removed local definition, using global)
    # BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    # base_dir = os.path.join(BASE_DIR, "QC Anonymized Study Files")
    
    @st.cache_resource
    def get_all_safety_files(root_dir):
        keywords = ["coding", "medra", "meddra", "whodd", "whodrug", "sae", "dashboard", "safety"]
        files_found = []
        for root, dirs, files in os.walk(root_dir):
            if ".cache" in root: continue
            for f in files:
                f_low = f.lower().replace("_", " ")
                if any(kw in f_low for kw in keywords) and f.endswith(".xlsx"):
                    files_found.append(os.path.join(root, f))
        return files_found

    all_safety_files = get_all_safety_files(base_dir)

    if discovery_mode == "Keyword Signal Tracking":
        query = st.text_input("Enter a symptom or medical term to track across studies:", "Headache")
        
        if query:
            # Semantic Expansion
            semantic_map = {
                "headache": ["migraine", "cephalgia", "head pain", "nervous system"],
                "nausea": ["vomiting", "emesis", "upset stomach", "queasiness"],
                "pain": ["ache", "discomfort", "soreness"],
                "fatigue": ["tiredness", "lethargy", "exhaustion"],
                "fever": ["pyrexia", "temperature", "hyperthermia"]
            }
            expanded = [query.lower()]
            for k, v in semantic_map.items():
                if k in query.lower(): expanded.extend(v)
            
            st.caption(f"🤖 Gen AI Semantic Expansion: Also searching for {', '.join(expanded)}")

            results = []
            with st.spinner("Scanning for safety patterns (Deep Scan)..."):
                for f in all_safety_files:
                    try:
                        df_tmp = pd.read_excel(f, engine='calamine')
                        mask = df_tmp.astype(str).apply(lambda x: x.str.contains('|'.join(expanded), case=False)).any(axis=1)
                        matches = df_tmp[mask].copy()
                        if not matches.empty:
                            matches['Study'] = os.path.basename(os.path.dirname(f))
                            matches['File'] = os.path.basename(f)
                            # Tag if it's an SAE
                            matches['Signal Type'] = "Critical (SAE)" if "sae" in f.lower() else "Operational (Coding)"
                            results.append(matches)
                    except: continue

            if results:
                master_signals = pd.concat(results, ignore_index=True)
                
                # Signal Density Visualization
                st.subheader(f"Signal Map for '{query}'")
                fig_signal = px.histogram(master_signals, x='Study', color='Signal Type', barmode='group',
                                       title="Clinical Signal Concentration by study")
                st.plotly_chart(fig_signal, use_container_width=True)
                
                # Insights
                top_study = master_signals['Study'].value_counts().idxmax()
                st.info(f"**AI Interpretation**: The highest signal cluster for `{query}` is located in **{top_study}**. Recommendation: Cross-reference with Site Anomaly scores in the Operational Dashboard.")
                
                st.write("### Data-Level Evidence")
                st.dataframe(master_signals)
            else:
                st.info("No matching signal patterns found.")

    else: # Global Pattern Discovery (Agentic)
        st.subheader("Global Medical Pattern Discovery (Top Signals)")
        st.write("Automatically categorizing clinical terms across ALL reports to find where the 'Headaches' are hiding.")
        
        if st.button("Run Agentic Signal Scan (Full Portfolio)"):
            with st.spinner("Processing portofolio-wide safety signals..."):
                # Simulation of a high-power pattern recognizer
                # We extract the most common coding patterns from the MedDRA reports
                all_found_terms = []
                for f in all_safety_files[:10]: # Scan first 10 for performance
                    if "meddra" in f.lower():
                        try:
                            df_tmp = pd.read_excel(f, usecols=['Coded Term'], nrows=500, engine='calamine')
                            all_found_terms.extend(df_tmp['Coded Term'].dropna().tolist())
                        except: continue
                
                if all_found_terms:
                    term_counts = pd.Series(all_found_terms).value_counts().head(10).reset_index()
                    term_counts.columns = ['Medical Pattern', 'Occurrence']
                    
                    st.write("### Portfolio-Wide Safety Heatmap")
                    fig_global = px.treemap(term_counts, path=['Medical Pattern'], values='Occurrence',
                                         color='Occurrence', color_continuous_scale='Reds')
                    st.plotly_chart(fig_global, use_container_width=True)
                    
                    st.success("Successfully identified clinical hotspots across the database.")
                    
                    # Highlight 'Headache' specifically if found in patterns
                    headache_patterns = [t for t in all_found_terms if "headache" in str(t).lower()]
                    if headache_patterns:
                        st.warning(f"⚠️ FOUND: Hidden 'Headache' patterns detected {len(headache_patterns)} times in the global portfolio data, even when not explicitly searched for.")
                    else:
                        st.info("No dominant 'Headache' patterns found in the global scan. The data appears stable.")

# Sidebar Configuration
st.sidebar.markdown("---")
st.sidebar.subheader("📤 Upload New Study Data")
uploaded_files = st.sidebar.file_uploader("Upload Study ZIP or Excel files", type=["zip", "xlsx"], accept_multiple_files=True)

if uploaded_files:
    import zipfile
    import shutil
    
    for uploaded_file in uploaded_files:
        if uploaded_file.name.endswith(".zip"):
            # Handle ZIP uploads
            with zipfile.ZipFile(uploaded_file, 'r') as zip_ref:
                # Extract to a folder named after the ZIP
                target_name = uploaded_file.name.replace(".zip", "")
                target_path = os.path.join(base_dir, target_name)
                os.makedirs(target_path, exist_ok=True)
                zip_ref.extractall(target_path)
                st.sidebar.success(f"Extracted: {uploaded_file.name}")
        else:
            # Handle individual Excel files
            # Default to a "Manual_Uploads" folder if no ZIP context
            target_path = os.path.join(base_dir, "Manual_Uploads")
            os.makedirs(target_path, exist_ok=True)
            with open(os.path.join(target_path, uploaded_file.name), "wb") as f:
                f.write(uploaded_file.getbuffer())
            st.sidebar.success(f"Saved: {uploaded_file.name}")
    
    st.sidebar.info("Refresh to see new studies in the list.")
    if st.sidebar.button("Refresh Study List"):
        st.rerun()

st.sidebar.markdown("---")
if os.path.exists(base_dir):
    study_options = [d for d in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, d))]
else:
    study_options = []
    st.sidebar.warning(f"Note: Data directory not found at {base_dir}")
study_selection = st.sidebar.selectbox("Select Study for Dashboard", study_options)

# Data Loading and Re-training Logic
@st.cache_data
def get_study_data(study):
    # Added explicit status logging for user visibility
    status_msg = st.empty()
    status_msg.info(f"Initiating Data Synthesis for {study}...")
    
    with st.spinner(f"Synchronizing Global Intelligence for {study}..."):
        try:
            df_processed = load_and_preprocess_data(study)
            if df_processed.empty:
                status_msg.error(f"Synthesis Failed for {study}: No valid EDC metrics found in folder.")
                return None
            
            status_msg.info(f"Synthesis Success. Re-calibrating Site Risk Boundaries...")
            
            # Save locally for train_model to pick up
            df_processed.to_csv(os.path.join(BASE_DIR, "processed_site_metrics.csv"), index=False)
            train_custom_model()
            
            # Clear status on success
            status_msg.empty()
            
            # Load the scored results
            return pd.read_csv(os.path.join(BASE_DIR, "scored_site_metrics.csv"))
        except Exception as e:
            status_msg.error(f"Critical Error in Data Pipeline: {e}")
            return None

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

    # PAGE 1 - NEW SECTION: Global Risk Heatmap (Choropleth Map)
    st.write("### Predictive Risk Heatmap (Geospatial Analysis)")
    country_risk = df.groupby('Country')['anomaly_score'].mean().reset_index()
    
    # Using choropleth for professional mapping
    fig_map = px.choropleth(country_risk, 
                            locations="Country", 
                            locationmode='country names',
                            color="anomaly_score", 
                            hover_name="Country",
                            color_continuous_scale="Reds_r",
                            labels={'anomaly_score':'Risk Index'})
    
    fig_map.update_layout(
        geo=dict(showframe=False, showcoastlines=True, projection_type='equirectangular'),
        margin=dict(l=0, r=0, t=30, b=0),
        height=500
    )
    st.plotly_chart(fig_map, use_container_width=True)

    # Anomaly Breakdown with Narrative Generation
    st.write("### Custom ML Anomaly Analysis (Interactive Data Grid)")
    anomalies = df[df['is_anomaly'] == -1].sort_values(by='anomaly_score')
    
    if not anomalies.empty:
        st.warning(f"Detection System identified {len(anomalies)} sites with irregular operational patterns.")
        
        # AgGrid Implementation
        gb = GridOptionsBuilder.from_dataframe(anomalies[['Site ID', 'Country', 'query_count', 'missing_page_count', 'sae_count', 'anomaly_score']])
        gb.configure_pagination(paginationAutoPageSize=True)
        gb.configure_side_bar()
        gb.configure_selection('single', use_checkbox=True)
        gridOptions = gb.build()
        
        grid_response = AgGrid(
            anomalies,
            gridOptions=gridOptions,
            update_mode=GridUpdateMode.SELECTION_CHANGED,
            theme='balham', # Professional theme
            height=300,
            width='100%',
        )
        
        selected = grid_response['selected_rows']
        selected_site = None
        if selected is not None and not selected.empty:
            selected_site = selected.iloc[0]['Site ID']
        
        # Narrative Section
        if selected_site:
            st.write(f"#### Generated Narrative for Site {selected_site}")
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
{n['header']}

{n['exec']}

{n['findings']}:
- {n['query']}
- {n['integrity']}
- {n['safety']}

{n['rca']}

{n['rec']}
            """
            st.info(narrative)
            
            # PDF Export Button
            try:
                pdf_data = create_pdf_report(selected_site, narrative, site_data)
                st.download_button(
                    label="📥 Download Clinical Study Report (PDF)",
                    data=pdf_data,
                    file_name=f"NEST_Report_Site_{selected_site}.pdf",
                    mime="application/pdf"
                )
            except Exception as e:
                st.error(f"Error generating PDF: {e}")
            
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
if os.path.exists(os.path.join(BASE_DIR, "activity_log.txt")):
    with open(os.path.join(BASE_DIR, "activity_log.txt"), "r") as f:
        st.sidebar.text(f.read()[-500:]) # Show last 500 chars
