"""
test_pipeline.py
================
Integration test script to verify API fetching and Pandas transformations.
Run via: python test_pipeline.py
"""

import sys

def run_tests():
    print("Testing WeatherScope Pipeline...")

    try:
        import weather_api
        import utils
    except ImportError as e:
        print(f"FAILED to import modules: {e}")
        return False

    # 1. Test Geocoding API
    print("\n[1/4] Testing search_cities('Paris')...")
    cities = weather_api.search_cities("Paris", count=3)
    if not cities:
        print("FAIL: No cities returned for 'Paris'")
        return False
    print(f"SUCCESS: Found {len(cities)} matches. Top match: {cities[0]['label']} (lat={cities[0]['latitude']}, lon={cities[0]['longitude']})")

    # 2. Test Weather Forecast API
    print("\n[2/4] Testing get_weather_forecast for Paris...")
    paris = cities[0]
    forecast = weather_api.get_weather_forecast(
        latitude=paris["latitude"],
        longitude=paris["longitude"],
        timezone=paris.get("timezone", "auto")
    )
    if "current" not in forecast or "daily" not in forecast or "hourly" not in forecast:
        print(f"FAIL: Missing keys in forecast response: {list(forecast.keys())}")
        return False
    print(f"SUCCESS: Received weather data. Current Temp = {forecast['current'].get('temperature_2m')}°C")

    # 3. Test Pandas Daily Processing
    print("\n[3/4] Testing utils.process_daily_forecast...")
    daily_df = utils.process_daily_forecast(forecast["daily"])
    if daily_df.empty or len(daily_df) < 7:
        print(f"FAIL: daily_df empty or has fewer than 7 days ({len(daily_df)})")
        return False
    print(f"SUCCESS: Daily DataFrame shape = {daily_df.shape}. Columns: {list(daily_df.columns[:6])}...")

    # 4. Test Summary Metrics
    print("\n[4/4] Testing utils.calculate_summary_metrics...")
    metrics = utils.calculate_summary_metrics(daily_df)
    print(f"SUCCESS: Summary metrics = {metrics}")

    print("\n>>> ALL TESTS PASSED SUCCESSFULLY! <<<")
    return True

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
