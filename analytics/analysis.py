from typing import Any, Dict, List, Optional, Tuple
import pandas as pd


def aggregate_data(
    df: pd.DataFrame,
    granularity: str = "15-Minute",
    congestion_threshold: float = 80.0,
    idle_threshold: float = 20.0
) -> pd.DataFrame:
    """
    Aggregate ferry dataset across selected time granularity (15-Minute, Hourly, Daily),
    filter out inactive periods, re-normalize the Operational Load Index (OLI) for that scale,
    compute the Congestion Pressure Index (CPI), and flag Congestion / Sustained Idle states.
    """
    if df.empty:
        return pd.DataFrame()

    data = df.copy()

    if granularity == "15-Minute":
        rule = "15min"
    elif granularity == "Hourly":
        rule = "1h"
    else:  # Daily
        rule = "1D"

    agg_df = (
        data.set_index("Timestamp")
        .resample(rule)
        .agg({
            "Sales Count": "sum",
            "Redemption Count": "sum",
            "Total Activity": "sum"
        })
        .reset_index()
    )

    # Filter out empty/inactive periods
    agg_df = agg_df[agg_df["Total Activity"] > 0].copy()
    if agg_df.empty:
        return agg_df

    # Recalculate 95th percentile normalized OLI at current aggregation scale
    ref = float(agg_df["Total Activity"].quantile(0.95))
    if ref <= 0:
        ref = 1.0

    agg_df["Operational Load Index"] = (
        (agg_df["Total Activity"] / ref) * 100.0
    ).clip(0, 100)

    # Congestion Pressure Index (OLI weighted by redemption proportion)
    redemption_ratio = agg_df["Redemption Count"] / (agg_df["Total Activity"] + 1)
    cpi_raw = agg_df["Operational Load Index"] * redemption_ratio
    cpi_max = cpi_raw.max()
    if cpi_max > 0:
        agg_df["Congestion Pressure Index"] = (cpi_raw / cpi_max) * 100.0
    else:
        agg_df["Congestion Pressure Index"] = 0.0

    # Congestion and Idle flags
    agg_df["Congestion"] = agg_df["Operational Load Index"] >= congestion_threshold
    agg_df["Idle"] = agg_df["Operational Load Index"] <= idle_threshold

    # Sustained Idle indicator (streak >= 3 consecutive idle intervals)
    idle_streak = agg_df["Idle"].astype(int).groupby((~agg_df["Idle"]).cumsum()).cumsum()
    agg_df["Idle Streak"] = idle_streak
    agg_df["Sustained Idle"] = idle_streak >= 3

    return agg_df


def seasonal_analysis(df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute operational efficiency and volume broken down by Season.
    """
    if df.empty:
        return pd.DataFrame()

    season_order = ["Winter", "Spring", "Summer", "Autumn"]
    result = (
        df.groupby("Season", observed=True)
        .agg(
            Average_Activity=("Total Activity", "mean"),
            Total_Activity=("Total Activity", "sum"),
            Average_Load=("Operational Load Index", "mean"),
            Total_Sales=("Sales Count", "sum"),
            Total_Redemptions=("Redemption Count", "sum"),
            Records=("Timestamp", "count")
        )
        .reset_index()
    )

    result["Season"] = pd.Categorical(result["Season"], categories=season_order, ordered=True)
    return result.sort_values("Season").reset_index(drop=True)


def weekday_analysis(df: pd.DataFrame) -> pd.DataFrame:
    """
    Compare operational metrics between Weekday and Weekend.
    """
    if df.empty:
        return pd.DataFrame()

    return (
        df.groupby("Day Type", observed=True)
        .agg(
            Average_Activity=("Total Activity", "mean"),
            Total_Activity=("Total Activity", "sum"),
            Average_Load=("Operational Load Index", "mean"),
            Records=("Timestamp", "count")
        )
        .reset_index()
    )


def time_period_analysis(df: pd.DataFrame) -> pd.DataFrame:
    """
    Analyze operational metrics across Morning, Afternoon, Evening, and Night.
    """
    if df.empty:
        return pd.DataFrame()

    order = ["Morning", "Afternoon", "Evening", "Night"]
    data = df.copy()

    # If Time Band doesn't exist, create it from Hour
    if "Time Band" not in data.columns:
        data["Time Band"] = pd.cut(
            data["Hour"],
            bins=[-1, 11, 16, 20, 24],
            labels=order
        )

    result = (
        data.groupby("Time Band", observed=True)
        .agg(
            Average_Activity=("Total Activity", "mean"),
            Total_Activity=("Total Activity", "sum"),
            Average_Load=("Operational Load Index", "mean"),
            Records=("Timestamp", "count")
        )
        .reset_index()
    )

    result["Time Band"] = pd.Categorical(result["Time Band"], categories=order, ordered=True)
    return result.sort_values("Time Band").reset_index(drop=True)


def hourly_heatmap_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Generate Day of Week x Hour matrix of average Operational Load Index for heatmap visualization.
    """
    if df.empty:
        return pd.DataFrame()

    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    heatmap = (
        df.groupby(["Day of Week", "Hour"], observed=True)["Operational Load Index"]
        .mean()
        .reset_index()
    )

    heatmap["Day of Week"] = pd.Categorical(heatmap["Day of Week"], categories=days, ordered=True)
    pivot = heatmap.pivot(index="Day of Week", columns="Hour", values="Operational Load Index")
    pivot = pivot.reindex(days)
    return pivot


def yearly_analysis(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregate year-over-year operational trends.
    """
    if df.empty:
        return pd.DataFrame()

    return (
        df.groupby("Year", observed=True)
        .agg(
            Average_Activity=("Total Activity", "mean"),
            Total_Activity=("Total Activity", "sum"),
            Average_Load=("Operational Load Index", "mean"),
            Total_Sales=("Sales Count", "sum"),
            Total_Redemptions=("Redemption Count", "sum"),
            Records=("Timestamp", "count")
        )
        .reset_index()
        .sort_values("Year")
        .reset_index(drop=True)
    )


def get_top_congestion_windows(analysis_df: pd.DataFrame, limit: int = 20) -> pd.DataFrame:
    """
    Retrieve highest Congestion Pressure Index windows.
    """
    if analysis_df.empty or "Congestion" not in analysis_df.columns:
        return pd.DataFrame()

    congested = analysis_df[analysis_df["Congestion"]]
    if congested.empty:
        return pd.DataFrame()

    return congested.sort_values("Congestion Pressure Index", ascending=False).head(limit)


def get_top_idle_windows(analysis_df: pd.DataFrame, limit: int = 20) -> pd.DataFrame:
    """
    Retrieve sustained idle periods with lowest load.
    """
    if analysis_df.empty or "Sustained Idle" not in analysis_df.columns:
        return pd.DataFrame()

    idle = analysis_df[analysis_df["Sustained Idle"]]
    if idle.empty:
        return pd.DataFrame()

    return idle.sort_values("Operational Load Index", ascending=True).head(limit)