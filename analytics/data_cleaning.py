from pathlib import Path
from typing import Dict, Tuple, Union
import pandas as pd


REQUIRED_COLUMNS = ["_id", "Timestamp", "Redemption Count", "Sales Count"]


def load_and_clean_data(
    file_path: Union[str, Path]
) -> Tuple[pd.DataFrame, Dict[str, int]]:
    """
    Load Toronto Ferry Ticket sales dataset, perform validation,
    compute pre-cleaning data quality flags, and return a clean DataFrame
    along with a comprehensive quality metrics dictionary.
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(
            f"Dataset not found at {path}. Please ensure 'Toronto_Ferry_Terminal_Ticket_Sales.csv' "
            f"is present in the 'data/' directory."
        )

    df = pd.read_csv(path)
    df.columns = df.columns.str.strip()

    missing_cols = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing_cols:
        raise ValueError(f"Missing required columns in dataset: {', '.join(missing_cols)}")

    # Parse numeric and timestamp columns
    raw_sales = pd.to_numeric(df["Sales Count"], errors="coerce")
    raw_redemption = pd.to_numeric(df["Redemption Count"], errors="coerce")
    parsed_timestamps = pd.to_datetime(df["Timestamp"], errors="coerce")

    # Capture data quality statistics BEFORE cleaning
    quality_report = {
        "total_raw_rows": len(df),
        "total_columns": len(df.columns),
        "invalid_timestamps": int(parsed_timestamps.isna().sum()),
        "negative_sales": int((raw_sales < 0).sum()),
        "negative_redemptions": int((raw_redemption < 0).sum()),
        "missing_sales": int(raw_sales.isna().sum()),
        "missing_redemptions": int(raw_redemption.isna().sum()),
        "zero_activity_rows": int(((raw_sales.fillna(0) + raw_redemption.fillna(0)) == 0).sum()),
        "duplicate_ids": int(df.duplicated(subset=["_id"], keep=False).sum()),
        "duplicate_timestamps": int(parsed_timestamps.dropna().duplicated(keep=False).sum()),
    }

    # Store quality flags on dataframe
    df["Original Sales Count"] = raw_sales
    df["Original Redemption Count"] = raw_redemption
    df["Timestamp"] = parsed_timestamps
    df["Invalid Timestamp"] = parsed_timestamps.isna()
    df["Negative Sales"] = raw_sales < 0
    df["Negative Redemption"] = raw_redemption < 0
    df["Zero Activity"] = (raw_sales.fillna(0) + raw_redemption.fillna(0)) == 0
    df["Duplicate ID"] = df.duplicated(subset=["_id"], keep=False)
    df["Duplicate Timestamp"] = parsed_timestamps.duplicated(keep=False)

    # Clean numeric columns: impute missing with 0 and clamp negative values to 0
    df["Sales Count"] = raw_sales.fillna(0).clip(lower=0).astype(int)
    df["Redemption Count"] = raw_redemption.fillna(0).clip(lower=0).astype(int)

    # Filter out rows with unparseable timestamps
    df = df.dropna(subset=["Timestamp"])

    # Sort deterministically by timestamp
    df = df.sort_values("Timestamp").reset_index(drop=True)

    quality_report["clean_rows"] = len(df)

    return df, quality_report


def get_data_quality_report(df: pd.DataFrame) -> Dict[str, int]:
    """
    Generate quality metrics from a processed DataFrame containing quality flags.
    """
    return {
        "total_rows": len(df),
        "total_columns": len(df.columns),
        "invalid_timestamps": int(df["Invalid Timestamp"].sum()) if "Invalid Timestamp" in df else 0,
        "negative_sales": int(df["Negative Sales"].sum()) if "Negative Sales" in df else 0,
        "negative_redemptions": int(df["Negative Redemption"].sum()) if "Negative Redemption" in df else 0,
        "zero_activity": int(df["Zero Activity"].sum()) if "Zero Activity" in df else 0,
        "duplicate_ids": int(df["Duplicate ID"].sum()) if "Duplicate ID" in df else 0,
        "duplicate_timestamps": int(df["Duplicate Timestamp"].sum()) if "Duplicate Timestamp" in df else 0,
    }