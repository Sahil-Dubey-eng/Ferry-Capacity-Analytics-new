# ⛴️ Ferry Capacity Utilization & Operational Efficiency Analytics System

An enterprise-grade, data-driven analytical dashboard built with **Streamlit**, **Pandas**, **NumPy**, and **Plotly** to evaluate ferry ticketing demand, terminal throughput, congestion pressure, and capacity utilization patterns using historical data from the **Toronto Ferry Terminal**.

---

## 📂 Project Architecture & File-by-File Directory Guide

The codebase is organized following modern modular data engineering principles:

```text
Ferry-Capacity-Analytics/
├── .streamlit/
│   └── config.toml               # Streamlit theme (navy/blue dark palette) & server settings
├── analytics/                    # Core mathematical, statistical & analytical engines
│   ├── __init__.py               # Python package initialization
│   ├── data_cleaning.py          # CSV ingestion, data validation & pre-cleaning quality audits
│   ├── feature_engineering.py    # Normalized OLI (95th percentile), ratios, temporal attributes, rolling spikes
│   ├── kpi.py                    # High-level KPIs, peak strain duration, and variability metrics
│   └── analysis.py               # Granular aggregations (15m/Hourly/Daily), diurnal, seasonal, heatmap
├── components/                   # UI Presentation modules
│   ├── __init__.py               # Python package initialization
│   └── documentation.py          # Comprehensive bilingual (English + Hindi) documentation modal
├── data/                         # Data layer
│   └── Toronto_Ferry_Terminal_Ticket_Sales.csv  # Canonical historical dataset (278,598 records)
├── utils/                        # Shared utility helpers
│   ├── __init__.py               # Python package initialization
│   └── helpers.py                # Number/percentage formatting, badges & operational alerts
├── .dockerignore                 # Exclusions for container builds
├── .gitignore                    # Standard Python, virtual environment & cache ignores
├── Dockerfile                    # Container definition for cloud deployments
├── Procfile                      # Web process launcher for PaaS (Render / Railway / Heroku)
├── render.yaml                   # Infrastructure-as-Code blueprint for 1-click Render deployment
├── requirements.txt              # Pinned Python package dependencies
├── app.py                        # Main Streamlit application entrypoint & reactive orchestrator
└── README.md                     # System documentation & deployment handbook
```

---

### 📄 Detailed File Descriptions

| File / Folder | Purpose & Role |
| :--- | :--- |
| **`app.py`** | **Main Application Entrypoint.** Manages cached data pipelines (`@st.cache_data`), sidebar parameter controls, KPI cards, interactive Plotly visualizations, anomaly tables, and CSV exports. |
| **`analytics/data_cleaning.py`** | **Data Ingestion & Integrity Engine.** Parses timestamps, handles missing counts, clamps negative entries, detects zero activity, checks duplicate IDs, and compiles data quality audit statistics. |
| **`analytics/feature_engineering.py`** | **Feature Transformation Engine.** Calculates Total Activity, Redemption Pressure Ratio, Operational Load Index (OLI) against a 95th-percentile baseline, and runs a 2-hour rolling window ($2\sigma$) anomaly spike detector. |
| **`analytics/kpi.py`** | **Operational KPI Calculator.** Calculates utilization rates, idle and congestion percentages, sustained idle counts, operational variability score, and uninterrupted peak strain durations. |
| **`analytics/analysis.py`** | **Aggregation & Pattern Mining.** Powers dynamic resampling (`15-Minute`, `Hourly`, `Daily`), Congestion Pressure Index (CPI), Weekday vs Weekend comparisons, seasonal efficiency, and Day-of-Week $\times$ Hour heatmaps. |
| **`components/documentation.py`** | **Documentation Component.** Renders an interactive, bilingual (English & Hindi) modal detailing the project architecture, objectives, formulas, and operational implications. |
| **`utils/helpers.py`** | **Display Formatting Utilities.** Provides human-readable numerical formatting, safe percentages, and status alerts. |
| **`data/Toronto_Ferry_Terminal_Ticket_Sales.csv`** | **Primary Dataset.** Contains 278,598 rows of 15-minute interval ticket sales and redemption records. |
| **`requirements.txt`** | **Dependency Specifications.** Declares runtime dependencies (`streamlit`, `pandas`, `numpy`, `plotly`, `openpyxl`). |
| **`.streamlit/config.toml`** | **Visual Styling & Performance.** Dark naval theme palette, disables usage telemetry, and enables headless execution. |
| **`Dockerfile` & `.dockerignore`** | **Containerization.** Portable container build for deployment to any cloud container host. |
| **`Procfile` & `render.yaml`** | **PaaS Hosting Configs.** Configuration files for automatic builds on Render or Railway. |

---

## 🚀 Deployment Guide: Where & How to Deploy

### 🌐 Summary: Which Files Go Where?

When you push this repository to **GitHub**, **all files in this project are deployed together**. Unlike traditional decoupled applications (which have separate frontend React and backend Express folders), this is a unified **full-stack Python/Streamlit data application**.

| What Platform To Use | Cost | Best For | Deployment Source |
| :--- | :--- | :--- | :--- |
| **1. Streamlit Community Cloud** *(Recommended)* | **100% Free** | Native hosting, automatic updates on git push, 1-click setup | Connect directly to your GitHub repository |
| **2. Hugging Face Spaces** | **100% Free** | Machine learning & data showcase | Select "Streamlit" SDK and connect GitHub |
| **3. Render.com / Railway.app** | **Free / Low-cost** | Production cloud web services using `Procfile` / `Dockerfile` | Connect GitHub repository |
| **4. Docker / AWS / GCP / Azure** | **Variable** | Custom virtual machine or Kubernetes cluster | Deploy using the included `Dockerfile` |

---

### Option 1: Deploying on Streamlit Community Cloud (Recommended & Easiest)

**Why Streamlit Cloud?**
- 100% Free with zero cloud configuration required.
- Automatically rebuilds and redeploys every time you push changes to GitHub.
- Handles SSL certificates, domain routing, and secrets automatically.

**Step-by-step instructions:**
1. Push your project to GitHub:
   ```bash
   git add .
   git commit -m "Configure clean modular ferry analytics project ready for deployment"
   git push origin main
   ```
2. Go to **[share.streamlit.io](https://share.streamlit.io/)** and log in with your GitHub account.
3. Click **"Create app"** (or **"New app"**).
4. Fill in the deployment fields:
   - **Repository:** `Sahil-Dubey-eng/Ferry-Capacity-Analytics-new`
   - **Branch:** `main`
   - **Main file path:** `app.py`
5. Click **"Deploy!"**.
6. Within 1-2 minutes, your dashboard will be live at a public URL (e.g., `https://ferry-capacity-analytics.streamlit.app`).

---

### Option 2: Deploying on Hugging Face Spaces

1. Create a free account on **[huggingface.co](https://huggingface.co/)**.
2. Click on your profile $\rightarrow$ **"New Space"**.
3. Choose a Space name (e.g. `ferry-capacity-analytics`).
4. Select **Streamlit** as the Space SDK.
5. Select **Public** and click **"Create Space"**.
6. Under Settings, connect your GitHub repository or push via Git:
   ```bash
   git remote add space https://huggingface.co/spaces/YOUR_USERNAME/ferry-capacity-analytics
   git push space main
   ```

---

### Option 3: Deploying on Render (Free Web Service)

1. Sign up at **[render.com](https://render.com/)**.
2. Click **"New +"** $\rightarrow$ **"Web Service"**.
3. Connect your GitHub repository (`Sahil-Dubey-eng/Ferry-Capacity-Analytics-new`).
4. Settings:
   - **Environment:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `streamlit run app.py --server.port=$PORT --server.address=0.0.0.0`
5. Click **"Create Web Service"**.

---

### Option 4: Deploying with Docker (Self-Hosted / Cloud VM)

Build and run locally or on any server with Docker installed:
```bash
# 1. Build the container image
docker build -t ferry-capacity-analytics .

# 2. Run the container
docker run -d -p 8501:8501 --name ferry-app ferry-capacity-analytics

# 3. Access in your browser
http://localhost:8501
```

---

## 💻 Local Development Setup

To run the project locally on your machine:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Sahil-Dubey-eng/Ferry-Capacity-Analytics-new.git
   cd Ferry-Capacity-Analytics-new
   ```

2. **Create and activate a virtual environment:**
   ```bash
   # Windows (PowerShell)
   python -m venv venv
   .\venv\Scripts\Activate.ps1

   # macOS / Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Launch the dashboard:**
   ```bash
   streamlit run app.py
   ```

---

## 📊 Analytical Methodology & Indicators

- **Operational Load Index (OLI):** Measures handling pressure normalized against the 95th-percentile activity baseline ($P_{95}$).
- **Congestion Pressure Index (CPI):** Weights load intensity by actual boarding demand (redemption ratio):
  $$\text{CPI} = \text{OLI} \times \left( \frac{\text{Redemption Count}}{\text{Total Activity} + 1} \right)$$
- **Rolling Spike Detection:** Flags intervals where total passenger activity exceeds the 2-hour rolling mean by more than two standard deviations ($> \mu + 2\sigma$).
- **Sustained Idle Indicator:** Identifies consecutive intervals ($\ge 3$ consecutive periods) operating below the $20\%$ utilization threshold to assist in staff scheduling and vessel idling strategies.

---

## 📜 License & Authorship
Developed for **Toronto Ferry Terminal Ticket Activity Analytics**.
