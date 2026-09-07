from typing import Any, Dict
import pandas as pd


def calculate_peak_strain_duration(
    df: pd.DataFrame,
    congestion_threshold: float = 80.0,
    interval_minutes: int = 15
) -> int:
    """
    Calculate the longest continuous period (in minutes) where
    the Operational Load Index remains above or equal to the congestion threshold.
    """
    if df.empty:
        return 0

    sorted_df = df.sort_values("Timestamp")
    is_congested = (sorted_df["Operational Load Index"] >= congestion_threshold).tolist()

    longest_streak = 0
    current_streak = 0

    for flag in is_congested:
        if flag:
            current_streak += 1
            if current_streak > longest_streak:
                longest_streak = current_streak
        else:
            current_streak = 0

    return longest_streak * interval_minutes


def calculate_kpis(
    df: pd.DataFrame,
    congestion_threshold: float = 80.0,
    idle_threshold: float = 20.0,
    interval_minutes: int = 15
) -> Dict[str, Any]:
    """
    Calculate high-level Key Performance Indicators (KPIs) for ferry capacity:
    - Volume metrics (records, sales, redemptions)
    - Utilization metrics (mean, peak, minimum OLI)
    - Congestion and idle shares
    - Operational variability score
    - Longest peak strain duration
    """
    total_records = len(df)
    if total_records == 0:
        return {
            "total_records": 0,
            "total_sales": 0,
            "total_redemptions": 0,
            "average_activity": 0.0,
            "maximum_activity": 0,
            "minimum_activity": 0,
            "average_oli": 0.0,
            "peak_oli": 0.0,
            "minimum_oli": 0.0,
            "capacity_utilization": 0.0,
            "congestion_count": 0,
            "congestion_percentage": 0.0,
            "idle_count": 0,
            "idle_percentage": 0.0,
            "sustained_idle_count": 0,
            "operational_variability": 0.0,
            "variability_score": 0.0,
            "peak_strain_minutes": 0,
            "peak_strain_text": "0 min",
        }

    total_sales = int(df["Sales Count"].sum())
    total_redemptions = int(df["Redemption Count"].sum())

    activity_col = "Total Activity" if "Total Activity" in df.columns else "Total Activity Load"
    average_activity = float(df[activity_col].mean())
    maximum_activity = int(df[activity_col].max())
    minimum_activity = int(df[activity_col].min())

    average_oli = float(df["Operational Load Index"].mean())
    peak_oli = float(df["Operational Load Index"].max())
    minimum_oli = float(df["Operational Load Index"].min())

    is_congested = df["Operational Load Index"] >= congestion_threshold
    is_idle = df["Operational Load Index"] <= idle_threshold

    congestion_count = int(is_congested.sum())
    idle_count = int(is_idle.sum())

    congestion_percentage = (congestion_count / total_records) * 100.0
    idle_percentage = (idle_count / total_records) * 100.0

    # Sustained idle (3 or more consecutive idle intervals)
    idle_streak = is_idle.astype(int).groupby((~is_idle).cumsum()).cumsum()
    sustained_idle_count = int((idle_streak >= 3).sum())

    # Operational variability
    oli_std = float(df["Operational Load Index"].std()) if total_records > 1 else 0.0
    variability_score = (oli_std / average_oli) if average_oli > 0 else 0.0

    # Peak strain duration
    peak_strain_minutes = calculate_peak_strain_duration(
        df,
        congestion_threshold=congestion_threshold,
        interval_minutes=interval_minutes
    )

    if peak_strain_minutes >= 60:
        peak_strain_text = f"{peak_strain_minutes / 60:.1f} hrs"
    else:
        peak_strain_text = f"{peak_strain_minutes:.0f} min"

    return {
        "total_records": total_records,
        "total_sales": total_sales,
        "total_redemptions": total_redemptions,
        "average_activity": average_activity,
        "maximum_activity": maximum_activity,
        "minimum_activity": minimum_activity,
        "average_oli": average_oli,
        "peak_oli": peak_oli,
        "minimum_oli": minimum_oli,
        "capacity_utilization": average_oli,
        "congestion_count": congestion_count,
        "congestion_percentage": congestion_percentage,
        "idle_count": idle_count,
        "idle_percentage": idle_percentage,
        "sustained_idle_count": sustained_idle_count,
        "operational_variability": oli_std,
        "variability_score": variability_score,
        "peak_strain_minutes": peak_strain_minutes,
        "peak_strain_text": peak_strain_text,
    }