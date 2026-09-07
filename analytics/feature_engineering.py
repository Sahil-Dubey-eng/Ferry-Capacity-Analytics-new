import numpy as np
import pandas as pd


def get_season(month: int) -> str:
    """
    Map calendar month to season:
    Dec, Jan, Feb -> Winter
    Mar, Apr, May -> Spring
    Jun, Jul, Aug -> Summer
    Sep, Oct, Nov -> Autumn
    """
    if month in (12, 1, 2):
        return "Winter"
    if month in (3, 4, 5):
        return "Spring"
    if month in (6, 7, 8):
        return "Summer"
    return "Autumn"


def get_time_period(hour: int) -> str:
    """
    Map hour of day to operational time band:
    05:00 - 11:59 -> Morning
    12:00 - 16:59 -> Afternoon
    17:00 - 20:59 -> Evening
    21:00 - 04:59 -> Night
    """
    if 5 <= hour < 12:
        return "Morning"
    if 12 <= hour < 17:
        return "Afternoon"
    if 17 <= hour < 21:
        return "Evening"
    return "Night"


def get_efficiency_status(oli: float) -> str:
    """
    Categorize Operational Load Index into operational state.
    """
    if oli >= 80:
        return "High Pressure"
    if oli <= 20:
        return "Idle"
    if oli >= 50:
        return "Normal"
    return "Low Utilization"


def create_features(
    df: pd.DataFrame,
    quantile_ref: float = 0.95,
    rolling_window: int = 8
) -> pd.DataFrame:
    """
    Compute domain analytical features for ferry capacity and demand analysis:
    1. Total Activity & Redemption Pressure Ratio
    2. Operational Load Index (OLI) normalized by 95th percentile baseline
    3. Calendar & temporal attributes (Season, Day Type, Time Band)
    4. Rolling baseline statistics & extreme activity spike detection
    5. Operational efficiency classification
    """
    df = df.copy()

    # 1. Activity metrics
    df["Total Activity"] = df["Sales Count"] + df["Redemption Count"]
    df["Total Activity Load"] = df["Total Activity"]  # Backward compatibility

    # Pressure ratio bounded in [0, 1]
    df["Redemption Pressure Ratio"] = (
        df["Redemption Count"] / (df["Total Activity"] + 1)
    )

    # 2. Operational Load Index (OLI)
    # Using 95th percentile avoids skew from rare anomalies (e.g. bulk resets)
    ref = float(df["Total Activity"].quantile(quantile_ref))
    if ref <= 0:
        ref = 1.0

    df["Operational Load Index"] = (
        (df["Total Activity"] / ref) * 100
    ).clip(0, 100)

    # 3. Calendar and temporal features
    df["Date"] = df["Timestamp"].dt.date
    df["Year"] = df["Timestamp"].dt.year
    df["Month"] = df["Timestamp"].dt.month
    df["Month Name"] = df["Timestamp"].dt.month_name()
    df["Day"] = df["Timestamp"].dt.day
    df["Day Name"] = df["Timestamp"].dt.day_name()
    df["Day of Week"] = df["Timestamp"].dt.day_name()
    df["Day Number"] = df["Timestamp"].dt.dayofweek
    df["Hour"] = df["Timestamp"].dt.hour
    df["Minute"] = df["Timestamp"].dt.minute

    # Weekday vs Weekend (Day Type / Week Type)
    df["Day Type"] = np.where(df["Day Number"] >= 5, "Weekend", "Weekday")
    df["Week Type"] = df["Day Type"]

    # Seasonality & operational time periods
    df["Season"] = df["Month"].apply(get_season)
    df["Time Period"] = df["Hour"].apply(get_time_period)
    df["Time Band"] = df["Time Period"]

    # Efficiency status categorization
    df["Efficiency Status"] = df["Operational Load Index"].apply(get_efficiency_status)

    # 4. Rolling statistics & spike detection (2-hour rolling window at 15m intervals)
    df["Rolling Activity Mean"] = (
        df["Total Activity"].rolling(window=rolling_window, min_periods=3).mean()
    )
    df["Rolling Activity Std"] = (
        df["Total Activity"].rolling(window=rolling_window, min_periods=3).std()
    )
    df["Spike Upper Limit"] = (
        df["Rolling Activity Mean"] + (2 * df["Rolling Activity Std"].fillna(0))
    )
    df["Spike Detected"] = (
        (df["Total Activity"] > df["Spike Upper Limit"]) &
        (df["Total Activity"] > 0)
    ).fillna(False)

    return df