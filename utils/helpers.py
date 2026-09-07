from typing import Any, Optional


def format_number(value: Any) -> str:
    """
    Format a number with comma separators.
    Example: 1234567 -> '1,234,567'
    """
    if value is None:
        return "0"
    try:
        num = float(value)
        return f"{num:,.0f}"
    except (ValueError, TypeError):
        return str(value)


def format_decimal(value: Any, decimals: int = 2) -> str:
    """
    Format a float with comma grouping and a fixed number of decimals.
    Example: 1234.5678 -> '1,234.57'
    """
    if value is None:
        return "0"
    try:
        num = float(value)
        return f"{num:,.{decimals}f}"
    except (ValueError, TypeError):
        return str(value)


def safe_percentage(value: Any, decimals: int = 2) -> str:
    """
    Format numeric value into percentage string.
    Example: 78.432 -> '78.43%'
    """
    if value is None:
        return "0%"
    try:
        num = float(value)
        return f"{num:.{decimals}f}%"
    except (ValueError, TypeError):
        return str(value)


def get_status_icon(status: str) -> str:
    """
    Return appropriate emoji indicator for operational status.
    """
    icons = {
        "High Pressure": "🔴",
        "Normal": "🟢",
        "Low Utilization": "🟡",
        "Idle": "🔵"
    }
    return icons.get(status, "⚪")


def get_status_message(status: str) -> str:
    """
    Return human-readable operational status summary.
    """
    messages = {
        "High Pressure": "Congestion-prone period (heavy ticketing demand)",
        "Normal": "Optimal operational equilibrium",
        "Low Utilization": "Sub-optimal utilization window",
        "Idle": "Sustained idle capacity detected"
    }
    return messages.get(status, "Standard operating window")