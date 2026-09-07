import streamlit as st
import pandas as pd


def render_documentation():
    """
    Render comprehensive bilingual (English + Hindi) documentation.
    """

    st.title(
        "📘 Project Documentation / प्रोजेक्ट डॉक्यूमेंटेशन"
    )

    st.caption(
        "Ferry Capacity Utilization & Operational Efficiency Analytics System"
    )

    st.divider()

    # ========================================================
    # PROJECT OVERVIEW
    # ========================================================

    st.header("🚢 Project Overview / प्रोजेक्ट का परिचय")

    tab1, tab2 = st.tabs([
        "🇬🇧 English",
        "🇮🇳 हिंदी"
    ])

    # --------------------------------------------------------
    # ENGLISH OVERVIEW
    # --------------------------------------------------------

    with tab1:

        st.subheader(
            "Ferry Capacity Utilization & Operational Efficiency Analytics System"
        )

        st.write(
            """
            This project is a data-driven analytical system developed
            to analyse ferry ticket sales and redemption activity.

            The system processes historical timestamp-based ferry
            activity data and transforms raw records into meaningful
            operational indicators.

            The dashboard helps identify high-activity periods,
            congestion-prone intervals, low-activity periods,
            sustained idle periods, seasonal patterns,
            weekday/weekend differences and time-of-day trends.
            """
        )

        st.subheader("🎯 Main Objectives")

        objectives = [
            "Analyse historical ferry ticket activity.",
            "Measure total sales and redemption activity.",
            "Calculate an Operational Load Index.",
            "Identify congestion-prone periods.",
            "Identify low-activity and sustained idle periods.",
            "Detect unusual activity spikes.",
            "Compare weekday and weekend activity.",
            "Analyse seasonal demand patterns.",
            "Analyse morning, afternoon, evening and night activity.",
            "Provide an interactive analytical dashboard."
        ]

        for objective in objectives:
            st.markdown(f"✅ {objective}")

    # --------------------------------------------------------
    # HINDI OVERVIEW
    # --------------------------------------------------------

    with tab2:

        st.subheader(
            "फेरी क्षमता उपयोग एवं परिचालन दक्षता विश्लेषण प्रणाली"
        )

        st.write(
            """
            यह परियोजना फेरी टिकट बिक्री और रिडेम्पशन गतिविधि
            का डेटा-आधारित विश्लेषण करने के लिए विकसित की गई है।

            सिस्टम historical timestamp-based ferry activity data
            को process करके raw records को meaningful operational
            indicators में बदलता है।

            Dashboard के माध्यम से अधिक activity वाले समय,
            congestion-prone periods, low-activity periods,
            sustained idle periods, seasonal patterns,
            weekday/weekend differences और time-of-day trends
            को समझा जा सकता है।
            """
        )

        st.subheader("🎯 मुख्य उद्देश्य")

        objectives_hindi = [
            "Historical ferry ticket activity का विश्लेषण करना।",
            "Sales और redemption activity को measure करना।",
            "Operational Load Index calculate करना।",
            "Congestion-prone periods की पहचान करना।",
            "Low-activity और sustained idle periods की पहचान करना।",
            "Unusual activity spikes detect करना।",
            "Weekday और weekend activity की तुलना करना।",
            "Seasonal demand patterns का विश्लेषण करना।",
            "Morning, afternoon, evening और night activity का विश्लेषण करना।",
            "Interactive analytical dashboard उपलब्ध कराना।"
        ]

        for objective in objectives_hindi:
            st.markdown(f"✅ {objective}")

    st.divider()

    # ========================================================
    # TECHNOLOGY STACK
    # ========================================================

    st.header("💻 Technology Stack / प्रयुक्त Technologies")

    st.write(
        """
        The following technologies are used in the implementation
        of this analytical system.
        """
    )

    technology_data = pd.DataFrame({
        "Technology": [
            "Python",
            "Streamlit",
            "Pandas",
            "NumPy",
            "Plotly",
            "CSV",
            "VS Code"
        ],

        "Role in Project": [
            "Main programming language",
            "Interactive dashboard and web application",
            "Data loading, cleaning, transformation and analysis",
            "Numerical calculations and conditional processing",
            "Interactive charts and data visualization",
            "Dataset storage and input format",
            "Development and debugging environment"
        ],

        "Where It Is Used": [
            "Entire app.py application logic",
            "Dashboard UI, sidebar, filters, metrics and tables",
            "pd.read_csv(), data cleaning, groupby(), resample() and aggregations",
            "np.where(), numerical operations and calculations",
            "px.line(), px.bar(), px.imshow(), go.Figure() and charts",
            "Toronto_Ferry_Terminal_Ticket_Sales.csv",
            "Project development and testing"
        ]
    })

    st.dataframe(
        technology_data,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    # ========================================================
    # TECHNOLOGY DETAILS
    # ========================================================

    st.header(
        "🔧 Technology Implementation / Technology का उपयोग"
    )

    with st.expander("🐍 Python — Main Programming Language"):

        st.write(
            """
            Python is the primary programming language of this project.

            It is responsible for the main application logic,
            data processing, calculations, feature engineering,
            analytical operations and dashboard execution.
            """
        )

        st.code(
            """
    import streamlit as st
    import pandas as pd
    import numpy as np
    import plotly.express as px
    import plotly.graph_objects as go
            """,
            language="python"
        )

    with st.expander("📊 Streamlit — Dashboard Development"):

        st.write(
            """
            Streamlit is used to convert the Python analytics into
            an interactive web-based dashboard.

            It is used for:

            • Sidebar filters
            • Date selection
            • Dropdowns
            • KPI cards
            • Tables
            • Charts
            • Download buttons
            • Project documentation
            """
        )

        st.code(
            """
    st.set_page_config(...)
    st.sidebar.checkbox(...)
    st.sidebar.selectbox(...)
    st.sidebar.slider(...)
    st.metric(...)
    st.dataframe(...)
    st.plotly_chart(...)
    st.download_button(...)
            """,
            language="python"
        )

    with st.expander("🐼 Pandas — Data Analysis"):

        st.write(
            """
            Pandas is one of the main analytical libraries used
            in this project.

            It is used for:

            • Reading the CSV dataset
            • Cleaning data
            • Converting timestamps
            • Filtering records
            • Grouping data
            • Resampling data
            • Calculating aggregates
            • Creating analytical features
            """
        )

        st.code(
            """
    df = pd.read_csv(DATA_PATH)

    df["Timestamp"] = pd.to_datetime(
    df["Timestamp"],
    errors="coerce"
    )

    filtered = df[
    (df["Timestamp"] >= start_date) &
    (df["Timestamp"] < end_date)
    ].copy()

    filtered.groupby("Day Type")
            """,
            language="python"
        )

    with st.expander("🔢 NumPy — Numerical Processing"):

        st.write(
            """
            NumPy is used for numerical and conditional operations.

            For example, NumPy is used to classify records as
            weekday or weekend using np.where().
            """
        )

        st.code(
            """
    df["Day Type"] = np.where(
    df["Timestamp"].dt.dayofweek >= 5,
    "Weekend",
    "Weekday"
    )
            """,
            language="python"
        )

    with st.expander("📈 Plotly — Data Visualization"):

        st.write(
            """
            Plotly is used to create interactive visualizations.

            The project uses Plotly for:

            • Operational load timeline
            • Congestion Pressure Index
            • Sales vs Redemption activity
            • Weekday vs Weekend analysis
            • Seasonal analysis
            • Time-of-day analysis
            • Heatmap
            • Year-wise trend
            """
        )

        st.code(
            """
    fig = px.bar(
    day_analysis,
    x="Day Type",
    y="Average_Load"
    )

    st.plotly_chart(
    fig,
    use_container_width=True
    )
            """,
            language="python"
        )

    with st.expander("📄 CSV — Dataset Storage"):

        st.write(
            """
            The ferry activity dataset is stored in CSV format.

            The application loads the dataset using Pandas and
            processes the following important fields:

            • _id
            • Timestamp
            • Sales Count
            • Redemption Count
            """
        )

        st.code(
            """
    DATA_PATH = "data/Toronto_Ferry_Terminal_Ticket_Sales.csv"

    df = pd.read_csv(DATA_PATH)
            """,
            language="python"
        )

    with st.expander("💻 VS Code — Development Environment"):

        st.write(
            """
            Visual Studio Code can be used as the development
            environment for writing, testing and debugging the
            Python and Streamlit application.
            """
        )

    st.divider()

    # ========================================================
    # DATA FLOW
    # ========================================================

    st.header("🔄 Data Processing Flow / Data कैसे Process होता है")

    st.code(
        """
        Ferry Ticket Activity Data
                    ↓
                 CSV File
                    ↓
             Pandas Data Loading
                    ↓
              Data Validation
                    ↓
               Data Cleaning
                    ↓
            Timestamp Processing
                    ↓
             Feature Engineering
                    ↓
          Aggregation & Calculation
                    ↓
       Operational Load Calculation
                    ↓
       Congestion / Idle Detection
                    ↓
          Spike Detection Analysis
                    ↓
          Plotly Visualization
                    ↓
          Streamlit Dashboard
                    ↓
             Business Insights
        """,
        language="text"
    )

    st.divider()

    # ========================================================
    # DATASET
    # ========================================================

    st.header("📁 Dataset / Dataset की जानकारी")

    st.markdown(
        """
        **Dataset File:**

        `Toronto_Ferry_Terminal_Ticket_Sales.csv`

        **Location in Project:**

        `data/Toronto_Ferry_Terminal_Ticket_Sales.csv`
        """
    )

    dataset_columns = pd.DataFrame({
        "Column": [
            "_id",
            "Timestamp",
            "Sales Count",
            "Redemption Count"
        ],

        "Purpose": [
            "Unique record identifier",
            "Date and time of ferry activity",
            "Number of tickets sold",
            "Number of tickets redeemed"
        ]
    })

    st.dataframe(
        dataset_columns,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    # ========================================================
    # DATA QUALITY
    # ========================================================

    st.header("🧹 Data Quality & Validation")

    st.write(
        """
        The application performs several data-quality checks before
        performing the main analysis.
        """
    )

    quality_checks = [
        "Invalid timestamp detection",
        "Negative sales detection",
        "Negative redemption detection",
        "Zero-activity detection",
        "Duplicate ID detection",
        "Duplicate timestamp detection",
        "Irregular 15-minute interval detection",
        "Missing-value handling",
        "Numeric value validation"
    ]

    for check in quality_checks:
        st.markdown(f"🔍 {check}")

    st.divider()

    # ========================================================
    # FEATURE ENGINEERING
    # ========================================================

    st.header("⚙️ Feature Engineering")

    st.write(
        """
        Additional analytical features are generated from the
        original dataset to support deeper analysis.
        """
    )

    features_data = pd.DataFrame({
        "Feature": [
            "Total Activity",
            "Redemption Pressure Ratio",
            "Year",
            "Month",
            "Month Name",
            "Date",
            "Hour",
            "Day of Week",
            "Day Type",
            "Season",
            "Operational Load Index",
            "Rolling Activity Mean",
            "Rolling Activity Std",
            "Spike Upper Limit",
            "Spike Detected"
        ],

        "Purpose": [
            "Combined sales and redemption activity",
            "Measures redemption pressure relative to activity",
            "Year-based analysis",
            "Month-based analysis",
            "Seasonal/month-name analysis",
            "Daily analysis",
            "Time-of-day analysis",
            "Day-based analysis",
            "Weekday vs weekend classification",
            "Season classification",
            "Normalized operational activity indicator",
            "Rolling activity baseline",
            "Rolling activity variability",
            "Upper boundary for spike detection",
            "Identifies unusual activity spikes"
        ]
    })

    st.dataframe(
        features_data,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    # ========================================================
    # ANALYTICS IMPLEMENTED
    # ========================================================

    st.header("📊 Analytics Implemented / किए गए Analytics")

    analytics = [
        "Sales Count Analysis",
        "Redemption Count Analysis",
        "Operational Load Analysis",
        "Congestion Pressure Analysis",
        "Idle Period Analysis",
        "Sustained Idle Detection",
        "Rolling Spike Detection",
        "Weekday vs Weekend Analysis",
        "Seasonal Analysis",
        "Time-of-Day Analysis",
        "Day and Hour Heatmap Analysis",
        "Year-wise Trend Analysis",
        "Automated Operational Insights"
    ]

    for item in analytics:
        st.markdown(f"📌 **{item}**")

    st.divider()

    # ========================================================
    # KPI DEFINITIONS
    # ========================================================

    st.header("📈 KPI Definitions / KPI का मतलब")

    kpi_data = pd.DataFrame({

        "KPI": [
            "Total Records",
            "Total Sales",
            "Total Redemptions",
            "Operational Utilization",
            "Idle Capacity",
            "Congestion Pressure",
            "Peak Load",
            "Sustained Idle",
            "Peak Strain Duration",
            "Operational Variability Score"
        ],

        "Meaning": [
            "Number of records in the selected analysis period",
            "Total number of recorded sales",
            "Total number of recorded redemptions",
            "Average normalized operational activity",
            "Percentage of analysed intervals below idle threshold",
            "Percentage of analysed intervals classified as congestion",
            "Highest normalized operational load",
            "Number of intervals forming sustained idle periods",
            "Estimated duration of congestion intervals",
            "Relative variability of operational load"
        ]
    })

    st.dataframe(
        kpi_data,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    # ========================================================
    # METHODOLOGY
    # ========================================================

    st.header("⚙️ Methodology / कार्यप्रणाली")

    methodology = [
        "Data ingestion",
        "Data validation",
        "Data cleaning",
        "Timestamp conversion",
        "Feature engineering",
        "15-minute / hourly / daily aggregation",
        "Operational Load Index calculation",
        "Congestion Pressure Index calculation",
        "Congestion detection",
        "Idle-period detection",
        "Sustained idle detection",
        "Rolling spike detection",
        "Seasonal analysis",
        "Weekday/weekend analysis",
        "Time-of-day analysis",
        "Visualization",
        "Automated insight generation"
    ]

    for i, step in enumerate(methodology, start=1):
        st.markdown(f"**{i}.** {step}")

    st.divider()

    # ========================================================
    # DASHBOARD FEATURES
    # ========================================================

    st.header("🎨 Dashboard Features")

    dashboard_features = [
        "Interactive date range filtering",
        "Season filtering",
        "Weekday / weekend filtering",
        "15-minute, hourly and daily granularity",
        "Adjustable congestion threshold",
        "Adjustable idle threshold",
        "KPI cards",
        "Data quality monitoring",
        "Irregular interval detection",
        "Rolling spike detection",
        "Operational utilization timeline",
        "Congestion Pressure Index chart",
        "Sales vs Redemption chart",
        "Congestion period table",
        "Sustained idle period table",
        "Weekday vs Weekend comparison",
        "Seasonal comparison",
        "Time-of-day analysis",
        "Day-hour heatmap",
        "Year-wise trend",
        "Automated operational insights",
        "Filtered dataset export"
    ]

    for feature in dashboard_features:
        st.markdown(f"🔹 {feature}")

    st.divider()

    # ========================================================
    # PROJECT CONTRIBUTION
    # ========================================================

    st.header("👨‍💻 Project Contribution / Project में मेरा योगदान")

    contribution = [
        "Project problem identification",
        "Dataset integration",
        "Data preprocessing",
        "Data-quality validation",
        "Feature engineering",
        "Analytical metric development",
        "Operational load calculation",
        "Congestion and idle detection",
        "Spike detection",
        "Interactive dashboard development",
        "Data visualization",
        "Automated insight generation",
        "Data export functionality",
        "Testing and debugging",
        "Project documentation"
    ]

    for item in contribution:
        st.markdown(f"✔️ {item}")

    st.divider()

    # ========================================================
    # IMPORTANT METHODOLOGICAL NOTE
    # ========================================================

    st.header("⚠️ Important Methodological Note")

    st.warning(
        """
        The Operational Load Index is an activity-based normalized
        operational pressure indicator.

        It does NOT represent actual passenger occupancy because
        vessel-level passenger capacity is not available in the
        supplied dataset.

        Similarly, direct operational cost efficiency cannot be
        calculated from the current dataset because operating-cost
        information is not available.
        """
    )

    st.divider()

    # ========================================================
    # BUSINESS VALUE
    # ========================================================

    st.header("💼 Business Value / व्यावसायिक उपयोग")

    benefits = [
        "Better understanding of ferry demand patterns",
        "Identification of congestion-prone periods",
        "Identification of low-activity periods",
        "Better operational planning",
        "Improved scheduling decisions",
        "Seasonal planning support",
        "Identification of unusual demand spikes",
        "Data-driven operational decision making"
    ]

    for benefit in benefits:
        st.markdown(f"💡 {benefit}")

    st.divider()

    # ========================================================
    # FUTURE SCOPE
    # ========================================================

    st.header("🔮 Future Scope / भविष्य में सुधार")

    future_scope = [
        "Actual vessel capacity integration",
        "Passenger count integration",
        "Route information",
        "Vessel assignment information",
        "Staffing information",
        "Operating cost information",
        "Weather conditions",
        "Special event information",
        "Real-time operational data",
        "Predictive demand forecasting",
        "Machine-learning based demand prediction"
    ]

    for item in future_scope:
        st.markdown(f"🚀 {item}")

    st.divider()

    # ========================================================
    # PROJECT SUMMARY
    # ========================================================

    st.header("📌 Project Summary / संक्षिप्त सारांश")

    st.success(
        """
        This project demonstrates how raw ferry ticket activity
        data can be transformed into meaningful operational insights.

        Python is used for application logic and analytics,
        Pandas for data processing, NumPy for numerical operations,
        Plotly for interactive visualization and Streamlit for
        building the final analytical dashboard.

        The system provides an interactive approach for analysing
        ferry activity, identifying operational pressure,
        detecting idle periods and understanding demand patterns.
        """
    )

    st.info(
        """
        हिंदी में:

        यह परियोजना दिखाती है कि raw ferry ticket activity data
        को data processing, analytics और visualization की सहायता
        से meaningful operational insights में बदला जा सकता है।

        Python, Pandas, NumPy, Plotly और Streamlit का उपयोग करके
        एक interactive analytical dashboard तैयार किया गया है।
        """
    )

    st.divider()

    st.caption(
        "⛴️ Ferry Capacity Utilization & Operational Efficiency Analytics System"
    )

    st.caption(
        "Technology Stack: Python • Streamlit • Pandas • NumPy • Plotly • CSV"
    )
