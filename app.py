"""
app.py
======
WeatherScope - Interactive Weather Forecast Web Application
Built with Streamlit, Pandas, Plotly, and the Open-Meteo API.
Ideal for Data Analytics Portfolio / BTech Showcase.
"""

from typing import List, Dict, Any, Optional
import datetime
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
st.markdown("""
<style>
#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    visibility: hidden;
}
</style>
""", unsafe_allow_html=True)
# Local modules
import weather_api
import utils

# ---------------------------------------------------------
# 1. Streamlit Page Configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="WeatherScope | Live Weather & 7-Day Forecast",
    page_icon="⛅",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# 2. Custom CSS for Modern, Responsive UI
# ---------------------------------------------------------
st.markdown("""
<style>
    /* Global styling */
    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2.5rem;
    }
    
    /* Hero Current Weather Card */
    .hero-card {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        color: #ffffff;
        border-radius: 16px;
        padding: 24px 28px;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
        margin-bottom: 24px;
        display: flex;
        flex-wrap: wrap;
        justify-content: space-between;
        align-items: center;
    }
    .hero-title {
        font-size: 1.8rem;
        font-weight: 700;
        margin-bottom: 4px;
    }
    .hero-subtitle {
        font-size: 0.95rem;
        opacity: 0.85;
        margin-bottom: 16px;
    }
    .hero-temp {
        font-size: 3.6rem;
        font-weight: 800;
        line-height: 1;
        letter-spacing: -1px;
    }
    .hero-condition {
        font-size: 1.25rem;
        font-weight: 600;
        margin-top: 8px;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .hero-badge {
        display: inline-block;
        background: rgba(255, 255, 255, 0.2);
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 500;
        margin-top: 10px;
    }

    /* Metric Card Styling */
    .metric-card {
        background-color: var(--secondary-background-color, #f8f9fa);
        border: 1px solid rgba(128, 128, 128, 0.15);
        border-radius: 12px;
        padding: 16px;
        text-align: center;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
    }
    .metric-icon {
        font-size: 1.5rem;
        margin-bottom: 4px;
    }
    .metric-label {
        font-size: 0.82rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        opacity: 0.75;
    }
    .metric-value {
        font-size: 1.45rem;
        font-weight: 700;
        margin-top: 4px;
    }

    /* Forecast Daily Cards */
    .forecast-card {
        background-color: var(--secondary-background-color, #f8f9fa);
        border: 1px solid rgba(128, 128, 128, 0.18);
        border-radius: 14px;
        padding: 14px 10px;
        text-align: center;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.04);
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    .forecast-day {
        font-size: 0.95rem;
        font-weight: 700;
        margin-bottom: 2px;
    }
    .forecast-date {
        font-size: 0.78rem;
        opacity: 0.7;
        margin-bottom: 8px;
    }
    .forecast-icon {
        font-size: 2.2rem;
        margin: 6px 0;
    }
    .forecast-desc {
        font-size: 0.8rem;
        font-weight: 500;
        min-height: 2.2rem;
        display: flex;
        align-items: center;
        justify-content: center;
        opacity: 0.9;
        line-height: 1.15;
    }
    .forecast-temps {
        margin-top: 8px;
        font-size: 0.95rem;
        font-weight: 700;
    }
    .forecast-rain {
        margin-top: 6px;
        font-size: 0.75rem;
        font-weight: 600;
        color: #0284c7;
        background: rgba(2, 132, 199, 0.12);
        padding: 2px 6px;
        border-radius: 8px;
        display: inline-block;
    }

    /* Footer */
    .footer-text {
        text-align: center;
        font-size: 0.85rem;
        opacity: 0.7;
        padding: 20px 0;
        border-top: 1px solid rgba(128, 128, 128, 0.2);
        margin-top: 40px;
    }
</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------------
# 3. Cached Data Fetching
# ---------------------------------------------------------
@st.cache_data(ttl=600, show_spinner=False)
def cached_search_cities(query: str) -> List[Dict[str, Any]]:
    """Cached geocoding search to prevent redundant requests."""
    return weather_api.search_cities(query, count=5)


@st.cache_data(ttl=600, show_spinner=False)
def cached_weather_forecast(lat: float, lon: float, timezone: str, temp_unit: str, wind_unit: str, precip_unit: str) -> Dict[str, Any]:
    """Cached forecast fetcher (10-minute cache)."""
    return weather_api.get_weather_forecast(
        latitude=lat,
        longitude=lon,
        timezone=timezone,
        temperature_unit=temp_unit,
        wind_speed_unit=wind_unit,
        precipitation_unit=precip_unit
    )


# ---------------------------------------------------------
# 4. Popular Preset Cities for Instant Selection
# ---------------------------------------------------------
POPULAR_CITIES: Dict[str, Dict[str, Any]] = {
    "London": {
        "label": "London, Greater London, United Kingdom",
        "name": "London",
        "country": "United Kingdom",
        "latitude": 51.5085,
        "longitude": -0.1257,
        "timezone": "Europe/London"
    },
    "New York": {
        "label": "New York, New York, United States",
        "name": "New York",
        "country": "United States",
        "latitude": 40.7143,
        "longitude": -74.0060,
        "timezone": "America/New_York"
    },
    "Tokyo": {
        "label": "Tokyo, Tokyo, Japan",
        "name": "Tokyo",
        "country": "Japan",
        "latitude": 35.6895,
        "longitude": 139.6917,
        "timezone": "Asia/Tokyo"
    },
    "Mumbai": {
        "label": "Mumbai, Maharashtra, India",
        "name": "Mumbai",
        "country": "India",
        "latitude": 19.0728,
        "longitude": 72.8826,
        "timezone": "Asia/Kolkata"
    },
    "Paris": {
        "label": "Paris, Île-de-France, France",
        "name": "Paris",
        "country": "France",
        "latitude": 48.8534,
        "longitude": 2.3488,
        "timezone": "Europe/Paris"
    },
    "Sydney": {
        "label": "Sydney, New South Wales, Australia",
        "name": "Sydney",
        "country": "Australia",
        "latitude": -33.8678,
        "longitude": 151.2073,
        "timezone": "Australia/Sydney"
    }
}

# ---------------------------------------------------------
# 5. Session State Management
# ---------------------------------------------------------
if "selected_city_label" not in st.session_state:
    st.session_state["selected_city_label"] = POPULAR_CITIES["London"]["label"]
if "selected_city_meta" not in st.session_state:
    st.session_state["selected_city_meta"] = POPULAR_CITIES["London"]


# ---------------------------------------------------------
# 6. Sidebar Controls & Settings
# ---------------------------------------------------------
with st.sidebar:
    st.markdown("### 🌦️ WeatherScope")
    st.caption("Live Weather & 7-Day Forecasting Dashboard")
    st.markdown("---")

    # City Search Input
    city_input = st.text_input(
        "🔍 Search Any City",
        value="",
        placeholder="e.g. Berlin, Toronto, Dubai...",
        help="Type any city name and press Enter to search."
    )

    # Quick City Shortcuts
    st.markdown("##### 📍 Popular Destinations")
    quick_cols = st.columns(3)
    quick_city_names = list(POPULAR_CITIES.keys())
    for i, city_name in enumerate(quick_city_names):
        col = quick_cols[i % 3]
        if col.button(city_name, key=f"quick_{city_name}", use_container_width=True):
            st.session_state["selected_city_label"] = POPULAR_CITIES[city_name]["label"]
            st.session_state["selected_city_meta"] = POPULAR_CITIES[city_name]
            st.rerun()

    # Handle Geocoding Search when user types in search box
    if city_input:
        with st.spinner(f"Searching for '{city_input}'..."):
            try:
                candidates = cached_search_cities(city_input)
                if candidates:
                    candidate_labels = [c["label"] for c in candidates]
                    selected_label = st.selectbox(
                        "Select Matching Location:",
                        options=candidate_labels,
                        index=0
                    )
                    # Find selected candidate object
                    selected_match = next((c for c in candidates if c["label"] == selected_label), candidates[0])
                    if st.session_state["selected_city_label"] != selected_match["label"]:
                        st.session_state["selected_city_label"] = selected_match["label"]
                        st.session_state["selected_city_meta"] = selected_match
                        st.rerun()
                else:
                    st.warning(f"No matching locations found for '{city_input}'. Please check spelling.")
            except Exception as e:
                st.error(f"Search failed: {e}")

    st.markdown("---")
    st.markdown("##### ⚙️ Units & Preferences")

    temp_selection = st.radio(
        "Temperature Unit",
        options=["Celsius (°C)", "Fahrenheit (°F)"],
        index=0,
        horizontal=True
    )
    temp_unit_api = "celsius" if "Celsius" in temp_selection else "fahrenheit"
    temp_symbol = "°C" if temp_unit_api == "celsius" else "°F"

    wind_selection = st.radio(
        "Wind Speed Unit",
        options=["km/h", "mph"],
        index=0,
        horizontal=True
    )
    wind_unit_api = "kmh" if wind_selection == "km/h" else "mph"

    precip_selection = st.radio(
        "Precipitation Unit",
        options=["Millimeters (mm)", "Inches (inch)"],
        index=0,
        horizontal=True
    )
    precip_unit_api = "mm" if "Millimeters" in precip_selection else "inch"
    precip_symbol = "mm" if precip_unit_api == "mm" else "in"

    st.markdown("---")
    # Refresh Button
    if st.button("🔄 Refresh Weather Data", use_container_width=True):
        st.cache_data.clear()
        st.toast("Weather data cache refreshed!", icon="✅")

    # Project Info Expander
    with st.expander("ℹ️ About this Project"):
        st.markdown("""
        **WeatherScope Dashboard**
        - Built for **BTech / Fresher Portfolio**.
        - **Tech Stack**: Python, Streamlit, Pandas, Plotly.
        - **API**: Open-Meteo API (Free, No API Key required).
        - **Data Handling**: Pandas DataFrames for aggregation & summary analytics.
        """)


# ---------------------------------------------------------
# 6. Fetch & Process Weather Data
# ---------------------------------------------------------
active_city = st.session_state["selected_city_meta"]

try:
    with st.spinner(f"Loading weather data for {active_city['name']}..."):
        weather_data = cached_weather_forecast(
            lat=active_city["latitude"],
            lon=active_city["longitude"],
            timezone=active_city.get("timezone", "auto"),
            temp_unit=temp_unit_api,
            wind_unit=wind_unit_api,
            precip_unit=precip_unit_api
        )
except Exception as exc:
    st.error(f"⚠️ Unable to fetch weather data: {exc}")
    st.info("Please check your internet connection or try refreshing.")
    st.stop()

# Extract API datasets
current = weather_data.get("current", {})
daily_raw = weather_data.get("daily", {})
hourly_raw = weather_data.get("hourly", {})

# Process with Pandas
daily_df = utils.process_daily_forecast(daily_raw)
hourly_df = utils.process_hourly_forecast(hourly_raw, current_time_str=current.get("time"), hours_ahead=24)
summary_metrics = utils.calculate_summary_metrics(daily_df, temp_unit=temp_symbol, precip_unit=precip_symbol)

# Current weather mappings
curr_code = current.get("weather_code", 0)
curr_is_day = current.get("is_day", 1)
curr_desc, curr_icon = utils.get_weather_info(curr_code, is_day=curr_is_day)
curr_temp = current.get("temperature_2m", "--")
curr_feels = current.get("apparent_temperature", "--")
curr_humidity = current.get("relative_humidity_2m", "--")
curr_wind = current.get("wind_speed_10m", "--")
curr_precip = current.get("precipitation", 0.0)
curr_pressure = current.get("surface_pressure", "--")

# Format local date/time
api_time_str = current.get("time", "")
if api_time_str:
    try:
        dt_obj = datetime.datetime.fromisoformat(api_time_str)
        local_time_display = dt_obj.strftime("%A, %B %d, %Y • %I:%M %p")
    except Exception:
        local_time_display = api_time_str
else:
    local_time_display = datetime.datetime.now().strftime("%A, %B %d, %Y")

today_high = daily_df.iloc[0]["temperature_2m_max"] if not daily_df.empty else "--"
today_low = daily_df.iloc[0]["temperature_2m_min"] if not daily_df.empty else "--"
today_uv = daily_df.iloc[0]["uv_index_max"] if not daily_df.empty and "uv_index_max" in daily_df.columns else "--"


# ---------------------------------------------------------
# 7. Dashboard Main View - Current Weather Section
# ---------------------------------------------------------
# Hero Banner
hero_html = f"""
<div class="hero-card">
    <div>
        <div class="hero-title">{st.session_state['selected_city_label']}</div>
        <div class="hero-subtitle">🕒 {local_time_display} | Timezone: {weather_data.get('timezone', 'Local')}</div>
        <div class="hero-temp">{curr_temp}{temp_symbol}</div>
        <div class="hero-condition">
            <span>{curr_icon}</span>
            <span>{curr_desc}</span>
        </div>
        <div class="hero-badge">Feels like {curr_feels}{temp_symbol} • High: {today_high}{temp_symbol} / Low: {today_low}{temp_symbol}</div>
    </div>
    <div style="text-align: right; margin-top: 10px;">
        <div style="font-size: 5rem; line-height: 1;">{curr_icon}</div>
        <div style="font-size: 0.85rem; opacity: 0.8; margin-top: 8px;">Lat: {active_city['latitude']:.2f}° | Lon: {active_city['longitude']:.2f}°</div>
    </div>
</div>
"""
st.markdown(hero_html, unsafe_allow_html=True)

# Key Metric Cards (Row of 5 columns)
mcol1, mcol2, mcol3, mcol4, mcol5 = st.columns(5)

with mcol1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-icon">💧</div>
        <div class="metric-label">Humidity</div>
        <div class="metric-value">{curr_humidity}%</div>
    </div>
    """, unsafe_allow_html=True)

with mcol2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-icon">💨</div>
        <div class="metric-label">Wind Speed</div>
        <div class="metric-value">{curr_wind} <span style="font-size: 0.85rem;">{wind_selection}</span></div>
    </div>
    """, unsafe_allow_html=True)

with mcol3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-icon">🌧️</div>
        <div class="metric-label">Precipitation</div>
        <div class="metric-value">{curr_precip} <span style="font-size: 0.85rem;">{precip_symbol}</span></div>
    </div>
    """, unsafe_allow_html=True)

with mcol4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-icon">☀️</div>
        <div class="metric-label">UV Index (Max)</div>
        <div class="metric-value">{today_uv}</div>
    </div>
    """, unsafe_allow_html=True)

with mcol5:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-icon">⏲️</div>
        <div class="metric-label">Air Pressure</div>
        <div class="metric-value">{curr_pressure} <span style="font-size: 0.85rem;">hPa</span></div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)


# ---------------------------------------------------------
# 8. 7-Day Forecast Cards
# ---------------------------------------------------------
st.markdown("### 📅 7-Day Weather Forecast")

if not daily_df.empty:
    card_cols = st.columns(min(7, len(daily_df)))
    for idx, row in daily_df.head(7).iterrows():
        with card_cols[idx]:
            rain_prob = row.get("precipitation_probability_max", 0)
            rain_sum = row.get("precipitation_sum", 0)
            rain_badge = f"{rain_prob:.0f}% rain" if pd.notna(rain_prob) and rain_prob > 0 else "0% rain"
            
            card_html = f"""
            <div class="forecast-card">
                <div>
                    <div class="forecast-day">{row['day_label']}</div>
                    <div class="forecast-date">{row['date_formatted']}</div>
                    <div class="forecast-icon">{row['weather_icon']}</div>
                    <div class="forecast-desc">{row['weather_desc']}</div>
                </div>
                <div>
                    <div class="forecast-temps">
                        <span style="color: #e11d48;">{row['temperature_2m_max']:.0f}°</span>
                        <span style="opacity: 0.4;"> / </span>
                        <span style="color: #2563eb;">{row['temperature_2m_min']:.0f}°</span>
                    </div>
                    <div class="forecast-rain">💧 {rain_badge}</div>
                </div>
            </div>
            """
            st.markdown(card_html, unsafe_allow_html=True)
else:
    st.warning("Daily forecast data is unavailable.")

st.markdown("<div style='height: 25px;'></div>", unsafe_allow_html=True)


# ---------------------------------------------------------
# 9. Interactive Visualizations (Plotly)
# ---------------------------------------------------------
st.markdown("### 📊 Interactive Visualizations")

tab1, tab2, tab3, tab4 = st.tabs([
    "🌡️ Temperature Trend",
    "🌧️ Precipitation & Rain",
    "💨 Wind Speeds",
    "⏱️ 24-Hour Forecast"
])

# ----------------- Tab 1: Temperature Trend Chart -----------------
with tab1:
    if not daily_df.empty:
        fig_temp = go.Figure()

        # Max Temperature Line
        fig_temp.add_trace(go.Scatter(
            x=daily_df["date_formatted"],
            y=daily_df["temperature_2m_max"],
            name=f"Max Temperature ({temp_symbol})",
            mode="lines+markers+text",
            text=[f"{v:.0f}°" for v in daily_df["temperature_2m_max"]],
            textposition="top center",
            line=dict(color="#ef4444", width=3, shape="spline"),
            marker=dict(size=8, color="#ef4444"),
            hovertemplate="<b>%{x}</b><br>Max Temp: <b>%{y:.1f}" + temp_symbol + "</b><extra></extra>"
        ))

        # Min Temperature Line with Shaded Area
        fig_temp.add_trace(go.Scatter(
            x=daily_df["date_formatted"],
            y=daily_df["temperature_2m_min"],
            name=f"Min Temperature ({temp_symbol})",
            mode="lines+markers+text",
            text=[f"{v:.0f}°" for v in daily_df["temperature_2m_min"]],
            textposition="bottom center",
            line=dict(color="#3b82f6", width=3, shape="spline"),
            fill="tonexty",
            fillcolor="rgba(59, 130, 246, 0.12)",
            marker=dict(size=8, color="#3b82f6"),
            hovertemplate="<b>%{x}</b><br>Min Temp: <b>%{y:.1f}" + temp_symbol + "</b><extra></extra>"
        ))

        fig_temp.update_layout(
            title=f"7-Day Temperature Range for {active_city['name']}",
            xaxis_title="Date",
            yaxis_title=f"Temperature ({temp_symbol})",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            hovermode="x unified",
            margin=dict(l=20, r=20, t=60, b=20),
            height=380
        )
        st.plotly_chart(fig_temp, use_container_width=True)
    else:
        st.info("No temperature trend data available.")


# ----------------- Tab 2: Precipitation Chart -----------------
with tab2:
    if not daily_df.empty and "precipitation_probability_max" in daily_df.columns:
        fig_precip = go.Figure()

        # Probability Bar
        fig_precip.add_trace(go.Bar(
            x=daily_df["date_formatted"],
            y=daily_df["precipitation_probability_max"],
            name="Rain Probability (%)",
            marker_color="rgba(14, 165, 233, 0.75)",
            marker_line=dict(color="#0284c7", width=1.5),
            text=[f"{v:.0f}%" for v in daily_df["precipitation_probability_max"]],
            textposition="outside",
            hovertemplate="<b>%{x}</b><br>Probability: <b>%{y:.0f}%</b><extra></extra>",
            yaxis="y1"
        ))

        # Rainfall Amount Line (Secondary Y-Axis)
        if "precipitation_sum" in daily_df.columns:
            fig_precip.add_trace(go.Scatter(
                x=daily_df["date_formatted"],
                y=daily_df["precipitation_sum"],
                name=f"Rain Amount ({precip_symbol})",
                mode="lines+markers",
                line=dict(color="#1e3a8a", width=3),
                marker=dict(size=7, color="#1e3a8a"),
                hovertemplate="<b>%{x}</b><br>Amount: <b>%{y:.1f} " + precip_symbol + "</b><extra></extra>",
                yaxis="y2"
            ))

        fig_precip.update_layout(
            title=f"Daily Precipitation Probability & Rainfall Amount ({active_city['name']})",
            xaxis_title="Date",
            yaxis=dict(title="Precipitation Probability (%)", range=[0, 110]),
            yaxis2=dict(
                title=f"Rainfall Amount ({precip_symbol})",
                overlaying="y",
                side="right",
                showgrid=False
            ),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            margin=dict(l=20, r=20, t=60, b=20),
            height=380
        )
        st.plotly_chart(fig_precip, use_container_width=True)
    else:
        st.info("Precipitation data unavailable.")


# ----------------- Tab 3: Wind Speeds Chart -----------------
with tab3:
    if not daily_df.empty and "wind_speed_10m_max" in daily_df.columns:
        fig_wind = go.Figure()

        fig_wind.add_trace(go.Bar(
            x=daily_df["date_formatted"],
            y=daily_df["wind_speed_10m_max"],
            name=f"Max Wind Speed ({wind_selection})",
            marker_color="rgba(16, 185, 129, 0.75)",
            marker_line=dict(color="#059669", width=1.5),
            text=[f"{v:.1f}" for v in daily_df["wind_speed_10m_max"]],
            textposition="outside",
            hovertemplate="<b>%{x}</b><br>Max Wind: <b>%{y:.1f} " + wind_selection + "</b><extra></extra>"
        ))

        fig_wind.update_layout(
            title=f"7-Day Maximum Wind Speed ({wind_selection})",
            xaxis_title="Date",
            yaxis_title=f"Wind Speed ({wind_selection})",
            margin=dict(l=20, r=20, t=50, b=20),
            height=380
        )
        st.plotly_chart(fig_wind, use_container_width=True)
    else:
        st.info("Wind speed data unavailable.")


# ----------------- Tab 4: 24-Hour Forecast Curve -----------------
with tab4:
    if not hourly_df.empty:
        fig_hourly = go.Figure()

        fig_hourly.add_trace(go.Scatter(
            x=hourly_df["time_label"],
            y=hourly_df["temperature_2m"],
            name=f"Temperature ({temp_symbol})",
            mode="lines+markers",
            line=dict(color="#f59e0b", width=3, shape="spline"),
            marker=dict(size=6, color="#d97706"),
            fill="tozeroy",
            fillcolor="rgba(245, 158, 11, 0.12)",
            hovertemplate="<b>%{x}</b><br>Temperature: <b>%{y:.1f}" + temp_symbol + "</b><extra></extra>"
        ))

        fig_hourly.update_layout(
            title=f"Next 24 Hours Temperature Variation in {active_city['name']}",
            xaxis_title="Time of Day",
            yaxis_title=f"Temperature ({temp_symbol})",
            margin=dict(l=20, r=20, t=50, b=20),
            height=380
        )
        st.plotly_chart(fig_hourly, use_container_width=True)
    else:
        st.info("Hourly forecast unavailable.")

st.markdown("<div style='height: 25px;'></div>", unsafe_allow_html=True)


# ---------------------------------------------------------
# 10. Data Analytics Summary & Pandas Data Table
# ---------------------------------------------------------
st.markdown("### 📈 Weekly Analytics & Data Insights")

scol1, scol2, scol3, scol4 = st.columns(4)
with scol1:
    st.metric("Avg Weekly High", summary_metrics.get("avg_max_temp", "--"))
    st.caption(f"Warmest Day: **{summary_metrics.get('warmest_day', '--')}**")

with scol2:
    st.metric("Avg Weekly Low", summary_metrics.get("avg_min_temp", "--"))
    st.caption(f"Coolest Day: **{summary_metrics.get('coolest_day', '--')}**")

with scol3:
    st.metric("Total Rain Expected", summary_metrics.get("total_rain", "--"))
    st.caption(f"Rainy Days: **{summary_metrics.get('rainy_days_count', '--')}**")

with scol4:
    st.metric("Peak Wind Speed", f"{summary_metrics.get('max_wind', '--')} {wind_selection}")
    st.caption(f"Peak Rain: **{summary_metrics.get('rainiest_day', '--')}**")

# Expandable Data Table & CSV Export
with st.expander("📋 View & Download Full Forecast Data (Pandas DataFrame)"):
    display_df = daily_df[[
        "day_label", "date_formatted", "weather_desc",
        "temperature_2m_max", "temperature_2m_min",
        "precipitation_probability_max", "precipitation_sum", "wind_speed_10m_max"
    ]].copy()

    display_df.columns = [
        "Day", "Date", "Condition",
        f"Max Temp ({temp_symbol})", f"Min Temp ({temp_symbol})",
        "Precipitation Prob (%)", f"Precipitation ({precip_symbol})", f"Max Wind ({wind_selection})"
    ]

    st.dataframe(display_df, use_container_width=True)

    csv_data = display_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Download Forecast CSV",
        data=csv_data,
        file_name=f"{active_city['name'].lower()}_weather_forecast.csv",
        mime="text/csv"
    )

# ---------------------------------------------------------
# 11. Footer
# ---------------------------------------------------------
st.markdown(f"""
<div class="footer-text">
    <strong>WeatherScope</strong> — Interactive Weather Forecast Website<br>
    Powered by <a href="https://open-meteo.com/" target="_blank">Open-Meteo API</a> • 
    Built with <strong>Python</strong>, <strong>Streamlit</strong>, <strong>Pandas</strong>, and <strong>Plotly</strong>.<br>
    BTech Data Analytics Portfolio Project.
</div>
""", unsafe_allow_html=True)
