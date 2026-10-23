"""
weather_api.py
==============
Module for interacting with the Open-Meteo API.
Handles city geocoding (finding coordinates) and fetching weather forecast data.
Does not require any API keys.
"""

from typing import Any, Dict, List, Optional
import requests

GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"


def search_cities(query: str, count: int = 5) -> List[Dict[str, Any]]:
    """
    Search for cities matching the given query string using Open-Meteo Geocoding API.

    Args:
        query: Name of the city to search for (e.g., 'London', 'Mumbai').
        count: Maximum number of search results to return.

    Returns:
        List of dictionaries with city details (name, country, admin1, lat, lon, timezone).
    """
    clean_query = query.strip()
    if not clean_query or len(clean_query) < 2:
        return []

    params = {
        "name": clean_query,
        "count": count,
        "language": "en",
        "format": "json"
    }

    try:
        response = requests.get(GEOCODING_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        results = data.get("results", [])
        formatted_results = []
        for item in results:
            # Build a human-friendly label like "Mumbai, Maharashtra, India"
            name = item.get("name", "")
            admin1 = item.get("admin1", "")
            country = item.get("country", "")
            
            parts = [name]
            if admin1 and admin1 != name:
                parts.append(admin1)
            if country:
                parts.append(country)
            display_label = ", ".join(parts)

            formatted_results.append({
                "label": display_label,
                "name": name,
                "country": country,
                "admin1": admin1,
                "country_code": item.get("country_code", ""),
                "latitude": item.get("latitude"),
                "longitude": item.get("longitude"),
                "timezone": item.get("timezone", "auto")
            })

        return formatted_results

    except requests.exceptions.Timeout:
        raise RuntimeError("Geocoding request timed out. Please check your internet connection.")
    except requests.exceptions.ConnectionError:
        raise RuntimeError("Network error: Could not reach Open-Meteo Geocoding API.")
    except requests.exceptions.HTTPError as http_err:
        raise RuntimeError(f"HTTP error during city search: {http_err}")
    except Exception as err:
        raise RuntimeError(f"Unexpected error while searching for city: {err}")


def get_weather_forecast(
    latitude: float,
    longitude: float,
    timezone: str = "auto",
    temperature_unit: str = "celsius",
    wind_speed_unit: str = "kmh",
    precipitation_unit: str = "mm"
) -> Dict[str, Any]:
    """
    Fetch current, hourly, and 7-day daily weather forecast from Open-Meteo API.

    Args:
        latitude: Latitude of the location.
        longitude: Longitude of the location.
        timezone: Timezone string (e.g., 'Asia/Kolkata', 'Europe/London') or 'auto'.
        temperature_unit: 'celsius' or 'fahrenheit'.
        wind_speed_unit: 'kmh' or 'mph'.
        precipitation_unit: 'mm' or 'inch'.

    Returns:
        Dictionary containing raw API response with 'current', 'hourly', and 'daily' datasets.
    """
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "timezone": timezone,
        "temperature_unit": temperature_unit,
        "wind_speed_unit": wind_speed_unit,
        "precipitation_unit": precipitation_unit,
        "current": ",".join([
            "temperature_2m",
            "relative_humidity_2m",
            "apparent_temperature",
            "is_day",
            "precipitation",
            "rain",
            "weather_code",
            "wind_speed_10m",
            "wind_direction_10m",
            "surface_pressure"
        ]),
        "hourly": ",".join([
            "temperature_2m",
            "relative_humidity_2m",
            "apparent_temperature",
            "precipitation_probability",
            "precipitation",
            "weather_code",
            "wind_speed_10m"
        ]),
        "daily": ",".join([
            "weather_code",
            "temperature_2m_max",
            "temperature_2m_min",
            "apparent_temperature_max",
            "apparent_temperature_min",
            "precipitation_sum",
            "precipitation_probability_max",
            "wind_speed_10m_max",
            "uv_index_max",
            "sunrise",
            "sunset"
        ])
    }

    try:
        response = requests.get(FORECAST_URL, params=params, timeout=12)
        response.raise_for_status()
        return response.json()

    except requests.exceptions.Timeout:
        raise RuntimeError("Weather forecast request timed out. Please try again.")
    except requests.exceptions.ConnectionError:
        raise RuntimeError("Network error: Could not reach Open-Meteo Forecast API.")
    except requests.exceptions.HTTPError as http_err:
        raise RuntimeError(f"HTTP error during forecast fetch: {http_err}")
    except Exception as err:
        raise RuntimeError(f"Unexpected error while fetching weather data: {err}")
