import sys
from pathlib import Path
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# Modular Architecture Imports
from analytics.data_cleaning import load_and_clean_data, get_data_quality_report
from analytics.feature_engineering import create_features
from analytics.kpi import calculate_kpis
from analytics.analysis import (
    aggregate_data,
    seasonal_analysis,
    weekday_analysis,
    time_period_analysis,
    hourly_heatmap_data,
    yearly_analysis,
    get_top_congestion_windows,
    get_top_idle_windows
)
from utils.helpers import format_number, format_decimal, safe_percentage, get_status_message
from components.documentation import render_documentation

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Ferry Capacity Analytics",
    page_icon="⛴️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# DATA PATH & CONSTANTS
# ============================================================

DATA_PATH = Path(__file__).resolve().parent / "data" / "Toronto_Ferry_Terminal_Ticket_Sales.csv"
CONGESTION_DEFAULT = 80
IDLE_DEFAULT = 20

# ============================================================
# CACHED DATA INGESTION & FEATURE PIPELINE
# ============================================================

@st.cache_data(show_spinner="Loading and transforming ferry ticket data...")
def get_processed_dataset():
    """
    Load, validate, clean, and enrich ferry dataset.
    Cached to guarantee instant interactivity during dashboard navigation.
    """
    df_clean, raw_quality = load_and_clean_data(DATA_PATH)
    df_featured = create_features(df_clean)
    return df_featured, raw_quality


try:
    df, quality_stats = get_processed_dataset()
except Exception as err:
    st.error(f"⚠️ Dataset Initialization Error: {err}")
    st.info(
        "Please ensure 'Toronto_Ferry_Terminal_Ticket_Sales.csv' is placed inside the 'data/' folder."
    )
    st.stop()

# ============================================================
# SIDEBAR CONTROLS & DOCUMENTATION
# ============================================================

st.sidebar.title("⛴️ Ferry Analytics")
st.sidebar.caption("Capacity Utilization & Efficiency System")

show_about = st.sidebar.checkbox(
    "📘 About Project / प्रोजेक्ट के बारे में",
    help="Toggle full bilingual system documentation and architectural guide."
)

if show_about:
    render_documentation()
    st.stop()

st.sidebar.divider()
st.sidebar.header("🔍 Dashboard Filters")

min_date = df["Timestamp"].min().date()
max_date = df["Timestamp"].max().date()

date_range = st.sidebar.date_input(
    "📅 Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date,
    help="Select the chronological analysis window."
)

if isinstance(date_range, (tuple, list)) and len(date_range) == 2:
    start_date = pd.Timestamp(date_range[0])
    end_date = pd.Timestamp(date_range[1]) + pd.Timedelta(days=1)
elif isinstance(date_range, (tuple, list)) and len(date_range) == 1:
    start_date = pd.Timestamp(date_range[0])
    end_date = pd.Timestamp(date_range[0]) + pd.Timedelta(days=1)
else:
    start_date = pd.Timestamp(min_date)
    end_date = pd.Timestamp(max_date) + pd.Timedelta(days=1)

selected_season = st.sidebar.selectbox(
    "🌦️ Season Filter",
    ["All", "Winter", "Spring", "Summer", "Autumn"]
)

selected_day = st.sidebar.selectbox(
    "📅 Day Type Filter",
    ["All", "Weekday", "Weekend"]
)

granularity = st.sidebar.radio(
    "⏱️ Time Granularity",
    ["15-Minute", "Hourly", "Daily"],
    index=1
)

st.sidebar.subheader("⚙️ Operational Thresholds")

congestion_threshold = st.sidebar.slider(
    "🔴 Congestion Threshold (%)",
    min_value=50,
    max_value=100,
    value=CONGESTION_DEFAULT,
    step=5,
    help="Operational Load Index threshold considered high strain."
)

idle_threshold = st.sidebar.slider(
    "🔵 Idle Threshold (%)",
    min_value=0,
    max_value=50,
    value=IDLE_DEFAULT,
    step=5,
    help="Operational Load Index threshold considered underutilized/idle."
)

# ============================================================
# FILTER APPLICATION
# ============================================================

filtered = df[
    (df["Timestamp"] >= start_date) &
    (df["Timestamp"] < end_date)
].copy()

if selected_season != "All":
    filtered = filtered[filtered["Season"] == selected_season]

if selected_day != "All":
    filtered = filtered[filtered["Day Type"] == selected_day]

if filtered.empty:
    st.warning("⚠️ No records match the selected filter parameters. Please widen your selection.")
    st.stop()

# ============================================================
# AGGREGATION & OPERATIONAL METRICS
# ============================================================

analysis = aggregate_data(
    filtered,
    granularity=granularity,
    congestion_threshold=congestion_threshold,
    idle_threshold=idle_threshold
)

if analysis.empty:
    st.warning("⚠️ No active ticketing activity detected within the selected timeframe.")
    st.stop()

# Determine interval length in minutes for strain duration calculation
if granularity == "15-Minute":
    interval_mins = 15
elif granularity == "Hourly":
    interval_mins = 60
else:
    interval_mins = 1440

kpi_metrics = calculate_kpis(
    analysis,
    congestion_threshold=congestion_threshold,
    idle_threshold=idle_threshold,
    interval_minutes=interval_mins
)

# Overall totals from raw filtered slice
total_records = len(filtered)
total_sales = int(filtered["Sales Count"].sum())
total_redemptions = int(filtered["Redemption Count"].sum())

# ============================================================
# DASHBOARD HEADER
# ============================================================

st.title("⛴️ Ferry Capacity Utilization & Operational Efficiency Analytics")
st.caption("Toronto Ferry Terminal Real-Time Demand, Load & Congestion Intelligence")
st.divider()

# ============================================================
# KPI OVERVIEW CARDS
# ============================================================

st.subheader("📊 Key Performance Indicators")

c1, c2, c3, c4, c5 = st.columns(5)
with c1:
    st.metric("Total Records", f"{total_records:,}")
with c2:
    st.metric("Total Sales", f"{total_sales:,.0f}")
with c3:
    st.metric("Total Redemptions", f"{total_redemptions:,.0f}")
with c4:
    st.metric("Operational Utilization", f"{kpi_metrics['average_oli']:.2f}%")
with c5:
    st.metric("Idle Capacity Share", f"{kpi_metrics['idle_percentage']:.2f}%")

c6, c7, c8, c9 = st.columns(4)
with c6:
    st.metric("Congestion Pressure Share", f"{kpi_metrics['congestion_percentage']:.2f}%")
with c7:
    st.metric("Peak Observed Load", f"{kpi_metrics['peak_oli']:.2f}%")
with c8:
    st.metric("Sustained Idle Windows", f"{kpi_metrics['sustained_idle_count']:,}")
with c9:
    st.metric("Peak Strain Duration", kpi_metrics["peak_strain_text"])

st.info(
    f"ℹ️ **Operational Variability Score:** `{kpi_metrics['variability_score']:.2f}` (Standard Deviation: `{kpi_metrics['operational_variability']:.2f}%`)\n\n"
    "**Methodological Context:** Operational Load Index (OLI) is a normalized throughput benchmark based on 95th percentile baseline activity. "
    "Because vessel passenger manifests are not part of the ticket stream, this metric reflects terminal handling strain rather than static physical boat occupancy."
)

# ============================================================
# DATA QUALITY & CONSISTENCY
# ============================================================

st.divider()
st.subheader("🧹 Data Quality & Integrity Validation")

q1, q2, q3, q4, q5, q6 = st.columns(6)
with q1:
    st.metric("Invalid Timestamps", quality_stats["invalid_timestamps"])
with q2:
    st.metric("Negative Sales Clamped", quality_stats["negative_sales"])
with q3:
    st.metric("Negative Redemptions Clamped", quality_stats["negative_redemptions"])
with q4:
    st.metric("Zero Activity Records", quality_stats["zero_activity_rows"])
with q5:
    st.metric("Duplicate IDs Flagged", quality_stats["duplicate_ids"])
with q6:
    st.metric("Duplicate Timestamps", quality_stats["duplicate_timestamps"])

# ============================================================
# INTERVAL GAPS & SPIKE DETECTION
# ============================================================

st.subheader("⏱️ 15-Minute Interval Regularity & Spike Anomaly Analysis")

col_gap, col_spike = st.columns(2)

with col_gap:
    timestamp_diff = df["Timestamp"].sort_values().diff()
    expected_step = pd.Timedelta(minutes=15)
    irregular_gaps = timestamp_diff[timestamp_diff != expected_step].dropna()
    
    st.metric("Detected Irregular Time Gaps", f"{len(irregular_gaps):,}")
    if len(irregular_gaps) > 0:
        st.warning("Historical dataset contains seasonal off-peak closures or reporting hiatuses.")
    else:
        st.success("15-minute interval sequence is uniformly continuous.")

with col_spike:
    spike_count = int(filtered["Spike Detected"].sum())
    st.metric("Detected Extreme Activity Spikes", f"{spike_count:,}")
    if spike_count > 0:
        st.info("Spikes indicate activity exceeding 2 standard deviations above the 2-hour rolling mean.")
    else:
        st.success("No rolling-statistic activity anomalies detected in the selected period.")

spike_records = filtered[filtered["Spike Detected"]]
if not spike_records.empty:
    with st.expander("🔍 View Detected Activity Spikes Table"):
        st.dataframe(
            spike_records[
                [
                    "Timestamp", "Sales Count", "Redemption Count",
                    "Total Activity", "Rolling Activity Mean", "Spike Upper Limit"
                ]
            ].sort_values("Total Activity", ascending=False).head(20),
            use_container_width=True
        )

# ============================================================
# CAPACITY UTILIZATION TIMELINE
# ============================================================

st.divider()
st.subheader("📈 Capacity Utilization & Throughput Timeline")

fig_timeline = go.Figure()
fig_timeline.add_trace(
    go.Scattergl(
        x=analysis["Timestamp"],
        y=analysis["Operational Load Index"],
        mode="lines",
        name="Operational Load Index (%)",
        line=dict(color="#38bdf8", width=2)
    )
)
fig_timeline.add_hline(
    y=congestion_threshold,
    line_dash="dash",
    line_color="#ef4444",
    annotation_text=f"Congestion Limit ({congestion_threshold}%)"
)
fig_timeline.add_hline(
    y=idle_threshold,
    line_dash="dash",
    line_color="#3b82f6",
    annotation_text=f"Idle Threshold ({idle_threshold}%)"
)
fig_timeline.update_layout(
    title=f"Operational Load Over Time ({granularity} Granularity)",
    xaxis_title="Timeline",
    yaxis_title="Load Index (%)",
    yaxis=dict(range=[0, 105]),
    height=450,
    template="plotly_dark",
    margin=dict(l=40, r=40, t=50, b=40)
)
st.plotly_chart(fig_timeline, use_container_width=True)

# ============================================================
# CONGESTION PRESSURE INDEX & SALES VS REDEMPTIONS
# ============================================================

col_cpi, col_sales = st.columns(2)

with col_cpi:
    st.subheader("🔥 Congestion Pressure Index (CPI)")
    fig_cpi = px.line(
        analysis,
        x="Timestamp",
        y="Congestion Pressure Index",
        title="Congestion Pressure Index (OLI × Redemption Ratio)",
        labels={"Congestion Pressure Index": "Pressure Index (%)"},
        template="plotly_dark"
    )
    fig_cpi.update_traces(line_color="#f97316")
    fig_cpi.add_hline(y=80, line_dash="dash", line_color="#ef4444", annotation_text="Severe Strain")
    fig_cpi.update_layout(height=420, margin=dict(l=40, r=40, t=50, b=40))
    st.plotly_chart(fig_cpi, use_container_width=True)

with col_sales:
    st.subheader("🎟️ Sales vs. Redemption Activity")
    fig_sr = go.Figure()
    fig_sr.add_trace(
        go.Scattergl(
            x=analysis["Timestamp"],
            y=analysis["Sales Count"],
            mode="lines",
            name="Tickets Sold",
            line=dict(color="#10b981", width=1.5)
        )
    )
    fig_sr.add_trace(
        go.Scattergl(
            x=analysis["Timestamp"],
            y=analysis["Redemption Count"],
            mode="lines",
            name="Tickets Redeemed (Boarded)",
            line=dict(color="#8b5cf6", width=1.5)
        )
    )
    fig_sr.update_layout(
        title="Ticketing Inflow vs. Boarding Inflow",
        xaxis_title="Timeline",
        yaxis_title="Passenger / Ticket Count",
        height=420,
        template="plotly_dark",
        margin=dict(l=40, r=40, t=50, b=40)
    )
    st.plotly_chart(fig_sr, use_container_width=True)

# ============================================================
# CONGESTION & IDLE PERIOD DETAIL TABLES
# ============================================================

st.divider()
st.subheader("🚨 Congestion & Sustained Idle Interval Breakdowns")

left_col, right_col = st.columns(2)

with left_col:
    st.markdown("#### 🔴 Peak Congestion Windows")
    top_cong = get_top_congestion_windows(analysis, limit=15)
    if not top_cong.empty:
        st.dataframe(
            top_cong[
                [
                    "Timestamp", "Sales Count", "Redemption Count",
                    "Total Activity", "Operational Load Index", "Congestion Pressure Index"
                ]
            ].rename(columns={
                "Operational Load Index": "Load Index (%)",
                "Congestion Pressure Index": "CPI (%)"
            }),
            use_container_width=True
        )
    else:
        st.success("No intervals exceeded the congestion threshold in this window.")

with right_col:
    st.markdown("#### 🔵 Sustained Idle Windows (3+ Consecutive Intervals)")
    top_idle = get_top_idle_windows(analysis, limit=15)
    if not top_idle.empty:
        st.dataframe(
            top_idle[
                [
                    "Timestamp", "Sales Count", "Redemption Count",
                    "Total Activity", "Operational Load Index", "Idle Streak"
                ]
            ].rename(columns={"Operational Load Index": "Load Index (%)"}),
            use_container_width=True
        )
    else:
        st.success("No sustained idle periods detected in this window.")

# ============================================================
# TEMPORAL PATTERNS: WEEKDAY, SEASON, TIME BAND
# ============================================================

st.divider()
st.subheader("📅 Operational Patterns & Behavioral Dimensions")

tab_day, tab_season, tab_time = st.tabs([
    "📅 Weekday vs Weekend",
    "🌦️ Seasonal Efficiency",
    "🕐 Time-of-Day Band"
])

with tab_day:
    day_df = weekday_analysis(filtered)
    fig_day = px.bar(
        day_df,
        x="Day Type",
        y="Average_Load",
        text_auto=".2f",
        title="Average Operational Load by Day Type (%)",
        labels={"Average_Load": "Average Load (%)", "Day Type": "Day Classification"},
        color="Day Type",
        color_discrete_map={"Weekday": "#3b82f6", "Weekend": "#f59e0b"},
        template="plotly_dark"
    )
    fig_day.update_layout(height=400)
    st.plotly_chart(fig_day, use_container_width=True)

with tab_season:
    seas_df = seasonal_analysis(filtered)
    fig_season = px.bar(
        seas_df,
        x="Season",
        y="Average_Load",
        text_auto=".2f",
        title="Seasonal Operational Load Comparison (%)",
        labels={"Average_Load": "Average Load (%)", "Season": "Season"},
        color="Season",
        color_discrete_sequence=["#60a5fa", "#34d399", "#f87171", "#fbbf24"],
        template="plotly_dark"
    )
    fig_season.update_layout(height=400)
    st.plotly_chart(fig_season, use_container_width=True)

with tab_time:
    time_df = time_period_analysis(filtered)
    fig_time = px.bar(
        time_df,
        x="Time Band",
        y="Average_Load",
        text_auto=".2f",
        title="Operational Load Across Diurnal Periods (%)",
        labels={"Average_Load": "Average Load (%)", "Time Band": "Operational Window"},
        color="Time Band",
        color_discrete_sequence=["#38bdf8", "#fb923c", "#a855f7", "#64748b"],
        template="plotly_dark"
    )
    fig_time.update_layout(height=400)
    st.plotly_chart(fig_time, use_container_width=True)

# ============================================================
# HOURLY HEATMAP
# ============================================================

st.divider()
st.subheader("🔥 Terminal Congestion Heatmap (Day of Week × Hour)")

pivot_heatmap = hourly_heatmap_data(filtered)
if not pivot_heatmap.empty:
    fig_hm = px.imshow(
        pivot_heatmap,
        aspect="auto",
        title="Average Operational Load Index by Day and Hour (%)",
        labels={"x": "Hour of Day (0-23)", "y": "Day of Week", "color": "Load (%)"},
        color_continuous_scale="Viridis",
        template="plotly_dark"
    )
    fig_hm.update_layout(height=450)
    st.plotly_chart(fig_hm, use_container_width=True)

# ============================================================
# YEAR-WISE TREND
# ============================================================

st.divider()
st.subheader("📆 Long-Term Year-Over-Year Operational Trend")

yr_df = yearly_analysis(filtered)
if not yr_df.empty:
    fig_yr = px.line(
        yr_df,
        x="Year",
        y="Average_Load",
        markers=True,
        title="Annualized Mean Operational Load Index (%)",
        labels={"Average_Load": "Average Load (%)"},
        template="plotly_dark"
    )
    fig_yr.update_traces(line_color="#ec4899", marker=dict(size=8))
    fig_yr.update_layout(height=380)
    st.plotly_chart(fig_yr, use_container_width=True)

# ============================================================
# AUTOMATED OPERATIONAL INSIGHTS
# ============================================================

st.divider()
st.subheader("🤖 Automated Operational Insights & Recommendations")

highest_seas = seas_df.loc[seas_df["Average_Load"].idxmax()] if not seas_df.empty else None
highest_day = day_df.loc[day_df["Average_Load"].idxmax()] if not day_df.empty else None
highest_period = time_df.loc[time_df["Average_Load"].idxmax()] if not time_df.empty else None

ins_col1, ins_col2 = st.columns(2)

with ins_col1:
    if highest_seas is not None:
        st.markdown(
            f"🌦️ **Dominant Season:** `{highest_seas['Season']}` holds the highest terminal pressure with an average load of **{highest_seas['Average_Load']:.2f}%**."
        )
    if highest_day is not None:
        st.markdown(
            f"📅 **Peak Day Category:** `{highest_day['Day Type']}` experiences heightened throughput averaging **{highest_day['Average_Load']:.2f}%**."
        )
    if highest_period is not None:
        st.markdown(
            f"🕐 **Peak Time Band:** `{highest_period['Time Band']}` exhibits maximum activity concentration averaging **{highest_period['Average_Load']:.2f}%**."
        )

with ins_col2:
    st.markdown(
        f"🔴 **Congestion Share:** **{kpi_metrics['congestion_percentage']:.2f}%** of analyzed intervals operated under high terminal strain."
    )
    st.markdown(
        f"🔵 **Idle Share:** **{kpi_metrics['idle_percentage']:.2f}%** of analyzed intervals experienced low utilization / idle berths."
    )
    st.markdown(
        f"📈 **Activity Anomalies:** **{spike_count:,}** extreme spike intervals detected requiring dynamic queue management."
    )

# ============================================================
# DATASET SUMMARY & EXPORT
# ============================================================

st.divider()
st.subheader("📋 Dataset Provenance & Export")

s1, s2, s3, s4 = st.columns(4)
with s1:
    st.metric("Total Dataset Rows", f"{len(df):,}")
with s2:
    st.metric("Total Schema Columns", f"{len(df.columns)}")
with s3:
    st.metric("Historical Start Date", str(df["Timestamp"].min().date()))
with s4:
    st.metric("Historical End Date", str(df["Timestamp"].max().date()))

with st.expander("🔍 Preview Filtered Data Records (First 100 Rows)"):
    st.dataframe(filtered.head(100), use_container_width=True)

csv_export = filtered.to_csv(index=False).encode("utf-8")
st.download_button(
    label="📥 Download Filtered Data as CSV",
    data=csv_export,
    file_name="ferry_capacity_analytics_export.csv",
    mime="text/csv",
    help="Export current filtered view for external reporting or spreadsheets."
)

st.divider()
st.caption(
    "Ferry Capacity Utilization & Operational Efficiency Analytics System | Built with Streamlit, Pandas, NumPy, and Plotly"
)
