"""
utils.py
========
Helper functions and data processing utilities for the Weather Forecast Dashboard.
Includes WMO weather code mapping and Pandas transformations.
"""

from typing import Dict, Tuple, Any
import pandas as pd
from datetime import datetime

# WMO Weather Interpretation Codes (WW)
# Source: World Meteorological Organization & Open-Meteo documentation
WMO_WEATHER_CODES: Dict[int, Dict[str, str]] = {
    0: {"desc": "Clear sky", "day_icon": "☀️", "night_icon": "🌙"},
    1: {"desc": "Mainly clear", "day_icon": "🌤️", "night_icon": "🌤️"},
    2: {"desc": "Partly cloudy", "day_icon": "⛅", "night_icon": "☁️"},
    3: {"desc": "Overcast", "day_icon": "☁️", "night_icon": "☁️"},
    45: {"desc": "Foggy", "day_icon": "🌫️", "night_icon": "🌫️"},
    48: {"desc": "Depositing rime fog", "day_icon": "🌫️", "night_icon": "🌫️"},
    51: {"desc": "Light drizzle", "day_icon": "🌦️", "night_icon": "🌧️"},
    53: {"desc": "Moderate drizzle", "day_icon": "🌦️", "night_icon": "🌧️"},
    55: {"desc": "Dense drizzle", "day_icon": "🌧️", "night_icon": "🌧️"},
    56: {"desc": "Light freezing drizzle", "day_icon": "🌧️❄️", "night_icon": "🌧️❄️"},
    57: {"desc": "Dense freezing drizzle", "day_icon": "🌧️❄️", "night_icon": "🌧️❄️"},
    61: {"desc": "Slight rain", "day_icon": "🌦️", "night_icon": "🌧️"},
    63: {"desc": "Moderate rain", "day_icon": "🌧️", "night_icon": "🌧️"},
    65: {"desc": "Heavy rain", "day_icon": "🌧️🌧️", "night_icon": "🌧️🌧️"},
    66: {"desc": "Light freezing rain", "day_icon": "🌨️", "night_icon": "🌨️"},
    67: {"desc": "Heavy freezing rain", "day_icon": "🌨️", "night_icon": "🌨️"},
    71: {"desc": "Slight snow fall", "day_icon": "❄️", "night_icon": "❄️"},
    73: {"desc": "Moderate snow fall", "day_icon": "❄️❄️", "night_icon": "❄️❄️"},
    75: {"desc": "Heavy snow fall", "day_icon": "🌨️", "night_icon": "🌨️"},
    77: {"desc": "Snow grains", "day_icon": "🌨️", "night_icon": "🌨️"},
    80: {"desc": "Slight rain showers", "day_icon": "🌦️", "night_icon": "🌧️"},
    81: {"desc": "Moderate rain showers", "day_icon": "🌧️", "night_icon": "🌧️"},
    82: {"desc": "Violent rain showers", "day_icon": "⛈️", "night_icon": "⛈️"},
    85: {"desc": "Slight snow showers", "day_icon": "🌨️", "night_icon": "🌨️"},
    86: {"desc": "Heavy snow showers", "day_icon": "🌨️❄️", "night_icon": "🌨️❄️"},
    95: {"desc": "Thunderstorm", "day_icon": "⛈️", "night_icon": "⛈️"},
    96: {"desc": "Thunderstorm with slight hail", "day_icon": "⛈️🌨️", "night_icon": "⛈️🌨️"},
    99: {"desc": "Thunderstorm with heavy hail", "day_icon": "⛈️🌨️", "night_icon": "⛈️🌨️"},
}


def get_weather_info(code: int, is_day: int = 1) -> Tuple[str, str]:
    """
    Map WMO weather code to human-readable description and appropriate emoji icon.

    Args:
        code: Integer WMO weather code.
        is_day: 1 for daytime, 0 for nighttime.

    Returns:
        Tuple of (description, emoji_icon).
    """
    info = WMO_WEATHER_CODES.get(int(code), {"desc": "Unknown", "day_icon": "🌤️", "night_icon": "🌤️"})
    icon = info["day_icon"] if is_day == 1 else info["night_icon"]
    return info["desc"], icon


def process_daily_forecast(daily_raw: Dict[str, Any]) -> pd.DataFrame:
    """
    Process raw daily forecast dictionary from Open-Meteo into a clean Pandas DataFrame.

    Args:
        daily_raw: Raw dictionary from response['daily'].

    Returns:
        pd.DataFrame with processed dates, day names, weather info, and temperatures.
    """
    df = pd.DataFrame(daily_raw)

    if df.empty or "time" not in df.columns:
        return pd.DataFrame()

    # Convert time string to pandas datetime
    df["date"] = pd.to_datetime(df["time"])

    # Determine day labels (e.g., 'Today', 'Tomorrow', 'Fri, Oct 24')
    today_date = pd.Timestamp.now().normalize().date()
    
    def format_day_label(dt: pd.Timestamp) -> str:
        d = dt.date()
        if d == today_date:
            return "Today"
        elif d == today_date + pd.Timedelta(days=1):
            return "Tomorrow"
        else:
            return dt.strftime("%a, %b %d")

    df["day_label"] = df["date"].apply(format_day_label)
    df["day_name_short"] = df["date"].dt.strftime("%a")
    df["date_formatted"] = df["date"].dt.strftime("%b %d")

    # Map weather code to description and icon
    weather_meta = df["weather_code"].apply(lambda code: get_weather_info(code, is_day=1))
    df["weather_desc"] = [m[0] for m in weather_meta]
    df["weather_icon"] = [m[1] for m in weather_meta]

    # Ensure numeric columns are rounded cleanly
    for col in ["temperature_2m_max", "temperature_2m_min", "apparent_temperature_max", 
                "apparent_temperature_min", "precipitation_sum", "precipitation_probability_max", 
                "wind_speed_10m_max", "uv_index_max"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").round(1)

    return df


def process_hourly_forecast(hourly_raw: Dict[str, Any], current_time_str: str = None, hours_ahead: int = 24) -> pd.DataFrame:
    """
    Process raw hourly forecast into a 24-hour forecast window DataFrame.

    Args:
        hourly_raw: Raw dictionary from response['hourly'].
        current_time_str: Current timestamp from the API response (e.g., '2026-10-23T19:00').
        hours_ahead: Number of upcoming hours to include.

    Returns:
        pd.DataFrame with hourly forecasts.
    """
    df = pd.DataFrame(hourly_raw)
    if df.empty or "time" not in df.columns:
        return pd.DataFrame()

    df["datetime"] = pd.to_datetime(df["time"])

    # Filter from current time or first record
    if current_time_str:
        try:
            curr_dt = pd.to_datetime(current_time_str)
            df = df[df["datetime"] >= curr_dt].copy()
        except Exception:
            pass

    # Slice to desired hours ahead
    df = df.head(hours_ahead).copy()

    # Format display time e.g., '7 PM', '12 AM'
    df["time_label"] = df["datetime"].dt.strftime("%I %p").str.lstrip("0")

    # Map weather code
    weather_meta = df["weather_code"].apply(lambda code: get_weather_info(code, is_day=1))
    df["weather_desc"] = [m[0] for m in weather_meta]
    df["weather_icon"] = [m[1] for m in weather_meta]

    for col in ["temperature_2m", "relative_humidity_2m", "apparent_temperature", 
                "precipitation_probability", "precipitation", "wind_speed_10m"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").round(1)

    return df


def calculate_summary_metrics(daily_df: pd.DataFrame, temp_unit: str = "°C", precip_unit: str = "mm") -> Dict[str, Any]:
    """
    Calculate high-level weekly analytics metrics from the daily forecast DataFrame.

    Args:
        daily_df: Processed 7-day forecast DataFrame.
        temp_unit: Unit string ('°C' or '°F').
        precip_unit: Unit string ('mm' or 'inch').

    Returns:
        Dictionary of key metrics for display.
    """
    if daily_df.empty:
        return {}

    avg_max_temp = daily_df["temperature_2m_max"].mean()
    avg_min_temp = daily_df["temperature_2m_min"].mean()

    # Warmest and coolest day
    warmest_idx = daily_df["temperature_2m_max"].idxmax()
    warmest_day = daily_df.loc[warmest_idx]

    coolest_idx = daily_df["temperature_2m_min"].idxmin()
    coolest_day = daily_df.loc[coolest_idx]

    # Precipitation analytics
    total_rain = daily_df["precipitation_sum"].sum() if "precipitation_sum" in daily_df.columns else 0.0
    rainy_days_count = int((daily_df["precipitation_sum"] > 0.5).sum()) if "precipitation_sum" in daily_df.columns else 0

    rainiest_idx = daily_df["precipitation_sum"].idxmax() if "precipitation_sum" in daily_df.columns else None
    rainiest_day = daily_df.loc[rainiest_idx] if rainiest_idx is not None else None

    # Max wind speed
    max_wind = daily_df["wind_speed_10m_max"].max() if "wind_speed_10m_max" in daily_df.columns else 0.0

    return {
        "avg_max_temp": f"{avg_max_temp:.1f}{temp_unit}",
        "avg_min_temp": f"{avg_min_temp:.1f}{temp_unit}",
        "warmest_day": f"{warmest_day['day_label']} ({warmest_day['temperature_2m_max']:.1f}{temp_unit})",
        "coolest_day": f"{coolest_day['day_label']} ({coolest_day['temperature_2m_min']:.1f}{temp_unit})",
        "total_rain": f"{total_rain:.1f} {precip_unit}",
        "rainy_days_count": f"{rainy_days_count} of {len(daily_df)} days",
        "rainiest_day": f"{rainiest_day['day_label']} ({rainiest_day['precipitation_sum']:.1f} {precip_unit})" if rainiest_day is not None and rainiest_day['precipitation_sum'] > 0 else "None expected",
        "max_wind": f"{max_wind:.1f}"
    }
